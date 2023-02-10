import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, mean_absolute_error

df = yf.download('ETH-USD')
# print(df)

# Train test split

to_row = int(len(df) * 0.9)

training_data = list(df[0:to_row]['Adj Close'])
testing_data = list(df[to_row:]['Adj Close'])

model_predictions = []
n_test_observation = len(testing_data)

# print(training_data)
for i in range(n_test_observation):
    model = sm.tsa.arima.ARIMA(training_data, order=(1, 1, 0))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    model_predictions.append(yhat)
    actual_test_value = testing_data[i]
    training_data.append(actual_test_value)

    # # Output
    output = "[ {:<20} | {:<20} |= {:<20}".format(yhat, actual_test_value, yhat - actual_test_value)
    # output = "P [ {:<20} | {:<20} ] R (vector)".format(yhat - training_data[-2], actual_test_value - training_data[-2])
    print(output)

#
# print("-------------------------- DATA --------------------------")
# for i in range(n_test_observation - 1):
#     output = "P [ {:<20} | {:<20} ] R (prices)".format(model_predictions[i + 1], testing_data[i])
#     print(output)

plt.figure(figsize=(15, 9))
plt.grid(True)

date_range = df[to_row:].index

plt.plot(date_range, model_predictions, color='blue', marker='o', linestyle='dashed',
         label="BTC Predicted Price")
plt.plot(date_range, testing_data, color='red', label='BTC Actual Price')

plt.title('BTC Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

