# CasePilot

CasePilot is a human-approved support agent for synthetic financial cases. It combines a
versioned policy corpus with narrowly scoped, read-only account tools and produces cited,
structured investigation results.

## Start locally

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
casepilot
casepilot --demo
```

Copy `.env.example` to `.env` and add your Gemini key before running the demo. A normal
`casepilot` invocation performs no API call; `casepilot --demo` consumes API quota.

## Project map

```text
src/casepilot/
  agent/       orchestration and prompt construction
  domain/      typed inputs, outputs, evidence, and approval records
  retrieval/   policy ingestion, search, and citation validation
  security/    authorization and approval enforcement in host code
  tools/       narrow synthetic account interfaces
data/
  policies/              versioned policy documents
  synthetic_accounts/    fictional account and transaction fixtures
evals/cases/              normal, ambiguous, adversarial, and out-of-scope cases
tests/
  unit/ and integration/
docs/                    threat model and architecture notes
```

## Trust boundary

```text
User request
    |
    v
Host authorization + case/account scope
    |                         retrieved text is untrusted
    +--> policy retriever -------------------------------+
    +--> allowlisted read-only account tools ------------+--> model
    +--> approval gate for consequential actions --------+    |
                                                               v
                                             schema and citation validation
```

The model never grants itself access. Host code filters documents, binds account identifiers,
validates tool arguments, and blocks consequential actions unless an explicit approval record
is valid.

## Structured result boundary

Gemini is given `CaseResponse` as a JSON response schema. Pydantic first validates the shape and
types. A separate host validator then checks facts the schema cannot know: the case ID must match,
account evidence must cite a transaction actually exposed by the tool, inference references must
exist, and every recommendation must remain marked as requiring human approval.

