import numpy as np


def reconstruct_data(input_data, output_data, n: int) -> (np.array, np.array):
    """
    Match each element in output_data (except the first n element)
    to list of previous n elements of input_data.

    The data will be reshaped so network could see what output should be to the given input data.
    [1, 2, 3] -> 4; [2, 3, 4] -> [5]

    the length of input_data should be = length of output_data.
    Input and output data could be the same or different.
    Input data could contain multiple or single features.


    For example - input_data = output_data = [[1], [2], [3], [4], [5], [6], [7], [8]], n=3
    The result - [1, 2, 3] -> 4; [2, 3, 4] -> [5] ...
    The result data will be returned in form:
    (array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7]]),
    array([4, 5, 6, 7, 8]))

    :param input_data: array
    :param output_data: array
    :param n: number of previous items to predict next
    :return: reshaped input array and output array
    """
    # TODO change doc
    x, y = [], []

    for i in range(len(input_data) - n):
        a = input_data[i : (i + n)]
        x.append(a)
        y.append(output_data[i + n])

    return np.array(x), np.array(y)


def train_test_split(data, train_cof):
    train, test = data[0 : int(len(data) * train_cof), :], data[int(len(data) * train_cof) : len(data), :]

    return train, test
