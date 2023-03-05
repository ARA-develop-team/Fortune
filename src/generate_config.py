import json


def add_api_json(file_name='api_config'):
    conf_dict = {"api-key": None, "api-secret": None}
    json_string = json.dumps(conf_dict)
    json_file = open(f"./config/{file_name}.json", 'w')
    json_file.write(json_string)
    json_file.close()

    print("[Warning] api_config.json was created in config directory. \nPlease, complete your details in it.")


if __name__ == '__main__':
    add_api_json('test')
