from decimal import Decimal

from casepilot.tools import InMemoryAccountReader, Transaction


def test_reader_returns_only_the_requested_account() -> None:
    reader = InMemoryAccountReader(
        [
            Transaction("txn-1", "acct-1", "Merchant A", Decimal("10.00"), "posted", "now"),
            Transaction("txn-2", "acct-2", "Merchant B", Decimal("20.00"), "posted", "now"),
        ]
    )

    result = reader.list_transactions(account_id="acct-1")

    assert [item.transaction_id for item in result] == ["txn-1"]
