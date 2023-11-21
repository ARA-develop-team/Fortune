""" Statistics Record Module"""

import pandas as pd

from src.custom_types import kline_metric_statistics


class StatisticsRecord:
    def __init__(self):
        self.cryptocurrency_klines = pd.DataFrame(columns=kline_metric_statistics)
        self.prediction_record = None
        self.decision = None

    def insert_klines(self, df_klines):
        self.cryptocurrency_klines = pd.concat([self.cryptocurrency_klines, df_klines], ignore_index=True)

    def insert_prediction(self, prediction):
        self.prediction_record = prediction

    def insert_decision(self, decision):
        self.decision = decision

    def get_full_record(self):
        self.cryptocurrency_klines['prediction'] = int(self.prediction_record)
        self.cryptocurrency_klines['decision'] = int(self.decision)
        return self.cryptocurrency_klines
