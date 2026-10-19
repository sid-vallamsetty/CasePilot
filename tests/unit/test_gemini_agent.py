import inspect
from decimal import Decimal
from types import SimpleNamespace

from casepilot.agent import GeminiCaseAgent
from casepilot.config import Settings
from casepilot.domain.models import CaseRequest, CaseResponse
from casepilot.security import PermissionGate
from casepilot.tools import InMemoryAccountReader, Transaction


class FakeModels:
    """Capture the Gemini request without making a network call."""

    def __init__(self) -> None:
        self.request: dict[str, object] | None = None

    def generate_content(self, **kwargs: object) -> SimpleNamespace:
        self.request = kwargs
        config = kwargs["config"]
        tool_result = config.tools[0]()
        source_id = tool_result["transactions"][0]["transaction_id"]
        parsed = CaseResponse.model_validate(
            {
                "case_id": "case-1",
                "summary": "One matching transaction was found.",
                "evidence": [
                    {
                        "claim": "The transaction is posted.",
                        "source_type": "account_tool",
                        "source_id": source_id,
                    }
                ],
                "inferences": [],
                "missing_information": [],
                "recommendations": [],
            }
        )
        return SimpleNamespace(parsed=parsed, text=parsed.model_dump_json())


def test_tool_is_bound_to_the_host_authorized_account() -> None:
    fake_models = FakeModels()
    fake_client = SimpleNamespace(models=fake_models)
    reader = InMemoryAccountReader(
        [
            Transaction("txn-1", "acct-1", "Visible", Decimal("10.00"), "posted", "now"),
            Transaction("txn-2", "acct-2", "Hidden", Decimal("20.00"), "posted", "now"),
        ]
    )
    agent = GeminiCaseAgent(
        settings=Settings("gemini", "test-model", "test-embedding", "test-key"),
        account_reader=reader,
        permission_gate=PermissionGate("actor-1", frozenset({"acct-1"})),
        client=fake_client,
    )

    result = agent.investigate(CaseRequest("case-1", "acct-1", "Show my transactions"))

    assert result.case_id == "case-1"
    assert result.evidence[0].source_id == "txn-1"
    assert fake_models.request is not None
    config = fake_models.request["config"]
    tool = config.tools[0]

    # The model can choose only `limit`; the host-selected account cannot be replaced.
    assert "account_id" not in inspect.signature(tool).parameters
    assert [item["transaction_id"] for item in tool()["transactions"]] == ["txn-1"]
    assert config.response_schema is CaseResponse
