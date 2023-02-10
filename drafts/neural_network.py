import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

print("\nARA Drafts\n")
df = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2019-12-17')

data = df.filter(['Close'])
dataset = data.values
training_data_len = math.ceil(len(dataset) * .8)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_date = scaler.fit_transform(dataset)

training_data = scaled_date[0:training_data_len, :]
x_train = []
y_train = []

for i in range(60, len(training_data)):
    x_train.append(training_data[i-60:i, 0])
    y_train.append(training_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

print("[]")
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=1)

test_data = scaled_date[training_data_len - 60:, :]
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])


x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

rmse = np.sqrt(np.mean(predictions - y_test)**2)

train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

# network accuracy
# for point in valid[['Close', 'Predictions']]:
#     print(point)

# ------

# plt.figure(figsize=(16, 8))
# plt.grid(True)
# plt.title('Model')
# plt.plot(train['Close'])
# plt.plot(valid[['Close', 'Predictions']])
# plt.xlabel('Date', fontsize=18)
# plt.ylabel('Close Price USD ($)', fontsize=18)
# plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
# plt.show()
