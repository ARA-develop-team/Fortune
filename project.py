""" Fortune Module """

import os
import logging
import threading
import asyncio

from queue import Queue

import pandas as pd

from trader import trader_service
from analyst import analyst_service
from predictor import predictor_service

from src.statistics.statistics_collector import StatisticsCollector
from src.custom_types.noop_queue import NoopQueue
from src import api_binance
from src import discord_bot
from src import log_setup


class Fortune:
    CONFIG_PATH = os.path.abspath(os.path.expanduser('./src/config/'))

    def __init__(self, **kwargs):
        log_setup.configurate_logs(os.path.join(self.CONFIG_PATH, 'log_config.yml'))
        self.logger = logging.getLogger(__class__.__name__)
        self.exit_flag = asyncio.Event()
        self.run_pigamma = kwargs['pigamma']

        self.client = api_binance.configure_binance_api(os.path.join(self.CONFIG_PATH,
                                                                     api_binance.API.CLIENT_CONFIG_FILE))
        self.trader = trader_service.Trader()
        self.analyst = analyst_service.Analyst()
        self.predictor = predictor_service.Predictor()

        self.stats_collector = StatisticsCollector(self.CONFIG_PATH)
        self.stats_queue = Queue() if self.run_pigamma else NoopQueue()
        self.pigamma_thread = threading.Thread(target=self.configure_pigamma_wrapper)

        self.klines_dataframe = self.get_initial_klines()

    def configure_pigamma_wrapper(self):
        discord_bot.configure_pigamma(
            self.CONFIG_PATH + discord_bot.PiGamma.CONFIG_FILE,
            self.stats_queue,
            self.exit_flag
        )

    def get_initial_klines(self):
        """ The initial K-lines do not include the last price because it will be added at the beginning of the
        iteration. This is why it is essential to use 'load_last_prices_with_offset' instead of 'load_last_prices'.
        """
        return self.client.load_last_prices_with_offset(self.client.BTCUSDT, self.client.KLINE_INTERVAL_15MINUTE,
                                                        self.predictor.model_handler.NUM_OF_PREV_ITEMS)

    def add_kline(self, new_kline):
        """ Add a new K-line (price data point) to the existing DataFrame while removing the oldest kline and
        maintaining a fixed size.

        :param new_kline: A DataFrame representing the new kline data to be added.
        """
        self.klines_dataframe = self.klines_dataframe.iloc[1:]
        self.klines_dataframe = pd.concat([self.klines_dataframe, new_kline], ignore_index=True)

    def update_kline(self):
        new_kline = self.client.await_price_update()
        self.stats_collector.add_klines(self.client.BTCUSDT, new_kline)    # TODO solve BTCUSDT
        self.add_kline(new_kline)
        return float(new_kline['close'][0])

    def process_iteration(self):
        exchange_rate = self.update_kline()
        predicted_rate = self.predictor.predict(self.klines_dataframe)

        self.logger.info(f"Current rate: {exchange_rate}; Predicted Rate: {predicted_rate}")
        vector = analyst_service.calculate_vector(exchange_rate, predicted_rate)

        decision = self.analyst.make_trading_decision(vector)
        self.trader.demo_trade(decision, exchange_rate)

        self.stats_queue.put(self.trader.generate_stats(exchange_rate))
        self.stats_collector.push_record()

    def main_loop(self):
        while True:
            self.process_iteration()

    def terminate(self):
        self.logger.info("Fortune was terminated")
        self.exit_flag.set()
        self.trader.terminate()
        self.client.terminate_price_update_subprocess()
        if self.pigamma_thread.is_alive():
            self.pigamma_thread.join()

    def run(self):
        self.logger.info("Fortune is running")
        self.client.launch_price_update_subprocess(self.client.BTCUSDT, self.client.KLINE_INTERVAL_15MINUTE)
        self.stats_queue.put(self.trader.generate_stats())
        self.stats_collector.add_klines(self.client.BTCUSDT, self.klines_dataframe)
        if self.run_pigamma:
            self.pigamma_thread.start()

        try:
            self.main_loop()
        except KeyboardInterrupt:
            self.terminate()
