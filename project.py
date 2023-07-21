import logging
import predictor

from src import api_binance, log_setup


class Fortune:
    CONFIG_PATH = './src/config/'

    def __init__(self):
        log_setup.configurate_logs(self.CONFIG_PATH + 'log_config.yml')
        self.logger = logging.getLogger(__class__.__name__)

        self.client = api_binance.configure_binance_api(self.CONFIG_PATH + api_binance.API.CLIENT_CONFIG_FILE)
        self.client.launch_price_update_subprocess(self.client.BTCUSDT, 1)

    def run(self):
        # p = predictor.Predictor()
        # print(p.predict([1, 23, 45, 6, 4]))
        
        self.logger.info("Fortune is running")

        for _ in range(4):
            print(self.client.await_price_update())

        self.client.terminate_price_update_subprocess()
