import logging

import wallet_exceptions


class Wallet:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
        logging.info("Demo-Wallet was configured successfully")

    def convert_to(self, to_currency):
        try:
            exchange_rate = get_exchange_rate(self.currency, to_currency)

        except wallet_exceptions.ExchangeRateError as error:
            print(error)
            return self.amount, self.currency    # Not to convert money.

        else:
            converted_amount = exchange_rate * self.amount
            converted_currency = to_currency

        return converted_amount, converted_currency

    def buy_currency(self, currency):
        self.amount, self.currency = self.convert_to(currency)


def get_exchange_rate(from_currency, to_currency):
    # TODO
    raise wallet_exceptions.ExchangeRateError


if __name__ == '__main__':
    my_wallet = Wallet(100.0, 'USD')
    my_wallet.buy_currency('EUR')
    print(f"In your wallet {my_wallet.amount} {my_wallet.currency}")
