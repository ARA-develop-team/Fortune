import numpy as np
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
import keras
import os

from .config_parser import get_network_data

class Snowfall():
    def __init__(self):
        data = get_network_data(os.path.join(os.path.dirname(__file__), "config.json"))
        relative_path = data["relative-path"]
        self.NUM_OF_PREV_ITEMS = data["num-of-privious-item"]


        path_to_model = os.path.join(os.path.dirname(__file__), relative_path)
        self.model = keras.models.load_model(path_to_model)


    def predict_next(self, data_set):
        """Predict next value using model"""

        # min-max normalixation (inverse to (0, 1) range)
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_set = np.reshape(data_set, (-1, 1))
        data = scaler.fit_transform(data_set)

        data = np.reshape(data, (1, 1, self.NUM_OF_PREV_ITEMS))

        prediction = self.model.predict(np.array(data))

        # inverse from (0, 1) range to actual value
        prediction = scaler.inverse_transform(prediction)

        return prediction
    

if __name__ == '__main__':
    model = Snowfall()

    data = read_csv('BTC-USD.csv', usecols=[3])
    data = data.astype('float32')

    print(model.predict_next([[100], [123], [12], [34], [22]]))
