from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from ..data_processing import reconstruct_data

class ModelTesting:
    def __init__(self, *args):
        self.model_handlers = args

    def two_line_test(self, data_set, train_coefficient=0):
        testing_data = data_set[int(len(data_set) * train_coefficient):] 
        testing_data = np.reshape(testing_data, (-1, 1))

        lines = []
        
        train_label_plot = data_set
        line1, = plt.plot(train_label_plot, label='real data')
        lines.append(line1)

        # make prediction
        for model in self.model_handlers:
            test_x, test_labels = reconstruct_data(testing_data, model.NUM_OF_PREV_ITEMS)
            test_predict = model.make_prediction(test_x)
            test_score = mean_squared_error(test_labels, test_predict[:, 0])
            print(f'[{model.__class__.__name__}|{model.model_name}] Score on test set: {test_score} MSE')

            number_of_unlabaled_data = int(len(data_set) * train_coefficient) + 1 + model.NUM_OF_PREV_ITEMS
            predict_plot = np.array([[np.nan]] * number_of_unlabaled_data).astype('float32')
            predict_plot = np.concatenate((predict_plot.astype('float32'), 
                                                test_predict.astype('float32')))
            
            predicted_line, = plt.plot(predict_plot, label=f'{model.model_name}')
            lines.append(predicted_line)

        plt.legend(handles=lines)
        plt.show() # TODO show date on axis

