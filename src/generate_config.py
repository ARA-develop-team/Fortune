import json


def add_api_json(file):
    """ Creates an empty JSON configuration file at the specified path.

    :param file: The path and name of the configuration file to be created.
    :return: None
    """
    conf_dict = {"api-key": None, "api-secret": None}
    json_string = json.dumps(conf_dict)
    json_file = open(file, 'w')
    json_file.write(json_string)
    json_file.close()

    print("[Warning] api_config.json was created in config directory. \n"
          "Please, complete your details in it.")


if __name__ == '__main__':
    add_api_json('test')
