from predictor import predictor_service
from pandas import read_csv
from src.parse_arguments import parse_arguments



if __name__ == "__main__":
    args_dict = parse_arguments()

    predictor = predictor_service.Predictor()

    data = read_csv('predictor/dataset/tmp.csv')
    data = data.astype('float32')

    if args_dict["train"] or not args_dict["test"]:
        predictor.train_main(data)
    if args_dict["test"] or not args_dict["train"]:
        predictor.test(data)
