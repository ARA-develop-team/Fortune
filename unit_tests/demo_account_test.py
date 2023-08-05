import unittest


import logging
from trader.demo_account import DemoAccount

# Disable logging during testing
logging.disable(logging.CRITICAL)


class TestDemoAccount(unittest.TestCase):
    def setUp(self):
        self.currency = "USD"
        self.initial_balance = 1000
        self.account = DemoAccount(self.currency, balance=self.initial_balance)

    def test_deposit_valid_amount(self):
        deposit_amount = 500
        expected_balance = self.initial_balance + deposit_amount
        self.account.deposit(deposit_amount)
        self.assertEqual(self.account.balance, expected_balance)

    def test_deposit_invalid_amount(self):
        deposit_amount = -200
        self.account.deposit(deposit_amount)
        self.assertEqual(self.account.balance, self.initial_balance)

    def test_withdraw_valid_amount(self):
        withdraw_amount = 300
        expected_balance = self.initial_balance - withdraw_amount
        self.account.withdraw(withdraw_amount)
        self.assertEqual(self.account.balance, expected_balance)

    def test_withdraw_invalid_amount(self):
        withdraw_amount = -200
        self.account.withdraw(withdraw_amount)
        self.assertEqual(self.account.balance, self.initial_balance)

    def test_withdraw_insufficient_funds(self):
        withdraw_amount = self.initial_balance + 100
        self.account.withdraw(withdraw_amount)
        self.assertEqual(self.account.balance, self.initial_balance)

    def test_transfer_valid_amount(self):
        to_account = DemoAccount("EUR", balance=500)
        exchange_rate = 0.85
        transfer_amount = 200
        expected_from_balance = self.initial_balance - transfer_amount
        expected_to_balance = to_account.balance + (transfer_amount * exchange_rate)

        self.account.transfer(to_account, transfer_amount, exchange_rate)
        self.assertEqual(self.account.balance, expected_from_balance)
        self.assertEqual(to_account.balance, expected_to_balance)

    def test_transfer_invalid_amount(self):
        to_account = DemoAccount("EUR", balance=500)
        exchange_rate = 0.85
        transfer_amount = -200
        self.account.transfer(to_account, transfer_amount, exchange_rate)
        self.assertEqual(self.account.balance, self.initial_balance)
        self.assertEqual(to_account.balance, 500)

    def test_transfer_insufficient_funds(self):
        to_account = DemoAccount("EUR", balance=500)
        exchange_rate = 0.85
        transfer_amount = self.initial_balance + 100
        self.account.transfer(to_account, transfer_amount, exchange_rate)
        self.assertEqual(self.account.balance, self.initial_balance)
        self.assertEqual(to_account.balance, 500)


if __name__ == '__main__':
    unittest.main()
