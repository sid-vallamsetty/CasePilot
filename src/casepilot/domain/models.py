from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class FindingKind(StrEnum):
    EVIDENCE = "evidence"
    INFERENCE = "inference"
    MISSING_INFORMATION = "missing_information"
    RECOMMENDATION = "recommendation"


@dataclass(frozen=True)
class Citation:
    source_id: str
    passage_id: str
    quote: str
    policy_version: str | None = None


@dataclass(frozen=True)
class Finding:
    kind: FindingKind
    claim: str
    citations: tuple[Citation, ...] = ()


@dataclass(frozen=True)
class CaseRequest:
    case_id: str
    account_id: str
    customer_issue: str


@dataclass
class CaseResponse:
    case_id: str
    summary: str
    findings: list[Finding] = field(default_factory=list)
    proposed_action: str | None = None
    requires_approval: bool = False


@dataclass(frozen=True)
class Approval:
    case_id: str
    action: str
    approved_by: str
    approved_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

