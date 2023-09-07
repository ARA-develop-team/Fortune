""" Statistics Collector Module """
import os

import pandas as pd

import src.statistics.influxdb_client_app as influxdb_app

from src.statistics.record import StatisticsRecord


class StatisticsCollector:
    def __init__(self, config_path):
        self.influxdb_client = influxdb_app.configure_influx_client(os.path.join(config_path, 'influxdb_config.json'))

        self._active_record = StatisticsRecord()

    def add_klines(self, pair_name: str, default_df_klines: pd.DataFrame) -> None:
        df_klines = default_df_klines.drop(columns='ignore').copy()
        df_klines = df_klines.assign(pair=pair_name)
        self._active_record.insert_klines(df_klines)

    def push_record(self) -> None:
        self.influxdb_client.push_stats(self._active_record)
        # TODO send to PiGamma
        self._active_record = StatisticsRecord()
