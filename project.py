import logging
import src


class Fortune:
    def __init__(self):
        src.log_setup.configurate_logs()
        self.client = src.api_binance.configure_binance_api()

        self.logger = logging.getLogger(__class__.__name__)

    def run(self):
        pass
