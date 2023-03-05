import src

"""           FORTUNE            """
"""   ARA Development present    """
"""  First cryptography project  """

"""  Version 0.0.0               """
"""  Launched: 7 okt 2022        """


def main():
    try:
        src.api_binance.API('./config/api_confg.json')
    except FileNotFoundError:
        return 0

    return 0


if __name__ == "__main__":
    main()
