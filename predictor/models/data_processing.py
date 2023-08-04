import numpy as np


def reconstruct_data(data, num_of_prev_items):
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

    n = num_of_prev_items
    x, y = [], []

    for i in range(len(data) - n):
        a = data[i:(i + n), 0]
        x.append(a)
        y.append(data[i + n, 0])

    return np.array(x), np.array(y)
