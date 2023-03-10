import json
import logging

from src import generate_config


def get_api_data(file_name):
    """ Parsing of API key and secret.
    :param file_name: - name of config file.
    :return: api_key and api_secret.
    """
    try:
        file = open(file_name, "r")

    except FileNotFoundError:
        logging.error("[FileNotFoundError] - ./config/api_config.json")
        if file_name == "./config/api_config.json":
            print(f'[Warning] Cannot find api config file')
            generate_config.add_api_json()
        return -1

    data = json.load(file)
    return data['api-key'], data['api-secret']


if __name__ == "__main__":
    get_api_data("../config/api_config.json")
