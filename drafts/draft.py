import src
import asyncio
import json
from binance import AsyncClient

from binance.client import Client
# from config_parser import get_api_data
from binance import BinanceSocketManager

from datetime import datetime


def create_client():
    client = Client(*src.get_api_data("../config/api_config.json"))
    return client


def create_price_list():
    day_milli_sec = 86400000
    client = create_client()
    price_list = []

    dt_obj = datetime.strptime('14.06.2022 00:00:00,00',
                               '%d.%m.%Y %H:%M:%S,%f')

    milli_sec = dt_obj.timestamp() * 1000

    for i in range(61):
        price = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, int(milli_sec))
        price_list.append(price[0][2])
        milli_sec += day_milli_sec

    return price_list


if __name__ == "__main__":
    test_list = create_price_list()
    print(test_list)

    # bsm = BinanceSocketManager(client)
    # socket = bsm.trade_socket('BTCUSDT')
    #
    # await socket.__aenter__()
    # msg = await socket.recv()
    # print(msg)
    # print('\n')
    #
    # info = client.get_symbol_info('BNBBTC')
    #
    # res = client.get_exchange_info()
    # print(info)

    # res = client.get_avg_price(symbol='BTCBUSD')
    # res = client.get_historical_trades(symbol='BNBBTC')
    # res = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, "03 Oct, 2022")
    # print(res)
    # print(datetime.datetime.strptime('1655683200000', '%Y%m%d'))
