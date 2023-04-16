"""  Source Additional Directory

Provides all necessary functionality.
Contains config parser, main api class.

"""
import os

from src.config_parser import get_api_data

import src.log_setup
import src.generate_config
import src.api_binance

PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
print("*** ARA Development: Fortune ***\n"
      "All rights reserved!")
