import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers import Dropout



class SnowfallTestTrain():
    def __init__(self, num_of_previous_item):
        self.NUM_OF_PREV_ITEMS = num_of_previous_item

        self.model = Sequential()
        self.model.add(LSTM(units=100, return_sequences=True, input_shape=(1, num_of_previous_item)))
        self.model.add(Dropout(0.5))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.3))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(units=1))

    def train_test(self, data, train_cof=0.7, e=10, b=10, v=2):

        scaler = MinMaxScaler(feature_range=(0, 1))
        data = scaler.fit_transform(data)

        train, test = self.train_test_split(data, train_cof)
        self.train(train, e, b, v)

        self.show_test_predict(test)

    def train(self, data, e=10, b=10, v=2):

        # min-max normalixation (inverse to (0, 1) range)
        scaler = MinMaxScaler(feature_range=(0, 1))
        data = scaler.fit_transform(data)

        train_x, train_y = self._reconstruct_data(data)
        train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))

        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(train_x, train_y, epochs=e, batch_size=b, verbose=v)

    def save_model(self, destination):
        self.model.save(destination)

    def show_test_predict(self, data_set):
        """Used to test how this model is perform with data. 
        This function is showing predicted value and actual on graph 
        using matplotlib"""

        # min-max normalixation (inverse to (0, 1) range)
        scaler = MinMaxScaler(feature_range=(0, 1))
        data = scaler.fit_transform(data_set)

        # reshape data 
        test_x, test_y = self._reconstruct_data(data)
        test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1])) 

        # make prediction
        test_predict = self.model.predict(test_x)

        # min-max normalixation (inverse from (0, 1) range to actual value)
        test_predict = scaler.inverse_transform(test_predict)
        test_labels = scaler.inverse_transform([test_y])

        test_score = mean_squared_error(test_labels[0], test_predict[:, 0])
        print('Score on test set: %.2f MSE' % test_score)

        test_predict_plot = np.array([[np.nan]] * self.NUM_OF_PREV_ITEMS).astype('float32')
        test_predict_plot = np.concatenate((test_predict_plot.astype('float32'), test_predict.astype('float32')))
        

        plt.plot(scaler.inverse_transform(data))
        plt.plot(test_predict_plot, color="green")
        plt.show()

    def train_test_split(self, data, train_cof):
        train, test = data[0:int(len(data) * train_cof), :], data[int(len(data) * train_cof):len(data), :]

        return train, test

    def _reconstruct_data(self, data):
        #TODO remove from class
        """Reshape the data to input data and label(output).

        For example - data_set=[[1], [2], [3], [4], [5], [6], [7], [8]], n=3
        The result - [1, 2, 3] -> 4; [2, 3, 4] -> [5] ...
        The result data will be return in form:
        (array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7]]), 
        array([4, 5, 6, 7, 8]))

        :param data_set: numpy array
        :param n: number of previous number to predict next
        :return: input array - x; label(output) array - y
        """

        n = self.NUM_OF_PREV_ITEMS
        x, y = [], []

        for i in range(len(data) - n):
            a = data[i:(i + n), 0]
            x.append(a)
            y.append(data[i + n, 0])

        return np.array(x), np.array(y)
    
if __name__ == '__main__':
    model = SnowfallTestTrain(5)

    # scaler = MinMaxScaler(feature_range=(0, 1))
    # data = scaler.fit_transform([[1], [2], [3], [4], [5], [6], [7], [8]])

    # print(model._reconstruct_data(np.array([[1], [2], [3], [4], [5], [6], [7], [8]])))

    data = read_csv('BTC-USD.csv', usecols=[3])
    data = data.astype('float32')

    model.train_test(data)
