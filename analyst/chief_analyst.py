import logging


class Analyst:
    def __init__(self, threshold=0.75):
        self.threshold = threshold

    def analyse_threshold(self, vector):
        return vector >= self.threshold

    def decide_trading(self, vector):
        """ Decide if purchase is profitable.
            :arg vector: probability of cryptocurrency price growth.
            :return: buy/keep crypto - True, sell - False.
        """
        decision = self.analyse_threshold(vector)
        logging.info(f"Vector: {vector}, Decision: {decision}")
        return decision


