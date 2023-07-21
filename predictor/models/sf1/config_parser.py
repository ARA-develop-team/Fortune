import json
import logging

def get_network_data(file_name):
    try:
        file = open(file_name, "r")

    except FileNotFoundError as error:
        massage = f"[{error}] - {file_name}"
        logging.error(massage)
        raise FileNotFoundError(massage)
    data = json.load(file)
    return data
