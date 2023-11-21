""" Statistics Collector Module """
import os

import pandas as pd

import src.statistics.influxdb_client_app as influxdb_app

from src.statistics.record import StatisticsRecord

from src import api_binance
# uncomment the line below and comment above to use testing_api_binance
# from src import testing_api_binance as api_binance

class StatisticsCollector:
    def __init__(self, config_path, num_of_prev_items):
        self.influxdb_client = influxdb_app.configure_influx_client(os.path.join(config_path, 'influxdb_config.json'))
        
        self.client = api_binance.configure_binance_api(os.path.join(config_path,
                                                                api_binance.API.CLIENT_CONFIG_FILE))
        self.pair = self.client.BTCUSDT
        self.NUM_OF_PREV_ITEMS = num_of_prev_items
        self.klines_dataframe = self.get_initial_klines()
        self._active_record = StatisticsRecord()

    def push_record(self) -> None:
        self.influxdb_client.push_stats(self._active_record)
        # TODO send to PiGamma
        self._active_record = StatisticsRecord()
    
    def add_prediction(self, prediction: float) -> None: 
        self._active_record.insert_prediction(prediction)

    def add_decision(self, decision: float) -> None: 
        self._active_record.insert_decision(decision)

    def wait_for_update(self): 
        new_kline = self.client.await_price_update()

        self.klines_dataframe = self.klines_dataframe.iloc[1:]

        self.klines_dataframe = pd.concat([self.klines_dataframe, new_kline], 
                                          ignore_index=True)
        # TODO solve BTCUSDT
        df_klines = new_kline.drop(columns='ignore').copy()
        df_klines = df_klines.assign(pair=self.pair)
        self._active_record.insert_klines(df_klines)


    def get_initial_klines(self):
        """ The initial K-lines do not include the last price because it will be added at the beginning of the
        iteration. This is why it is essential to use 'load_last_prices_with_offset' instead of 'load_last_prices'.
        """
        return self.client.load_last_prices(self.client.BTCUSDT, self.client.KLINE_INTERVAL_15MINUTE,
                                                        self.NUM_OF_PREV_ITEMS)

    def launch_price_update_subprocess(self):
        self.client.launch_price_update_subprocess(self.client.BTCUSDT, self.client.KLINE_INTERVAL_15MINUTE)

    def terminate_price_update_subprocess(self):
        self.client.terminate_price_update_subprocess()
