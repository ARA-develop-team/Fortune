import numpy as np
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
import keras
import os
import pickle

from ..model_handler import ModelHandler

class Snowfall(ModelHandler):
    def __init__(self, model_name='model_15m'):
        PATH = os.path.dirname(__file__)

        self.model_name = model_name

        path_to_model = os.path.join(PATH, model_name)
        self.model = keras.models.load_model(path_to_model)

        with open(os.path.join(PATH, model_name, 'input_scaler'),'rb') as f:
            self.input_scaler = pickle.load(f)

        with open(os.path.join(PATH, model_name, 'output_scaler'),'rb') as f:
            self.output_scaler = pickle.load(f)

        self.input_shape = self.model.layers[0].input_shape[1:]

        self.NUM_OF_PREV_ITEMS = self.model.layers[0].input_shape[1]

    def make_prediction(self, data_set):

        n_data_set = np.reshape(data_set, (-1, self.input_shape[1]))
        # min-max normalixation (inverse to (0, 1) range)
        data = self.input_scaler.transform(n_data_set)
        data = np.reshape(data, (-1, self.NUM_OF_PREV_ITEMS, self.input_shape[1]))

        # data = np.reshape(data, (-1, 1, self.NUM_OF_PREV_ITEMS))

        prediction = self.model.predict(np.array(data))

        # inverse from (0, 1) range to actual value
        # prediction = np.reshape(prediction, (1, -1))
        prediction = self.output_scaler.inverse_transform(prediction)

        return prediction

    def predict_next(self, data_set):
        prediction = self.make_prediction(data_set)

        return prediction[0][0]
    
