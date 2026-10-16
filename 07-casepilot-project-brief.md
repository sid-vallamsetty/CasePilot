# CasePilot — Human-Approved Support Agent

## Brief

Build an agent for a fictional financial-support environment. It interprets a customer issue, retrieves policy text, calls narrowly scoped read-only account tools, cites evidence, and proposes a resolution. Consequential actions remain behind an explicit human-approval boundary.

This is a **5–6 hour sprint** in agent design, tool calling, retrieval, structured output, security, and evaluation. The value is controlled, measured behavior—not a chat interface alone.

## Scenario

A support representative needs help investigating fictional cases such as an unrecognized transaction, duplicate charge, or fee question. CasePilot may gather information and draft a next step, but cannot move money, modify an account, or represent a proposal as an approved decision.

## Required capabilities

- Accept a documented set of synthetic support scenarios.
- Retrieve from a small, versioned policy corpus and cite passages.
- Use structured, typed tools for synthetic account data.
- Distinguish evidence, inference, missing information, and recommendation.
- Require human approval before any simulated consequential action.
- Enforce permissions outside the language-model prompt.
- Treat retrieved documents and tool output as untrusted.
- Validate structured model results in host code.
- Evaluate at least 20 normal, ambiguous, adversarial, and out-of-scope cases.
- Report success, unsupported claims, citation quality, tool selection, latency, and cost.

## Threats and decisions you own

- Can a policy document tell the agent to ignore its rules?
- What prevents an unauthorized tool call?
- Which account fields can the model see?
- How is approval represented and enforced?
- What happens when policies disagree?
- How will you distinguish fluent from correct?
- Which evaluation results can be scored deterministically?

## Boundaries

Use synthetic identities, accounts, transactions, and policies. Do not provide real financial advice. Do not expose general SQL, shell, HTTP, or file-system tools. Simulated write tools are optional and must be host-blocked without approval.

## Time budget

| Area | Time |
|---|---:|
| Contract, corpus, and threat model | 45–60 min |
| Tools and controlled agent loop | 90–120 min |
| Retrieval and citations | 60–75 min |
| Evaluation and attacks | 75–90 min |
| Report and demo | 35–45 min |

## Definition of done

- Several investigations complete end-to-end with citations.
- Tool schemas and host code—not prompts alone—bound actions.
- At least three indirect prompt-injection attempts are safely handled.
- Missing evidence is surfaced rather than invented.
- The 20-case evaluation reruns and produces machine-readable results.
- Failures appear in the report.
- The README includes a trust-boundary diagram and approval explanation.

## Deliverables

1. Agent host and typed tool interfaces.
2. Synthetic account service and versioned policy corpus.
3. Retrieval/citation component.
4. Threat model and trust-boundary diagram.
5. Twenty or more evaluation cases and scoring harness.
6. Results and error taxonomy.
7. Demo showing a success and a blocked attack.
8. `AI_LOG.md`.

## AI collaboration

Use an LLM to create diverse test ideas, critique permissions, and cluster failures. Keep a human-written gold answer or required-facts rubric. Do not use the same model's unreviewed judgment as the sole proof of its correctness.

## Evidence to capture

Capture model/version, cases, task success, citation support, unauthorized-action rate, tool errors, latency, token usage or cost, and failure categories.

## Resources

- [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output)
- [Gemini embeddings](https://ai.google.dev/gemini-api/docs/embeddings)
- [Google Agent Development Kit](https://google.github.io/adk-docs/)
- [Google Cloud introduction to agents](https://cloud.google.com/discover/what-are-ai-agents)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [OWASP Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [Original RAG paper](https://arxiv.org/abs/2005.11401)

## Be ready to explain

- Which controls still work if the model ignores instructions?
- How do you know a citation supports a claim?
- Why is approval more than a sentence in the prompt?
- What were the most common evaluation failures?
