""" Client API """


from src.config_parser import get_api_data
from binance.client import Client


class API:
    """ Binance API """
    def __init__(self, addr_config):
        self.client = Client(*get_api_data(addr_config))

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
