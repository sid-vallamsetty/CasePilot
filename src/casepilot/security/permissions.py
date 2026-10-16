from dataclasses import dataclass

from casepilot.domain.models import Approval


class AuthorizationError(PermissionError):
    """Raised when host-enforced authorization rejects an operation."""


@dataclass(frozen=True)
class PermissionGate:
    actor_id: str
    allowed_account_ids: frozenset[str]

    def require_account_access(self, account_id: str) -> None:
        if account_id not in self.allowed_account_ids:
            raise AuthorizationError(f"Actor is not authorized for account {account_id!r}")

    def require_approval(self, *, case_id: str, action: str, approval: Approval | None) -> None:
        if approval is None:
            raise AuthorizationError("A human approval record is required")
        if approval.case_id != case_id or approval.action != action:
            raise AuthorizationError("Approval does not match the requested case and action")

