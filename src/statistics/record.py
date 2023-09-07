""" Statistics Record Module"""

import pandas as pd

from src.custom_types import kline_metric_statistics


class StatisticsRecord:
    def __init__(self):
        self.cryptocurrency_klines = pd.DataFrame(columns=kline_metric_statistics)
        self.prediction_record = pd.DataFrame(columns=['pair', 'prediction'])

    def insert_klines(self, df_klines):
        self.cryptocurrency_klines = pd.concat([self.cryptocurrency_klines, df_klines], ignore_index=True)
