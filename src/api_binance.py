""" Client API """

import src
import logging

from binance.client import Client


API_CONFIG_FILE = '/config/api_config.json'


class API:
    """ Binance API """

    def __init__(self):
        api_data = src.get_api_data(src.PROJECT_PATH + API_CONFIG_FILE)
        if api_data == -1:
            raise FileNotFoundError

        self.client = Client()
        logging.info("API client configured successfully")

    def load_data_history(self):
        # TODO change date to automated counter
        return self.client.get_historical_klines('BTCBUSD', Client.KLINE_INTERVAL_1DAY, '3 Sep 2020')

    def load_new_data(self):
        pass


def select_prices(all_data):
    # TODO decide how to organize this func.
    prices = []
    for data in all_data:
        prices.append(float(data[4]))

    return prices
