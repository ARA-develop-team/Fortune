
class PredictorModel:
    def __init__(self):
        self.training_set = [0, 0]

    def get_training_set(self):
        return self.training_set

    def train_model(self, data):
        pass

    def predict(self, data):
        s = 0
        for elem in data:
            s += elem

        return s / len(data)
