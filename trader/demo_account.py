import logging


class DemoAccount:
    def __init__(self, currency, balance=0):
        self.currency = currency
        self.balance = balance
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(f"Demo {self.currency} Account was configured successfully")
        self.log_account_balance()

    def _is_valid_amount(self, amount):
        if amount <= 0:
            self.logger.warning(f"{self.currency} amount must be greater than zero.")
            return False
        return True

    def _has_sufficient_funds(self, amount):
        if self.balance < amount:
            self.logger.warning("Insufficient funds for cash-out.")
            return False
        return True

    def deposit(self, amount):
        """Deposit the specified amount into the account.
        :param amount: The amount to be deposited.
        """
        if not self._is_valid_amount(amount):
            return

        self.balance += amount
        self.logger.info(f"Deposited {amount} {self.currency}. New balance: {self.balance} {self.currency}.")

    def withdraw(self, amount):
        """Withdraw the specified amount from the account.

        :param amount: The amount to be withdrawn.
        :return: True if the withdrawal was successful, False otherwise.
        """
        if not self._is_valid_amount(amount) or not self._has_sufficient_funds(amount):
            return False

        self.balance -= amount
        self.logger.info(f"Withdrew {amount} {self.currency}. New balance: {self.balance} {self.currency}.")
        return True

    def transfer(self, to_account, amount=None, exchange_rate=1):
        """Transfer funds to another account.

        :param to_account: The target account to transfer funds to.
        :type to_account: DemoAccount
        :param amount: The amount to be transferred. If not provided (or set to None),
            the entire available balance in the account will be transferred.
        :param exchange_rate: The exchange rate for converting the amount
            to the target account's currency. Default is 1.
        """
        if amount is None:
            amount = self.balance

        self.logger.info(f"Transferring {self.currency} -> {to_account.currency}.")
        if not self.withdraw(amount):
            return

        converted_amount = amount * exchange_rate
        to_account.deposit(converted_amount)
        self.logger.info("-" * 74)

    def log_account_balance(self):
        self.logger.info(f"Demo {self.currency} account balance: {self.balance}")


def reverse_exchange_rate(rate):
    if rate == 0:
        raise ValueError("Exchange rate cannot be zero.")
    return 1 / rate
