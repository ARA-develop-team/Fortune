""" InfluxDB Client Module """

import pandas as pd
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


from src import config_parser
from src.statistics.record import StatisticsRecord


class InfluxClient(influxdb_client.InfluxDBClient):
    def __init__(self, url, token, org, bucket, **kwargs):
        super().__init__(url=url, token=token, org=org, **kwargs)
        self.write_api = self.write_api(write_options=SYNCHRONOUS)
        self.default_bucket = bucket

    def write_klines(self, df_klines: pd.DataFrame) -> None:
        tag = df_klines.columns[0]
        df_klines.set_index(df_klines.columns[1], inplace=True)
        df_klines.index = pd.to_datetime(df_klines.index, unit='ms')

        self.write_api.write(self.default_bucket, self.org, record=df_klines,
                             data_frame_measurement_name="cryptocurrency_market", data_frame_tag_column=[tag])

    def push_stats(self, stats: StatisticsRecord) -> None:
        kline = stats.get_full_record()
        
        if len(kline) > 0:
            self.write_klines(kline.assign())


def configure_influx_client(config_path):
    config = config_parser.get_influxdb_data(config_path)
    return InfluxClient(config["URL"], config["TOKEN"], config["ORG"], config["BUCKET"])


if __name__ == '__main__':
    db_client = configure_influx_client("../config/influxdb_config.json")
