import src

class Fortune:
    def test_api_client(self):
        src.log_setup.configurate_logs()
        try:
            src.api_binance.API()
        except FileNotFoundError:
            return 0

        return 0