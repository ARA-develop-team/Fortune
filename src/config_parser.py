import json
import logging

from src import generate_config


def get_api_data(file_name):
    """ This function reads an API key and API secret from a specified configuration file.

    :param file_name: The path and name of the configuration file.
    :return: A tuple containing the API key and API secret read from the configuration file,
     or -1 if the file cannot be opened or read.
    """
    try:
        file = open(file_name, "r")

    except FileNotFoundError as error:
        logging.error(f"[{error}] - {file_name}")
        generate_config.add_api_json(file_name)
        return -1

    data = json.load(file)
    return data['api-key'], data['api-secret']


if __name__ == "__main__":
    get_api_data("../config/api_config.json")
