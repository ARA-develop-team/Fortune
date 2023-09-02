import numpy as np

def reconstruct_data(input_data: list, output_data: list, num_of_prev_items: int) -> (np.array, np.array):
    """ len(input_data) = len(output_data)"""

    """Reshape the data to input data and label(output).

    For example - data_set=[[1], [2], [3], [4], [5], [6], [7], [8]], n=3
    The result - [1, 2, 3] -> 4; [2, 3, 4] -> [5] ...
    The result data will be return in form:
    (array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7]]), 
    array([4, 5, 6, 7, 8]))

    :param data_set: numpy array
    :param n: number of previous number to predict next
    :return: input array - x; label(output) array - y
    """
    # TODO change doc
    n = num_of_prev_items
    x, y = [], []

    for i in range(len(input_data) - n):
        a = input_data[i:(i + n)]
        x.append(a)
        y.append(output_data[i + n])

    return np.array(x), np.array(y)

def train_test_split(data, train_cof):
    train, test = data[0:int(len(data) * train_cof), :], data[int(len(data) * train_cof):len(data), :]

    return train, test