import numpy as np
import keras
import os

from sklearn.preprocessing import MinMaxScaler

from predictor.models.model_handler import ModelHandler


class Snowfall(ModelHandler):
    SF_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, model_name='model_15m'):
        super().__init__()
        self.model_name = model_name

        path_to_model = os.path.join(self.SF_PATH, model_name)
        self.model = keras.models.load_model(path_to_model)

        self.NUM_OF_PREV_ITEMS = self.model.layers[0].input_shape[2]

    def make_prediction(self, data_set):
        data_set = np.reshape(data_set, (-1, 1))

        # min-max normalization (inverse to (0, 1) range)
        scaler = MinMaxScaler(feature_range=(0, 1))
        data = scaler.fit_transform(data_set)

        data = np.reshape(data, (-1, 1, self.NUM_OF_PREV_ITEMS))

        prediction = self.model.predict(np.array(data))

        # inverse from (0, 1) range to actual value
        prediction = scaler.inverse_transform(prediction)

        return prediction

    def predict_next(self, data_set):
        prediction = self.make_prediction(data_set)

        return prediction[0][0]
