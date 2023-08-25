import os
from pandas import read_csv
from sf1.snowfall_training import SnowfallTestTrain


def train(model, data, filename):
    model.train(data)
    model.save_model(os.path.join(model.PATH_TO_CONF, filename))


if __name__ == '__main__':
    data = read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset/tmp.csv'))
    data = data.astype('float32')
    model = SnowfallTestTrain((1, 50))
    train(model, data, 'model_15m')
