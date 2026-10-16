# Threat model

## Protected assets

- Synthetic account data and account boundaries
- Policy confidentiality and version integrity
- Approval state for consequential actions
- Accuracy and provenance of claims shown to support staff

## Initial threats

- Indirect prompt injection in policy text or tool output
- Model-generated access to an unauthorized account
- Fabricated or mismatched citations
- A proposed action being represented as approved
- Conflicting or obsolete policy versions
- Over-broad tools exposing unnecessary account fields

## Host-enforced controls

- Filter retrieval by authorization metadata before model context is assembled.
- Bind account IDs to the authenticated case rather than accepting arbitrary model values.
- Expose an allowlist of narrow, typed, read-only tools.
- Validate model output and citations against retrieved passages.
- Require a matching human approval record before any simulated consequential action.

