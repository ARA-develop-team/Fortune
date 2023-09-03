import os
from pandas import read_csv
from sf1.snowfall_training import SnowfallTestTrain

def train(model, input_data, output_data, save_file):
    model.train(input_data, output_data)
    model.save_model(os.path.join(model.PATH, save_file))

if __name__ == '__main__':
    data = read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset/tmp.csv'))
    data = data.astype('float32')
    data = data[['Open', 'High', 'Low', 'Close', 'Volume', 
                 'Quote asset volume', 'Number of trades', 
                 'Taker buy base asset volume', 'Taker buy quote asset volume', 
                 'Ignore']]

    model = SnowfallTestTrain((50, 10))
    train(model, data, data['Close'], 'model_15m_50:10_all-c')
