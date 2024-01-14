import time
import pandas as pd

from .api_binance import API
from .api_binance import Client
from src import get_api_data

class FastTestingAPI(API):
    """ Binance API for testing. 
    Returns random last data with a short time interval"""

    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)

        self.logger.warning("You using Client for tesing purposes")

        self.number_of_klines = 100
        self.waiting_time = 3 # in seconds
        self.last_testing_data = self.load_last_prices(self.BTCUSDT, 
                                    Client.KLINE_INTERVAL_15MINUTE, 
                                    self.number_of_klines)

    def _get_new_kline(self, symbol, interval):
        pass

    def _update_kline(self, symbol, interval):
        pass

    def launch_price_update_subprocess(self, symbol, interval):
        pass

    def terminate_price_update_subprocess(self):
        pass

    def await_price_update(self):
        time.sleep(self.waiting_time)
        value = self.last_testing_data.sample(n=1)
        self.set_current_time_to_kline(value)
        return value
    
    def set_current_time_to_kline(self, kline: pd.DataFrame):
        kline['open_time'] = int(time.time()) * 1000
        kline['close_time'] = int(time.time()) * 1000 + (self.waiting_time * 1000)


def configure_binance_api(config_file):
    """ Configures the Binance API client.

    This function reads the API configuration data from the specified file, creates a Binance API client instance,
    and returns it.

    :raises FileNotFoundError: If the API configuration file is not found.
    :return: The configured Binance API client.
    """
    api_data = get_api_data(config_file)
    if api_data == -1:
        raise FileNotFoundError

    client = FastTestingAPI(*api_data)
    return client
