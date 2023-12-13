import os
import logging
import numpy as np

from pandas import DataFrame

from predictor.models.sf1.snowfall_model import Snowfall


class Predictor:
    def __init__(self):
        self.model_handler = Snowfall()
        self.logger = logging.getLogger(__class__.__name__)

    def predict(self, data: DataFrame) -> int:
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
