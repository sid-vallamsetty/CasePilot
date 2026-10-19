import argparse
from decimal import Decimal

from casepilot.agent import GeminiCaseAgent
from casepilot.config import load_settings
from casepilot.domain.models import CaseRequest
from casepilot.security import PermissionGate
from casepilot.tools import InMemoryAccountReader, Transaction


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the CasePilot synthetic support demo")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="send one synthetic case to Gemini (uses API quota)",
    )
    args = parser.parse_args()

    if not args.demo:
        print("CasePilot is installed. Run `casepilot --demo` to call Gemini.")
        return 0

    case = CaseRequest(
        case_id="demo-001",
        account_id="acct-demo-001",
        customer_issue="I do not recognize the $84.19 Northwind Market transaction.",
    )

    # For now the synthetic service is in memory. It will later be loaded from the
    # fixtures directory without changing the agent-facing AccountReader interface.
    account_reader = InMemoryAccountReader(
        [
            Transaction(
                transaction_id="txn-demo-001",
                account_id=case.account_id,
                merchant="Northwind Market",
                amount=Decimal("84.19"),
                status="posted",
                posted_at="2026-10-15T14:32:00Z",
            )
        ]
    )

    # In a real application these account IDs would come from the authenticated session,
    # not from the model or user prompt.
    gate = PermissionGate(
        actor_id="support-representative-demo",
        allowed_account_ids=frozenset({case.account_id}),
    )
    agent = GeminiCaseAgent(
        settings=load_settings(),
        account_reader=account_reader,
        permission_gate=gate,
    )

    result = agent.investigate(case)
    print(result.model_dump_json(indent=2))
    return 0

