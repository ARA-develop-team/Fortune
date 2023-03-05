import src

"""           FORTUNE            """
"""   ARA Development present    """
"""  First cryptography project  """

"""  Version 0.0.0               """
"""  Launched: 7 okt 2022        """


def main():
    try:
        src.api_binance.API('./config/api_config.json')
    except FileNotFoundError:
        print(f'[Warning] Cannot find api config file')
        src.generate_config.add_api_json()
        return

    return 0


if __name__ == "__main__":
    main()
