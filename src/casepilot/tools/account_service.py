from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    account_id: str
    merchant: str
    amount: Decimal
    status: str
    posted_at: str


class AccountReader(Protocol):
    def list_transactions(self, *, account_id: str, limit: int = 20) -> list[Transaction]:
        """Read transactions for an account already authorized by host code."""
        ...

