""" Trader Module """

import logging

from .demo_account import DemoAccount, reverse_exchange_rate


class Trader:
    def __init__(self):
        self.bitcoin_account = DemoAccount("BTC", balance=0)
        self.dollars_account = DemoAccount("USD", balance=100)

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info("Trader was configured successfully")

    def demo_trade(self, profitable, exchange_rate):
        """ Performs a demo trade based on the profitability and exchange rate.

        :param profitable: A boolean indicating whether the trade is profitable (True) or not (False).
        :param exchange_rate: The exchange rate to be used for the transfer of assets between accounts.
        """
        if profitable and self.dollars_account.balance > 0:
            exchange_rate = reverse_exchange_rate(exchange_rate)
            self.dollars_account.transfer(self.bitcoin_account, exchange_rate=exchange_rate)

        if not profitable and self.bitcoin_account.balance > 0:
            self.bitcoin_account.transfer(self.dollars_account, exchange_rate=exchange_rate)

    def generate_stats(self, exchange_rate=None):
        """ Generates statistics related to the account balances.

        :param exchange_rate: The exchange rate. If not provided, the total value in dollars will not be calculated.
        :return: A dictionary containing the statistics with the account currencies as keys
                 and their corresponding balances as values.
        """
        stats = {self.dollars_account.currency: self.dollars_account.balance,
                 self.bitcoin_account.currency: self.bitcoin_account.balance}

        if exchange_rate is not None:
            stats["Total"] = self.dollars_account.balance + (self.bitcoin_account.balance * exchange_rate)

        return stats

    def terminate(self):
        self.bitcoin_account.log_account_balance()
        self.dollars_account.log_account_balance()
