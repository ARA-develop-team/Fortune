import unittest
import os
import json
from src.generate_config import generate_json, generate_api_json, generate_pigamma_json


class TestGenerateJsonFunctions(unittest.TestCase):
    def setUp(self):
        self.test_data = {"name": "John", "age": 30}
        self.test_file = "test_file.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_generate_json(self):
        generate_json(self.test_file, self.test_data)
        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, "r") as file:
            data_from_file = json.load(file)
            self.assertEqual(data_from_file, self.test_data)

    def test_generate_api_json(self):
        generate_api_json(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        expected_data = {"api-key": None, "api-secret": None}
        with open(self.test_file, "r") as file:
            data_from_file = json.load(file)
            self.assertEqual(data_from_file, expected_data)

    def test_generate_pigamma_json(self):
        generate_pigamma_json(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        expected_data = {"TOKEN": None, "CHANNEL_ID": None}
        with open(self.test_file, "r") as file:
            data_from_file = json.load(file)
            self.assertEqual(data_from_file, expected_data)


if __name__ == "__main__":
    unittest.main()
