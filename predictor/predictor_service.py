import logging
from numpy import shape

from .models.sf1.snowfall_model import Snowfall


class Predictor:
    def __init__(self):
        self.model_handler = Snowfall('model_15m_50:1_c-c')
        self.logger = logging.getLogger(__class__.__name__)

    def predict(self, data: list) -> int:
        """
        Make predictions using a list of data.

        This method uses the `model_handler` to predict the next number based on the input `data`. 
        The input `data` should be of the correct size, which can be found in the `model_handler` documentation
        or accessed using `self.model_handler.NUM_OF_PREV_ITEMS`.
        ("Snowfall" model by default use - 5, you can see it in config.json).

        :param data: list of numbers of correct size
        :return: predicted number
        """

        if shape(data) == self.model_handler.input_shape:
            return self.model_handler.predict_next(data)
        else:
            massage = f"Data should be shape of {self.model_handler.input_shape}, but not - {shape(data)}"         
            self.logger.error(massage)
