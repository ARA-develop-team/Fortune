import json


def get_api_data(file_name):
    """ Parsing of API key and secret.
    :param file_name: - name of config file.
    :return: api_key and api_secret.
    """

    file = open(file_name, "r")
    data = json.load(file)
    return data['api-key'], data['api-secret']


if __name__ == "__main__":
    get_api_data("../config/api_config.json")
