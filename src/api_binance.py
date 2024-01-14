""" Client API """

import csv
import time
import logging
import datetime

from multiprocessing import Process, Queue

import pandas as pd
import humanfriendly

from binance.client import Client
from requests.exceptions import RequestException

import src.custom_types as custom_types

from src import get_api_data


def convert_timestamp_to_str(timestamp):
    dt_object = datetime.date.fromtimestamp(timestamp / 1000)
    return dt_object.strftime('%-d %b %Y')


def convert_columns_to_numeric(df_klines: pd.DataFrame) -> pd.DataFrame:
    df_klines[custom_types.kline_float_columns] = df_klines[custom_types.kline_float_columns].astype(float)
    df_klines[custom_types.kline_int_columns] = df_klines[custom_types.kline_int_columns].astype(int)
    # TODO converting to int doesn't work properly
    return df_klines


def convert_klines_to_dataframe(klines) -> pd.DataFrame:
    dataframe = pd.DataFrame(klines, columns=custom_types.kline_metric)
    return convert_columns_to_numeric(dataframe)


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
        self.logger.info(f"Client was configured successfully!")

    def _get_new_kline(self, symbol, interval):
        try:
            response_ = self.futures_klines(symbol=symbol, interval=interval, limit=1)
        except RequestException as exception:
            self.logger.error(f"Unable to retrieve the latest price!\n{exception}")
            return None

        if not response_:
            self.logger.error(f"Failed to retrieve the latest price due to an empty response.\nR: {response_}")
            return None

        elif len(response_) > 1:
            self.logger.warning(f"Expected response size: 1, but received: {len(response_)}\nR: {response_}")
            return [response_[-1]]

        return response_

    def _update_kline(self, symbol, interval):
        """ Retrieves the latest price K-line for a given trading symbol and puts it into the price_queue.

        :param symbol: The trading pair symbol (e.g. 'BTCUSDT') for which to retrieve the price.
        :param interval: The kline interval length for fetching the klines data (e.g. KLINE_INTERVAL_15MINUTE).
        :return: None
        """
        interval_in_seconds = humanfriendly.parse_timespan(interval)

        while True:
            time.sleep(interval_in_seconds)
            new_kline = self._get_new_kline(symbol, interval)
            if new_kline is None:
                continue

            record = convert_klines_to_dataframe(new_kline)

            self.price_queue.put(record)
            self.logger.info(f"Price successfully updated.")


    def launch_price_update_subprocess(self, symbol, interval):
        """ Launches a subprocess to update the price for the given symbol at the specified interval.

        This function creates a new subprocess to continuously update the price for the specified trading symbol
        at the given interval. The subprocess runs the `_update_kline` method internally.

        :param symbol: The trading pair symbol (e.g., 'BTCUSDT') for which to update the price.
        :param interval: The time kline interval at which to update the price (e.g. KLINE_INTERVAL_15MINUTE).
        :return: None
        """
        if self._price_update_subprocess is not None:
            self.logger.warning("There is already an active subprocess for updating prices.")
            return

        self._price_update_subprocess = Process(target=self._update_kline, args=(symbol, interval))
        self._price_update_subprocess.daemon = True
        self._price_update_subprocess.start()
        self.logger.info("Price update subprocess was launched")

    def terminate_price_update_subprocess(self):
        """ Terminates the subprocess responsible for updating the price.

        This function terminates the subprocess that is responsible for updating the price of a trading symbol.
        If no subprocess is currently running, the function returns without taking any action.

        :return: None
        """
        if self._price_update_subprocess is None:
            self.logger.warning("There is currently no active subprocess for updating prices.")
            return

        if not self._price_update_subprocess.is_alive:
            self.logger.info("Price update subprocess is not alive.")
            return

        self._price_update_subprocess.terminate()
        self._price_update_subprocess.join()
        self._price_update_subprocess = None
        self.logger.info("Price update subprocess was terminated.")

    def await_price_update(self):
        """ Waits for a price update by retrieving the latest price from the price queue.

        If the price queue is not empty, this function retrieves and discards all existing prices
        until the queue becomes empty. If the price queue is empty, the function waits and blocks until
        a new price is available in the queue.

        :return: The latest kline retrieved from the price queue. If the subprocess for updating prices is not running
        or is not alive, 'None' value will be returned.
        """
        if not self._price_update_subprocess or not self._price_update_subprocess.is_alive():
            self.logger.error("Subprocess for updating prices is not running!")
            return None

        price = self.price_queue.get(block=True)
        while not self.price_queue.empty():
            price = self.price_queue.get()

        return price

    def load_price_history(self, symbol, interval):
        """ Loads historical klines data for a specified symbol and time interval.

        This function retrieves historical klines data for the specified trading symbol with the provided time interval.
        The data is fetched starting from '1 Jan 2000' up to the current date and time.

        :param symbol: The trading pair symbol (e.g., 'BTCUSDT') for which to load historical data.
        :param interval: The time interval for the klines data (e.g., Client.KLINE_INTERVAL_15MINUTE).

        :return: A list of historical klines data.
        (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades,
        Taker buy base asset volume, Taker buy quote asset volume, Ignore)
        """

        all_data = []
        end_date = datetime.datetime.now().strftime('%-d %b %Y')
        limit = 1000

        while True:
            data = self.get_historical_klines(symbol, interval, end_str=end_date, limit=limit)
            all_data = data + all_data
            if len(data) < limit:
                break

            end_date = convert_timestamp_to_str(data[0][0])
            print(f"\rLoading price history: {end_date}", end="", flush=True)
        print(f"\rLoading price history: DONE", end="\n", flush=True)

        first_data_date = convert_timestamp_to_str(all_data[1][0])
        last_data_date = convert_timestamp_to_str(all_data[-1][0])
        self.logger.info(f"Price history loaded: \nFrom {first_data_date} to {last_data_date}")

        return all_data

    def _check_column_for_duplicates(self, data, column_index):
        column_values = [row[column_index] for row in data]

        seen_values = set()
        for value in column_values:
            if value in seen_values:
                self.logger.warning("Data duplicity occurs!")
                return
            seen_values.add(value)

        self.logger.info("No data duplication was detected")

    def save_price_history_csv(self, symbol, interval, file_path):
        """ Save price history data to CSV

        :param symbol: The trading pair symbol (e.g., 'BTCUSDT') for which to load historical data.
        :param interval: The time interval for the klines data (e.g., Client.KLINE_INTERVAL_15MINUTE).
        :param file_path: File path to save data, which may not currently exist.

        :return: The path to the newly created/updated file.
        """
        data = self.load_price_history(symbol, interval)
        self._check_column_for_duplicates(data, 0)

        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(custom_types.kline_metric)
            csv_writer.writerows(data)

        self.logger.info(f"Saved {len(data)} records to \n{file_path}")
        return file_path

    def load_last_prices(self, symbol, interval, limit):
        """ Load the last 'limit' price data points for a given trading symbol and time interval.

        :param symbol: The trading symbol (e.g., 'BTCUSDT').
        :param interval: The time interval (e.g., Client.KLINE_INTERVAL_15MINUTE).
        :param limit: The maximum number of data points to retrieve.

        :return: A DataFrame containing the price data.
        """
        klines = self.futures_klines(symbol=symbol, interval=interval, limit=limit)
        return convert_klines_to_dataframe(klines)

    def load_last_prices_with_offset(self, symbol, interval, limit):
        """ Load the last 'limit' price data points for a given trading symbol and time interval, excluding the last
        data point.

        :param symbol: The trading symbol (e.g., 'BTCUSDT').
        :param interval: The time interval (e.g., Client.KLINE_INTERVAL_15MINUTE).
        :param limit: The maximum number of data points to retrieve, excluding the last data point.

        :return: A DataFrame containing the price data, excluding the last data point.
        """
        df_klines = self.load_last_prices(symbol, interval, limit + 1)
        return df_klines.drop(df_klines.index[-1])


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

    client = API(*api_data)
    return client



if __name__ == '__main__':
    api = configure_binance_api('./config/api_config.json')
    prices = api.load_price_history(api.BTCUSDT, Client.KLINE_INTERVAL_15MINUTE)
    api.save_price_history_csv(api.BTCUSDT, api.KLINE_INTERVAL_15MINUTE, "./tmp.csv")
    print(len(prices))
