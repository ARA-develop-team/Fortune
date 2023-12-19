import json


def generate_json(file: str, data: dict):
    """Generates a JSON file with the provided data dictionary.

    :param file: The path and name of the JSON file to be created.
    :param data: The dictionary containing data to be written to the JSON file.
    """
    json_string = json.dumps(data)
    json_file = open(file, "w")
    json_file.write(json_string)
    json_file.close()


def generate_api_json(file: str):
    """Creates an API JSON configuration file at the specified path.

    This function generates a new JSON configuration file for API settings at the provided file path. The file will
    contain keys for "api-key" and "api-secret," initially set to None to be filled with actual API credentials later.

    :param file: The path and name of the API configuration file to be created.
    """
    conf_dict = {"api-key": None, "api-secret": None}
    generate_json(file, conf_dict)
    print(f"[Warning] API config file {file} was created.\n" "Please, complete your details in it.")


def generate_pigamma_json(file: str):
    """Creates a PiGamma JSON configuration file at the specified path.

    This function generates a new JSON configuration file for PiGamma settings at the provided file path. The file will
    contain keys for "TOKEN" and "CHANNEL_ID" initially set to None, to be filled with the required values later.

    :param file: The path and name of the PiGamma configuration file to be created.
    """
    conf_dict = {"TOKEN": None, "CHANNEL_ID": None}
    generate_json(file, conf_dict)
    print(f"[Warning] PiGamma config file {file} was created.\n" "Please, complete your details in it.")


if __name__ == "__main__":
    generate_api_json("test")
