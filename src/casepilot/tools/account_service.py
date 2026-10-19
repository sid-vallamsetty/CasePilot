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


class InMemoryAccountReader:
    """A deterministic synthetic account service suitable for demos and tests."""

    def __init__(self, transactions: list[Transaction]) -> None:
        # Copy the input so callers cannot mutate our backing store after initialization.
        self._transactions = tuple(transactions)

    def list_transactions(self, *, account_id: str, limit: int = 20) -> list[Transaction]:
        # Enforce a modest result bound even if the model asks for an extreme value.
        safe_limit = max(1, min(limit, 100))
        matching = [item for item in self._transactions if item.account_id == account_id]
        return matching[:safe_limit]

