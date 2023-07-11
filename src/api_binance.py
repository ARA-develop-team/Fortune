""" Client API """

import time
import logging
import datetime

from multiprocessing import Process, Queue
from binance.client import Client

from . import get_api_data


class API(Client):
    """ Binance API """

    CLIENT_CONFIG_FILE = 'api_config.json'
    BTCUSDT = 'BTCUSDT'

    def __init__(self, api_key, api_secret):
        """
        :param api_key: The API key for accessing the Binance API.
        :param api_secret: The API secret for accessing the Binance API.
        """
        super().__init__(api_key, api_secret)

        self.price_queue = Queue()
        self._price_update_subprocess = None

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(f"Client configured successfully!")

    def _update_price(self, symbol, interval):
        """Retrieves the latest price for a given trading symbol and puts it into the price_queue.

        :param symbol: The trading pair symbol (e.g., 'BTCUSDT') for which to retrieve the price.
        :param interval: The interval length in minutes for fetching the klines data.
        :return: None
        """
        interval_in_seconds = interval * 60

        while True:
            response = self.get_avg_price(symbol=symbol)
            avg_price = response['price']
            self.price_queue.put(avg_price)
            self.logger.info(f"Price updated. Current rate is {avg_price}")
            time.sleep(interval_in_seconds)

    def launch_price_update_subprocess(self, symbol, interval):
        """Launches a subprocess to update the price for the given symbol at the specified interval.

        This function creates a new subprocess to continuously update the price for the specified trading symbol
        at the given interval. The subprocess runs the `_update_price` method internally.

        :param symbol: The trading pair symbol (e.g., 'BTCUSDT') for which to update the price.
        :param interval: The time interval at which to update the price, specified in minutes.
        :return: None
        """
        if self._price_update_subprocess is not None:
            self.logger.warning("There is already an active subprocess for updating prices.")
            return

        self._price_update_subprocess = Process(target=self._update_price, args=(symbol, interval))
        self._price_update_subprocess.start()
        self.logger.info("Price update subprocess was launched")

    def terminate_price_update_subprocess(self):
        """Terminates the subprocess responsible for updating the price.

        This function terminates the subprocess that is responsible for updating the price of a trading symbol.
        If no subprocess is currently running, the function returns without taking any action.

        :return: None
        """
        if self._price_update_subprocess is None:
            self.logger.warning("There is currently no active subprocess for updating prices.")
            return

        self._price_update_subprocess.terminate()
        self._price_update_subprocess = None
        self.logger.info("Price update subprocess was terminated")

    def await_price_update(self):
        """Waits for a price update by retrieving the latest price from the price queue.

        If the price queue is not empty, this function retrieves and discards all existing prices
        until the queue becomes empty. If the price queue is empty, the function waits and blocks until
        a new price is available in the queue.

        :return: The latest price retrieved from the price queue.
        """
        price = self.price_queue.get(block=True)
        while not self.price_queue.empty():
            price = self.price_queue.get()
        return price

    def load_price_history(self, symbol, interval):
        """Loads historical klines data for a specified symbol and time interval.

        This function retrieves historical klines data for the specified trading symbol with the provided time interval.
        The data is fetched starting from '1 Jan 2000' up to the current date and time.

        :param symbol: The trading pair symbol (e.g., 'BTCUSDT') for which to load historical data.
        :param interval: The time interval for the klines data (e.g., Client.KLINE_INTERVAL_15MINUTE).

        :return: A list of historical klines data.
        (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades,
        Taker buy base asset volume, Taker buy quote asset volume, Ignore)
        """

        end_date = datetime.datetime.now()
        one_day = datetime.timedelta(days=1)

        data = self.get_historical_klines(symbol, interval, start_str='1 Jan 2000', end_str=str(end_date))

        first_data_date = datetime.datetime.fromtimestamp(data[1][0] / 1000)
        last_data_date = datetime.datetime.fromtimestamp(data[-1][0] / 1000)
        self.logger.info(f"Price history loaded: \nFrom {first_data_date} to {last_data_date}")

        if last_data_date < (end_date - one_day):
            self.logger.warning("Price history retrieval is incomplete or unavailable")

        return data


def configure_binance_api(config_file):
    """Configures the Binance API client.

    This function reads the API configuration data from the specified file, creates a Binance API client instance,
    and returns it.

    :raises FileNotFoundError: If the API configuration file is not found.
    :return: The configured Binance API client.
    """
    api_data = get_api_data(config_file)
    if api_data == -1:
        raise FileNotFoundError

    client = API(*api_data)
    return client


if __name__ == '__main__':
    api = configure_binance_api('./config/api_config.json')
    prices = api.load_price_history(api.BTCUSDT, Client.KLINE_INTERVAL_15MINUTE)
    print(len(prices))
