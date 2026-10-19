import pytest

from casepilot.domain.models import CaseResponse
from casepilot.domain.validation import CaseResponseValidationError, validate_case_response


def response_with(**changes: object) -> CaseResponse:
    """Create a valid baseline response and override fields needed by each test."""

    data: dict[str, object] = {
        "case_id": "case-1",
        "summary": "A transaction was found.",
        "evidence": [
            {
                "claim": "The transaction is posted.",
                "source_type": "account_tool",
                "source_id": "txn-1",
            }
        ],
        "inferences": [
            {"claim": "The issue may need review.", "supported_by": ["txn-1"]}
        ],
        "missing_information": [],
        "recommendations": [
            {
                "action": "Review the transaction",
                "rationale": "The customer does not recognize it.",
                "requires_human_approval": True,
            }
        ],
    }
    data.update(changes)
    return CaseResponse.model_validate(data)


def test_valid_response_passes_semantic_validation() -> None:
    validate_case_response(
        response_with(),
        expected_case_id="case-1",
        allowed_account_source_ids={"txn-1"},
    )


def test_unseen_evidence_source_is_rejected() -> None:
    with pytest.raises(CaseResponseValidationError, match="unseen source"):
        validate_case_response(
            response_with(),
            expected_case_id="case-1",
            allowed_account_source_ids={"a-different-transaction"},
        )


def test_recommendation_cannot_bypass_human_approval() -> None:
    response = response_with(
        recommendations=[
            {
                "action": "Issue refund",
                "rationale": "The customer requested it.",
                "requires_human_approval": False,
            }
        ]
    )

    with pytest.raises(CaseResponseValidationError, match="human approval"):
        validate_case_response(
            response,
            expected_case_id="case-1",
            allowed_account_source_ids={"txn-1"},
        )
