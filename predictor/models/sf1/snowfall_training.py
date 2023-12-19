import os
import numpy as np
import pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from keras.layers import Dropout

from sklearn.preprocessing import MinMaxScaler

from predictor.models.data_processing import reconstruct_data
from predictor.models.model_handler import ModelTrainer


class SnowfallTestTrain(ModelTrainer):
    def __init__(self, shape):
        super().__init__(shape)

        self.NUM_OF_PREV_ITEMS = self.input_shape[0]

        self.epochs = 10
        self.batch_size = 200
        self.verbose = 2
        self.model = Sequential()
        self.model.add(LSTM(units=100, return_sequences=True, input_shape=shape))
        self.model.add(Dropout(0.5))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.3))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(units=1))

        self.input_scaler = MinMaxScaler(feature_range=(0, 1))
        self.output_scaler = MinMaxScaler(feature_range=(0, 1))

    def train(self, train_data, label_data):
        train_data = np.reshape(train_data, (-1, self.input_shape[1]))
        label_data = np.reshape(label_data, (-1, 1))

        # min-max normalization (inverse to (0, 1) range)
        data_transformed = self.input_scaler.fit_transform(train_data)
        label_transformed = self.output_scaler.fit_transform(label_data)

        train_x, train_y = reconstruct_data(data_transformed, label_transformed, self.NUM_OF_PREV_ITEMS)

        self.model.compile(loss="mean_squared_error", optimizer="adam")
        self.model.fit(train_x, train_y, epochs=self.epochs, batch_size=self.batch_size, verbose=self.verbose)

    def save_model(self, path):
        self.model.save(path)

        with open(os.path.join(path, "input_scaler"), "wb") as save_file:
            pickle.dump(self.input_scaler, save_file)

        with open(os.path.join(path, "output_scaler"), "wb") as save_file:
            pickle.dump(self.output_scaler, save_file)

        print(f"Model 'sf' saved to - {path}")
