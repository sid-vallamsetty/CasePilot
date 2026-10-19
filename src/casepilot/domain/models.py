"""Typed inputs, outputs, and approval records for CasePilot.

Dataclasses represent values created by our host application. Pydantic models represent
model-generated data that must be parsed and validated at the trust boundary.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class EvidenceSource(StrEnum):
    """The only source categories the model may claim as evidence."""

    ACCOUNT_TOOL = "account_tool"
    POLICY = "policy"


class EvidenceItem(BaseModel):
    """A factual claim and the exact source that is supposed to support it."""

    claim: str = Field(min_length=1, description="A factual claim supported by the source.")
    source_type: EvidenceSource
    source_id: str = Field(
        min_length=1,
        description="A transaction ID for account evidence or document ID for policy evidence.",
    )
    passage_id: str | None = Field(
        default=None,
        description="Required later for evidence drawn from a policy passage.",
    )


class InferenceItem(BaseModel):
    """A conclusion derived from evidence rather than directly stated by a source."""

    claim: str = Field(min_length=1)
    supported_by: list[str] = Field(
        default_factory=list,
        description="Source IDs from the evidence list that support this inference.",
    )


class RecommendationItem(BaseModel):
    """A proposed next step; it is never itself an approved action."""

    action: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    requires_human_approval: bool = True


class CaseResponse(BaseModel):
    """The complete structured result Gemini must return for an investigation."""

    case_id: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    inferences: list[InferenceItem] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    recommendations: list[RecommendationItem] = Field(default_factory=list)


@dataclass(frozen=True)
class CaseRequest:
    """A case created by trusted host code before invoking the model."""

    case_id: str
    account_id: str
    customer_issue: str


@dataclass(frozen=True)
class Approval:
    """A human decision recorded outside the model conversation."""

    case_id: str
    action: str
    approved_by: str
    approved_at: datetime = field(default_factory=lambda: datetime.now(UTC))

