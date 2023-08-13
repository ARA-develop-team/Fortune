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
        if profitable and self.dollars_account.balance > 0:
            exchange_rate = reverse_exchange_rate(exchange_rate)
            self.dollars_account.transfer(self.bitcoin_account, exchange_rate=exchange_rate)

        if not profitable and self.bitcoin_account.balance > 0:
            self.bitcoin_account.transfer(self.dollars_account, exchange_rate=exchange_rate)

    def terminate(self):
        self.bitcoin_account.log_account_balance()
        self.dollars_account.log_account_balance()
