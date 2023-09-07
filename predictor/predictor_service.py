import os
import logging
import numpy as np
from src.custom_types import shorten_kline_metric

from .models.sf1.snowfall_model import Snowfall
from predictor.models.model_testing.testing import ModelTesting
from predictor.models.sf1.snowfall_training import SnowfallTestTrain


class Predictor:
    def __init__(self):
        self.model_handler = Snowfall()
        self.logger = logging.getLogger(__class__.__name__)

    def predict(self, data: list) -> int:
        """
        Make predictions using a list of data.

        This method uses the `model_handler` to predict the next number based on the input `data`. 
        The input `data` should be of the correct size, which can be accessed using `self.model_handler.NUM_OF_PREV_ITEMS`.

        :param data: list of numbers of correct size
        :return: predicted number
        """
        if np.shape(data)[0] == self.model_handler.NUM_OF_PREV_ITEMS:
            return self.model_handler.predict_next(data)
        else:
            massage = f"The number of previous items should be {self.model_handler.NUM_OF_PREV_ITEMS}, but not - {np.shape(data)[0]}"         
            self.logger.error(massage)
            return False
        
    def train_main(self, data):
        output_data = data[['close']]
        input_data = data[shorten_kline_metric]
        model = SnowfallTestTrain((50, 10))
        Predictor._train(model, input_data, output_data, 'model_15m_50:10_all-c')

    def test(self, data: list):
        output_column = ['close']

        input_column1 = shorten_kline_metric
        model1 = Snowfall('model_15m_50:10_all-c')

        test = ModelTesting(data, 0.7, output_column)
        test.add_model(model1, input_column1)
        test.add_model(self.model_handler, ['close'])

        test.show_graph()

    def _train(model, input_data, output_data, save_file):
        model.train(input_data, output_data)
        model.save_model(os.path.join(model.PATH_TO_CONF, save_file))
