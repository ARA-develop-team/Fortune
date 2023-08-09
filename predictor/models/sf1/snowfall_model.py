import numpy as np
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
import keras
import os

from .config_parser import get_network_data
from ..model_handler import ModelHandler

class Snowfall(ModelHandler):
    def __init__(self, model_name=None):
        PATH = os.path.dirname(__file__)

        self.model_name = model_name

        if model_name == None:
            data = get_network_data(os.path.join(PATH, "config.json"))
            relative_path = data["relative-path"]
        else:
            relative_path = model_name
        
        path_to_model = os.path.join(PATH, relative_path)
        self.model = keras.models.load_model(path_to_model)

        self.NUM_OF_PREV_ITEMS = self.model.layers[0].input_shape[2]

    def make_prediction(self, data_set):

        data_set = np.reshape(data_set, (-1, 1))

        # min-max normalixation (inverse to (0, 1) range)
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
    

if __name__ == '__main__':
    model = Snowfall()

    data = read_csv('BTC-USD.csv', usecols=[3])
    data = data.astype('float32')

    print(model.predict_next([[100], [123], [12], [34], [22]]))
