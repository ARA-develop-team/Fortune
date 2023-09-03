""" Trader Module """

import logging

from src.custom_types.statistics import Statistics, AccountStats
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
        :return: A Statistics named tuple containing the account statistics and the total value in dollars.
        """

        total_in_usd = None
        if exchange_rate is not None:
            total_in_usd = AccountStats(currency=self.dollars_account.currency,
                                        balance=self.dollars_account.balance + (
                                                self.bitcoin_account.balance * exchange_rate))

        stats = Statistics(
            accounts=[
                AccountStats(currency=self.dollars_account.currency,
                             balance=self.dollars_account.balance),
                AccountStats(currency=self.bitcoin_account.currency,
                             balance=self.bitcoin_account.balance)
            ],
            total=total_in_usd
        )

        return stats

    def terminate(self):
        self.bitcoin_account.log_account_balance()
        self.dollars_account.log_account_balance()
