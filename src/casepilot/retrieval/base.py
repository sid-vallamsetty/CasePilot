from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PolicyPassage:
    document_id: str
    passage_id: str
    text: str
    version: str
    allowed_roles: frozenset[str]


class PolicyRetriever(Protocol):
    def search(self, query: str, *, role: str, limit: int = 5) -> list[PolicyPassage]:
        """Return only passages authorized for the caller's role."""
        ...

