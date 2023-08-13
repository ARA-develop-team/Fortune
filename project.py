""" Fortune Module """

import logging
import random
import threading
import asyncio

from queue import Queue

from trader import trader_service
from analyst import analyst_service

from src.noop_queue import NoopQueue
from src import api_binance
from src import discord_bot
from src import log_setup


class Fortune:
    CONFIG_PATH = './src/config/'

    def __init__(self, **kwargs):
        log_setup.configurate_logs(self.CONFIG_PATH + 'log_config.yml')
        self.logger = logging.getLogger(__class__.__name__)
        self.exit_flag = asyncio.Event()
        self.run_pigamma = kwargs['pigamma']

        self.client = api_binance.configure_binance_api(self.CONFIG_PATH + api_binance.API.CLIENT_CONFIG_FILE)
        self.trader = trader_service.Trader()
        self.analyst = analyst_service.Analyst()

        self.stats_queue = Queue() if self.run_pigamma else NoopQueue()
        self.pigamma_thread = threading.Thread(target=self.configure_pigamma_wrapper)

    def configure_pigamma_wrapper(self):
        discord_bot.configure_pigamma(
            self.CONFIG_PATH + discord_bot.PiGamma.CONFIG_FILE,
            self.stats_queue,
            self.exit_flag
        )

    def process_iteration(self):
        exchange_rate = self.client.await_price_update()

        # TODO: Add Predictor Service here
        temp_vector = random.uniform(0.0, 1.0)

        decision = self.analyst.make_trading_decision(temp_vector)
        self.trader.demo_trade(decision, exchange_rate)
        self.stats_queue.put(self.trader.generate_stats(exchange_rate))

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
        self.client.launch_price_update_subprocess(self.client.BTCUSDT, 1)
        self.stats_queue.put(self.trader.generate_stats())
        if self.run_pigamma:
            self.pigamma_thread.start()

        try:
            self.main_loop()

        except KeyboardInterrupt:
            self.terminate()
