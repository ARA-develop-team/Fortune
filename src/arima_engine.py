import statsmodels.api as sm


def predict_arima(data):
    model = sm.tsa.arima.ARIMA(data, order=(4, 1, 0))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    return yhat

