import unittest
import tempfile
import json
import logging
from unittest.mock import patch
from src.config_parser import get_api_data, get_pigamma_data

# Disable logging during testing
logging.disable(logging.CRITICAL)


def create_temp_file(data):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w") as f:
        json.dump(data, f)
    return temp_file.name


class TestFileParsing(unittest.TestCase):
    def setUp(self):
        self.config_data = {"api-key": "your-api-key", "api-secret": "your-api-secret"}

    def tearDown(self):
        pass

    def test_get_api_data_valid_file(self):
        file_path = create_temp_file(self.config_data)
        api_key, api_secret = get_api_data(file_path)
        self.assertEqual(api_key, self.config_data["api-key"])
        self.assertEqual(api_secret, self.config_data["api-secret"])

    def test_get_api_data_invalid_file(self):
        file_path = "non_existent_file.json"
        with patch("src.config_parser.generate_config.generate_api_json"):
            result = get_api_data(file_path)
        self.assertEqual(result, -1)

    def test_get_pigamma_data_valid_file(self):
        pigamma_data = {"some_key": "some_value"}
        file_path = create_temp_file(pigamma_data)
        data = get_pigamma_data(file_path)
        self.assertEqual(data, pigamma_data)

    def test_get_pigamma_data_invalid_file(self):
        file_path = "non_existent_file.json"
        with patch("src.config_parser.generate_config.generate_pigamma_json"):
            result = get_pigamma_data(file_path)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()
