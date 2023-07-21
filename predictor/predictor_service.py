from .models.sf1.snowfall_model import Snowfall

class Predictor:
    def __init__(self):
        self.model_handler = Snowfall()

    def predict(self, data):
        return self.model_handler.predict_next(data)
