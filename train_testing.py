import os
from pandas import read_csv

from src.custom_types import shorten_kline_metric
from predictor.model_testing.testing import ModelTesting
from predictor.models.sf1.snowfall_training import SnowfallTestTrain
from src.parse_arguments import parse_arguments
from predictor.models.sf1.snowfall_model import Snowfall

def test(data: list):
    output_column = ['close']

    test = ModelTesting(data, 0.7, output_column)
    test.add_model(Snowfall('model_15m_50:10_all-c'), shorten_kline_metric)
    test.add_model(Snowfall(), ['close'])

    test.show_graph()

def train_main(data):
    output_data = data[['close']]
    input_data = data[shorten_kline_metric]
    model = SnowfallTestTrain((50, 10))
    train(model, input_data, output_data, 'model_15m_50:10_all-c')

def train(model, input_data, output_data, save_file):
    model.train(input_data, output_data)
    model.save_model(os.path.join(model.PATH_TO_CONF, save_file))

if __name__ == "__main__":
    args_dict = parse_arguments()

    data = read_csv('predictor/dataset/btc_data.csv')
    data = data.astype('float32')

    if args_dict["train"] or not args_dict["test"]:
        train_main(data)
    if args_dict["test"] or not args_dict["train"]:
        test(data)
