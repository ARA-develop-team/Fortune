import logging

from .models.sf1.snowfall_model import Snowfall


class Predictor:
    def __init__(self):
        self.model_handler = Snowfall()
        self.logger = logging.getLogger(__class__.__name__)

    def predict(self, data):
        if len(data) == self.model_handler.NUM_OF_PREV_ITEMS:
            return self.model_handler.predict_next(data)
        else:
            massage = f"[Error] Data should be size of {self.model_handler.NUM_OF_PREV_ITEMS}, get lenght - {len(data)}"         
            self.logger.error(massage)
