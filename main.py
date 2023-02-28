import src

"""           FORTUNE            """
"""   ARA Development present    """
"""  First cryptography project  """

"""  Version 0.0.0               """
"""  Launched: 7 okt 2022        """


def main():
    print("Hello from ARA Development!")

    try:
        api = src.api_binance.API("config/api_config.json")

    except FileNotFoundError:
        print("Config file not found!!!")
        # TODO generate config file

    return 0


if __name__ == "__main__":
    main()
