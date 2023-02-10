"""Exception for demo wallet and simulation module"""


class ExchangeRateError(Exception):
    def __str__(self):
        return f"[WALLET] Can not update exchange rate."
