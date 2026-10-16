import pytest

from casepilot.domain.models import Approval
from casepilot.security.permissions import AuthorizationError, PermissionGate


def test_account_scope_is_enforced() -> None:
    gate = PermissionGate("agent-1", frozenset({"acct-1"}))

    gate.require_account_access("acct-1")

    with pytest.raises(AuthorizationError):
        gate.require_account_access("acct-2")


def test_approval_must_match_case_and_action() -> None:
    gate = PermissionGate("agent-1", frozenset({"acct-1"}))
    approval = Approval("case-1", "open_dispute", "supervisor-1")

    gate.require_approval(case_id="case-1", action="open_dispute", approval=approval)

    with pytest.raises(AuthorizationError):
        gate.require_approval(case_id="case-1", action="issue_refund", approval=approval)

