import os
from pandas import read_csv
from sf1.snowfall_training import SnowfallTestTrain

def train(model, save_file):
    model.train_test()
    model.save_model(os.path.join(model.PATH, save_file))

if __name__ == '__main__':
    data = read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset/tmp.csv'))
    data = data.astype('float32')
    model = SnowfallTestTrain(data, (1, 50))
    train(model, 'model_15m')
