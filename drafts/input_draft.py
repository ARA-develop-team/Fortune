import src

from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd


def main():
    client = Client(*src.get_api_data("../config/api_config.json"))

    # tickers = client.get_all_tickers()
    # tickers_df = pd.DataFrame(tickers)
    #
    # print(tickers_df)

    historical = client.get_historical_klines('BTCBUSD', Client.KLINE_INTERVAL_1MINUTE, '30 Okt 2022')
    for value in historical:
        print(value[1], value[2], value[3], value[4])


if __name__ == '__main__':
    main()
