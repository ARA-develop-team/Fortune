import unittest
import os
import json
import sys
from io import StringIO

import unit_tests    # append project path
from src.config_parser import get_api_data
from src.generate_config import add_api_json


class TestGenerateConfig(unittest.TestCase):
    def setUp(self):
        self.file_name = "test_api_config.json"
        sys.stdout = StringIO()
        add_api_json(self.file_name)

    def tearDown(self):
        os.remove(self.file_name)

    def test_add_api_json(self):
        self.assertTrue(os.path.exists(self.file_name))
        with open(self.file_name, "r") as f:
            conf_data = json.load(f)
        self.assertEqual(conf_data, {"api-key": None, "api-secret": None})

    def test_get_api_data(self):
        # Test case where file does not exist
        nonexistent_file_name = "nonexistent_file.json"
        if os.path.exists(nonexistent_file_name):
            os.remove(nonexistent_file_name)
        self.assertEqual(get_api_data(nonexistent_file_name), -1)
        self.assertTrue(os.path.exists(nonexistent_file_name))
        os.remove(nonexistent_file_name)

        # Test case where file exists but is empty
        empty_file_name = "test_empty_api_config.json"
        add_api_json(empty_file_name)
        self.assertEqual(get_api_data(empty_file_name), (None, None))
        os.remove(empty_file_name)

        # Test case where file exists and has valid data
        with open(self.file_name, "r") as f:
            conf_data = json.load(f)
        conf_data["api-key"] = "test_api_key"
        conf_data["api-secret"] = "test_api_secret"
        with open(self.file_name, "w") as f:
            json.dump(conf_data, f)

        self.assertEqual(get_api_data(self.file_name), ("test_api_key", "test_api_secret"))


if __name__ == '__main__':
    unittest.main()
