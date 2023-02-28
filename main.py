import src

"""           FORTUNE            """
"""   ARA Development present    """
"""  First cryptography project  """

"""  Version 0.0.0               """
"""  Launched: 7 okt 2022        """


def main():
    api = src.api_binance.API("config/api_config.json")
    print("Hello from ARA Development!")


if __name__ == "__main__":
    main()
