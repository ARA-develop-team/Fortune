import src
import logging

"""           FORTUNE            """
"""   ARA Development present    """
"""  First cryptography project  """

"""  Version 0.0.0               """
"""  Launched: 7 okt 2022        """


def main():
    src.log_setup.configurate_logs()
    try:
        src.api_binance.API('./config/api_config.json')
    except FileNotFoundError:
        return 0

    return 0


if __name__ == "__main__":
    main()
