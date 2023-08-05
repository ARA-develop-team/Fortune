""" Fortune Module """

import logging
import random

from src import api_binance, log_setup
from trader import trader_service
from analyst import analyst_service


class Fortune:
    CONFIG_PATH = './src/config/'

    def __init__(self):
        log_setup.configurate_logs(self.CONFIG_PATH + 'log_config.yml')
        self.logger = logging.getLogger(__class__.__name__)

        self.client = api_binance.configure_binance_api(self.CONFIG_PATH + api_binance.API.CLIENT_CONFIG_FILE)
        self.trader = trader_service.Trader()
        self.analyst = analyst_service.Analyst()

    def process_iteration(self):
        print("process iteration...")
        exchange_rate = self.client.await_price_update()

        # TODO: Add Predictor Service here
        temp_vector = random.uniform(0.0, 1.0)

        decision = self.analyst.make_trading_decision(temp_vector)
        self.trader.demo_trade(decision, exchange_rate)

    def main_loop(self):
        while True:
            self.process_iteration()

    def run(self):
        self.logger.info("Fortune is running")
        self.client.launch_price_update_subprocess(self.client.BTCUSDT, 1)

        try:
            self.main_loop()
        except KeyboardInterrupt:
            self.logger.info("Fortune was terminated")
            self.client.terminate_price_update_subprocess()
            self.trader.terminate()
