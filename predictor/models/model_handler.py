import os

from abc import ABC, abstractmethod


class ModelHandler(ABC):
    PATH = os.path.dirname(__file__)

    def __init__(self):
        super().__init__()

    @abstractmethod
    def predict_next(self, data_set: list) -> int:
        pass

    @abstractmethod
    def make_prediction(self, data_set: list) -> list:
        pass


class ModelTrainer(ABC):
    PATH = os.path.dirname(__file__)

    def __init__(self, input_shape: tuple):
        super().__init__()
        self.input_shape = input_shape

    @abstractmethod
    def train(self, data: list) -> None:
        pass
