""" Analyst Module """

import logging


def calculate_vector(previous_price, next_price):
    return (next_price - previous_price) / previous_price


class Analyst:
    def __init__(self, threshold=0.0):
        self.threshold = threshold

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info("Analyst was configured successfully")

    def analyse_threshold(self, vector):
        return vector >= self.threshold

    def make_trading_decision(self, vector):
        """Decide if purchasing cryptocurrency is profitable based on the probability of price growth.

        :arg vector: probability of cryptocurrency price growth.
        :return: True if it is profitable to buy/keep crypto, False otherwise (to sell).
        """
        decision = self.analyse_threshold(vector)
        self.logger.info(f"Vector: {vector}, Decision: {decision}")
        return decision
