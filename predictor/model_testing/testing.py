from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from predictor.models.data_processing import reconstruct_data


class ModelTesting:
    def __init__(self, data_set, train_coefficient, output):
        self.data_set = data_set
        self.testing_data = data_set[int(len(data_set) * train_coefficient) :]

        self.train_coefficient = train_coefficient
        self.output_column = output
        self.lines = []

        self._add_line(self.data_set[self.output_column], "real_data")

    def _add_line(self, data_set, name: str):
        (line1,) = plt.plot(data_set, label=name)
        self.lines.append(line1)

    def add_model(self, model, input_layers: list):
        test_x, test_labels = reconstruct_data(
            np.array(self.testing_data[input_layers]),
            np.array(self.testing_data[self.output_column]),
            model.NUM_OF_PREV_ITEMS,
        )

        test_predict = model.make_prediction(test_x)

        test_score = mean_squared_error(test_labels, test_predict)
        print(f"[{model.__class__.__name__}|{model.model_name}] Score on test set: {test_score} MSE")

        number_of_unlabeled_data = int(len(self.data_set) * self.train_coefficient) + 1 + model.NUM_OF_PREV_ITEMS
        predict_plot = np.array([[np.nan]] * number_of_unlabeled_data).astype("float32")
        predict_plot = np.concatenate((predict_plot.astype("float32"), test_predict.astype("float32")))

        self._add_line(predict_plot, model.model_name)

    def show_graph(self):
        plt.legend(handles=self.lines)
        plt.show()  # TODO show date on axis
