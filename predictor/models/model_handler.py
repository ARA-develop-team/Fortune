import os

from abc import ABC, abstractmethod


class ModelHandler(ABC):
    PATH_TO_CONF = os.path.join(os.path.dirname(__file__), "fortune-nn-configs")

    def __init__(self):
        super().__init__()

    @abstractmethod
    def predict_next(self, data_set: list) -> int:
        pass

    @abstractmethod
    def make_prediction(self, data_set: list) -> list:
        pass


class ModelTrainer(ABC):
    PATH_TO_CONF = os.path.join(os.path.dirname(__file__), "fortune-nn-configs")

    def __init__(self, input_shape: tuple):
        super().__init__()
        self.input_shape = input_shape

    @abstractmethod
    def train(self, train_data, label_data) -> None:
        pass
