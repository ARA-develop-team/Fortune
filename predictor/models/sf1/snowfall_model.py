import numpy as np
import keras
import os
import pickle

from predictor.models.model_handler import ModelHandler


def parse_dataframe(dataframe):
    return dataframe["close"].astype(float)


class Snowfall(ModelHandler):
    def __init__(self, model_name='model_15m_50:1_c-c'):
        super().__init__()
        self.model_name = model_name

        path_to_model = os.path.join(self.PATH_TO_CONF, model_name)
        self.model = keras.models.load_model(path_to_model)
        
        with open(os.path.join(ModelHandler.PATH_TO_CONF, model_name, 'input_scaler'),'rb') as f:
            self.input_scaler = pickle.load(f)

        with open(os.path.join(ModelHandler.PATH_TO_CONF, model_name, 'output_scaler'),'rb') as f:
            self.output_scaler = pickle.load(f)

        self.input_shape = self.model.layers[0].input_shape[1:]

        self.NUM_OF_PREV_ITEMS = self.model.layers[0].input_shape[1]

    def make_prediction(self, data_set):

        n_data_set = np.reshape(data_set, (-1, self.input_shape[1]))

        # min-max normalization (inverse to (0, 1) range)
        data = self.input_scaler.transform(n_data_set)

        data = np.reshape(data, (-1, self.NUM_OF_PREV_ITEMS, self.input_shape[1]))
        prediction = self.model.predict(np.array(data))

        # inverse from (0, 1) range to actual value
        # prediction = np.reshape(prediction, (1, -1))
        prediction = self.output_scaler.inverse_transform(prediction)

        return prediction

    def predict_next(self, dataframe):
        prediction = self.make_prediction(parse_dataframe(dataframe))

        return prediction[0][0]
