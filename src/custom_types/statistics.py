""" Custom Statistics Type
Description: This module defines custom data types for storing statistical information related to accounts.

Custom Types:
- Statistics: A named tuple representing statistics data that includes an array of account statistics 
  and a total account statistics.
- AccountStats: A named tuple representing statistics for an individual account,
  including currency and balance.

Example Usage:

    Statistics {
        accounts [
            AccountStats1 {
                currency: USD
                balance: 1500.00
            }
            AccountStats2 {
                currency: EUR
                balance: 2000.00
            }
        ]

        total {
            AccountStats_total {
                currency: USD
                balance: 3650.00
            }
        }
    }

Note: If there arises a need to make these types mutable, consider utilizing `RecordClass` instead of `NamedTuple`.
"""

from typing import Optional, NamedTuple


class AccountStats(NamedTuple):
    currency: str
    balance: float


class Statistics(NamedTuple):
    accounts: list[AccountStats]
    total: Optional[AccountStats]
