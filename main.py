import src

"""           FORTUNE            """
"""   ARA Development present    """
"""  First cryptography project  """

"""  Version 0.0.0               """
"""  Launched: 7 okt 2022        """


def main():
    api = src.api_binance.API("config/api_config.json")

    """Test"""
    start_data = api.load_data_history()
    prices_history = src.api_binance.select_prices(start_data)

    new_price = prices_history[-1]
    prices_history.pop()
    print("---Learning---")
    prediction = src.predict_arima(prices_history)

    print(f"Prediction: {prediction} <==> {new_price} Real price")
    print(f"Diff: {prediction - new_price}")
    print(f"Predicted Vector {prediction - prices_history[-1]} <==> {new_price - prices_history[-1]} Real Vector")
    """End Test"""


if __name__ == "__main__":
    print("Hello from ARA Development\n")
    main()
