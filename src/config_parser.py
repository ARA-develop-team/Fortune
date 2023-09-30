import json
import logging

from . import generate_config


def parse_json(file_path):
    """Reads and parses JSON data from the specified file.

    :param file_path: The path to the JSON file to be parsed.
    :return: dict or list or None
        The parsed JSON data if the file is successfully read and parsed.
        Returns None if the file is not found or if there's an error
        during the parsing process.
    """
    try:
        file = open(file_path, "r")

    except FileNotFoundError as error:
        logging.error(f"[{error}] - {file_path}")
        return None

    data = json.load(file)
    return data


def get_api_data(file):
    """This function reads an API key and API secret from a specified configuration file.

    :param file: The path and name of the configuration file.
    :return: A tuple containing the API key and API secret read from the configuration file,
        or -1 if the file cannot be opened or read.
    """
    data = parse_json(file)

    if data is None:
        generate_config.generate_api_json(file)
        return -1

    return data["api-key"], data["api-secret"]


def get_pigamma_data(file):
    """This function reads data from a specified configuration file for the Pigamma service.

    :param file: The path and name of the configuration file.
    :return: A dictionary containing data read from the configuration file,
        or None if the file cannot be opened or read.
    """
    data = parse_json(file)

    if data is None:
        generate_config.generate_pigamma_json(file)
        return None

    return data


if __name__ == "__main__":
    get_api_data("./config/api_config.json")
