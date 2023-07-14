import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers import Dropout

from tensorflow import keras

class Snowfall():
    def __init__(self, model):
        self.model = model
        self.NUM_OF_PREV_ITEMS = 5

    def predict_next(self, data_set):
        """Predict next value using model"""

        # min-max normalixation (inverse to (0, 1) range)
        scaler = MinMaxScaler(feature_range=(0, 1))
        data = scaler.fit_transform(data_set)

        data = np.reshape(data, (1, 1, self.NUM_OF_PREV_ITEMS))

        prediction = self.model.predict(np.array(data))

        # inverse from (0, 1) range to actual value
        prediction = scaler.inverse_transform(prediction)

        return prediction
    

if __name__ == '__main__':
    model = Snowfall(keras.models.load_model('models/snowfall_1'))

    data = read_csv('BTC-USD.csv', usecols=[3])
    data = data.astype('float32')

    data = data[-5:]

    print(model.predict_next(data))
