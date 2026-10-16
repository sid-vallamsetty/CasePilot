from casepilot.domain.models import CaseRequest


def main() -> int:
    example = CaseRequest(
        case_id="demo-001",
        account_id="acct-demo-001",
        customer_issue="I do not recognize a transaction on my account.",
    )
    print("CasePilot scaffold is ready.")
    print(f"Example case: {example.case_id} ({example.account_id})")
    return 0

