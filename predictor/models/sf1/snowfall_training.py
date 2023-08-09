import os
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers import Dropout

from data_processing import reconstruct_data

from model_handler import ModelTrainer

class SnowfallTestTrain(ModelTrainer):
    def __init__(self, shape):
        super().__init__(shape)

        self.NUM_OF_PREV_ITEMS = self.input_shape[1]

        self.epochs = 50
        self.batch_size = 1000
        self.verbose = 2
        self.model = Sequential()
        self.model.add(LSTM(units=100, return_sequences=True, input_shape=shape))
        self.model.add(Dropout(0.5))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.3))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(units=1))

        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def train(self, train_data):
        train_data = np.reshape(train_data, (-1, 1))

        # min-max normalixation (inverse to (0, 1) range)
        data_transformed = self.scaler.fit_transform(train_data)

        train_x, train_y = reconstruct_data(data_transformed, self.NUM_OF_PREV_ITEMS)
        train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))

        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(train_x, train_y, epochs=self.epochs, batch_size=self.batch_size , verbose=self.verbose)

    def save_model(self, path):
        print(f"Model 'sf' saved to - {path}")
        self.model.save(path)
    
if __name__ == '__main__':
    data = read_csv('tmp.csv')
    data = data.astype('float32')
    model = SnowfallTestTrain(data, (12, 50))

    model.train_test()
    model.save_model('model_15m')
