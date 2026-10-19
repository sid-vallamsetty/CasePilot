"""Semantic checks applied after Pydantic has validated the JSON structure.

Pydantic can prove that `source_id` is a string. It cannot prove that the source was
actually shown to the model. These checks compare model claims with host-observed data.
"""

from casepilot.domain.models import CaseResponse, EvidenceSource


class CaseResponseValidationError(ValueError):
    """Raised when a well-formed response violates a CasePilot trust rule."""


def validate_case_response(
    response: CaseResponse,
    *,
    expected_case_id: str,
    allowed_account_source_ids: set[str],
    allowed_policy_passage_ids: set[str] | None = None,
) -> None:
    """Reject unsupported sources, case swaps, and unapproved-looking recommendations."""

    if response.case_id != expected_case_id:
        raise CaseResponseValidationError("Response case_id does not match the requested case")

    allowed_policy_passage_ids = allowed_policy_passage_ids or set()
    evidence_source_ids = {item.source_id for item in response.evidence}

    for item in response.evidence:
        if item.source_type is EvidenceSource.ACCOUNT_TOOL:
            if item.source_id not in allowed_account_source_ids:
                raise CaseResponseValidationError(
                    f"Account evidence cites an unseen source: {item.source_id!r}"
                )
        elif item.source_type is EvidenceSource.POLICY and (
            not item.passage_id or item.passage_id not in allowed_policy_passage_ids
        ):
            raise CaseResponseValidationError(
                f"Policy evidence cites an unseen passage: {item.passage_id!r}"
            )

    for inference in response.inferences:
        unknown_sources = set(inference.supported_by) - evidence_source_ids
        if unknown_sources:
            raise CaseResponseValidationError(
                f"Inference refers to evidence not present in the response: {unknown_sources}"
            )

    for recommendation in response.recommendations:
        if not recommendation.requires_human_approval:
            raise CaseResponseValidationError(
                "Every recommendation must remain behind human approval"
            )
