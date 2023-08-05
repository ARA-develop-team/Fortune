import yaml
import logging
import logging.config
import time


def configurate_logs(file):
    try:
        with open(file) as cfg_file:
            config = yaml.safe_load(cfg_file.read())

    except FileNotFoundError:
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logging.error("[FileNotFoundError] Logs were not configured properly!")

    else:
        timestamp = time.strftime('%Y-%m-%d_(%H-%M-%S)', time.localtime())
        config["handlers"]["file_handler"]["filename"] = f"./logs/{timestamp}.log"

        logging.config.dictConfig(config)
        logging.info("Logs were configured successfully.")


if __name__ == '__main__':
    configurate_logs("./config/log_config.yml")

