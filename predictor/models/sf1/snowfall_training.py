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

from .config_parser import get_network_data
from data_processing import reconstruct_data

class SnowfallTestTrain():
    def __init__(self, data, shape):
        self.PATH = os.path.dirname(__file__)

        config_data = get_network_data(os.path.join(self.PATH, "config.json"))

        self.NUM_OF_PREV_ITEMS = shape[1]

        self.epochs = config_data["epochs"]
        self.batch_size = config_data["batch-size"]
        self.verbose = config_data["verbose"]
        self.model = Sequential()
        self.model.add(LSTM(units=100, return_sequences=True, input_shape=shape))
        self.model.add(Dropout(0.5))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.3))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(units=1))

        self.scaler = MinMaxScaler(feature_range=(0, 1))

        self.data = np.reshape(data, (-1, 1))

    def train_test(self, train_cof=0.7):
        train_data, test_data = self.train_test_split(self.data, train_cof)
        self.train(train_data)

        self.show_test_predict(test_data)

    def train(self, train_data):
        # min-max normalixation (inverse to (0, 1) range)
        data_transformed = self.scaler.fit_transform(train_data)

        train_x, train_y = reconstruct_data(data_transformed, self.NUM_OF_PREV_ITEMS)
        train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))

        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(train_x, train_y, epochs=self.epochs, batch_size=self.batch_size , verbose=self.verbose)

    def save_model(self, path):
        print(f"Model 'sf' saved to - {path}")
        self.model.save(path)

    def show_test_predict(self, data_set, show_all_data=True):
        """Used to test how this model is perform with data. 
        This function is showing predicted value and actual on graph 
        using matplotlib"""

        # min-max normalixation (inverse to (0, 1) range)
        data_transformed = self.scaler.fit_transform(data_set)

        # reshape data 
        test_x, test_y = reconstruct_data(data_transformed, self.NUM_OF_PREV_ITEMS)
        test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1])) 

        # make prediction
        test_predict = self.model.predict(test_x)
        # min-max normalixation (inverse from (0, 1) range to actual value)
        test_predict = self.scaler.inverse_transform(test_predict)
        test_labels = self.scaler.inverse_transform([test_y])
        test_score = mean_squared_error(test_labels[0], test_predict[:, 0])
        print('Score on test set: %.2f MSE' % test_score)

        if show_all_data:
            train_label_plot = self.data
            predict_plot = np.array([[np.nan]] * (len(self.data) - len(test_predict) + 1)).astype('float32')
            
        else:
            train_label_plot = test_labels[0]
            predict_plot = np.array([[np.nan]] * self.NUM_OF_PREV_ITEMS).astype('float32')

        predict_plot = np.concatenate((predict_plot.astype('float32'), 
                                            test_predict.astype('float32')))
        
        plt.plot(train_label_plot)
        plt.plot(predict_plot, color="green")
        plt.show()

    def train_test_split(self, data, train_cof):
        train, test = data[0:int(len(data) * train_cof), :], data[int(len(data) * train_cof):len(data), :]

        return train, test
    
if __name__ == '__main__':
    data = read_csv('tmp.csv')
    data = data.astype('float32')
    model = SnowfallTestTrain(data, (12, 50))

    model.train_test()
    model.save_model('model_15m')
