import logging

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
        The input `data` should be of the correct size, which can be found in the `model_handler` documentation
        or accessed using `self.model_handler.NUM_OF_PREV_ITEMS`.
        ("Snowfall" model by default use - 5, you can see it in config.json).

        :param data: list of numbers of correct size
        :return: predicted number
        """

        if len(data) == self.model_handler.NUM_OF_PREV_ITEMS:
            return self.model_handler.predict_next(data)
        else:
            massage = f"Data should be size of {self.model_handler.NUM_OF_PREV_ITEMS}, but not length - {len(data)}"
            self.logger.error(massage)
            return False
