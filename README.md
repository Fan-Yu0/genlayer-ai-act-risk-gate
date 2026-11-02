# AI Act Risk Gate

A reusable GenLayer Intelligent Contract for evidence-backed EU AI Act risk
screening. It turns two official documentation URLs into a public,
reproducible risk classification that other contracts can consume.

Repository: <https://github.com/Fan-Yu0/genlayer-ai-act-risk-gate>

## Live deployment

Deployment evidence will be added after the Studio deployment and live call.

## Problem

AI marketplaces, procurement contracts, agent registries, and DAOs increasingly
need to know whether a system is prohibited, high-risk, limited-risk, or
minimal-risk under Regulation (EU) 2024/1689. Today that answer usually comes
from a vendor self-declaration or a private compliance dashboard. Neither is
public, reproducible, or consumable by an on-chain workflow.

This contract creates a public screening record from two pieces of live
evidence:

1. the provider's official system documentation or model card;
2. the deployment, intended-purpose, or terms documentation.

The contract does not ask an LLM to invent a legal conclusion. The model
extracts only a constrained evidence record. Fixed contract code then applies
the tier policy and returns a deterministic decision plus the obligations that
the selected tier triggers.

## How it works

1. A publisher registers a system ID, an official system documentation URL, a
   deployment or intended-purpose URL, and whether it acts as provider or
   deployer.
2. Anyone calls `assess(system_id)`.
3. The leader fetches both pages as text and asks the LLM for one JSON object:
   `risk_tier`, `prohibited_practice`, `annex_iii_domain`,
   `transparency_required`, and `source_consistency`.
4. Validators independently fetch the same two pages and re-run the same
   extraction. They compare the decision-bearing fields, not the leader's JSON
   shape.
5. Deterministic contract code maps the agreed evidence to a decision and a
   fixed obligation list.

## Decision policy

| Condition | Decision |
| --- | --- |
| Sources conflict or cannot support a classification | `REVIEW_REQUIRED` |
| Risk tier is `unknown` | `REVIEW_REQUIRED` |
| An Article 5 prohibited practice is present | `BLOCKED` |
| Annex III domain is present but the tier is not high-risk | `REVIEW_REQUIRED` |
| Risk tier is high-risk | `CONDITIONAL` |
| Risk tier is limited-risk or Article 50 transparency applies | `DISCLOSURE_REQUIRED` |
| Risk tier is minimal-risk | `CLEAR` |

`is_clear` is true only for `CLEAR`. `is_admissible` is true for `CLEAR` and
`DISCLOSURE_REQUIRED`; `CONDITIONAL` deliberately requires a separate
attestation or review step before admission.

## Obligation catalog

High-risk provider obligations:

- risk management system
- data governance
- technical documentation
- record-keeping
- transparency and instructions for use
- human oversight
- accuracy, robustness, and cybersecurity
- quality management system
- conformity assessment
- CE marking
- EU database registration

High-risk deployer obligations:

- fundamental rights impact assessment
- human oversight
- monitoring and logging
- transparency to affected persons
- serious incident reporting
- data protection impact assessment

Limited-risk obligations:

- AI interaction disclosure
- synthetic content marking
- deepfake disclosure
- emotion recognition disclosure

## State machine

```text
DRAFT --assess--> ASSESSED --assess--> ASSESSED
  |                   |
  +------withdraw-----+--> WITHDRAWN
```

`register_system` and `withdraw` are restricted to the publisher. `assess` is
permissionless because the evidence and policy are public.

## Consensus design

The non-deterministic block returns only decision-bearing fields:

```json
{
  "risk_tier": "high",
  "prohibited_practice": false,
  "annex_iii_domain": "employment",
  "transparency_required": false,
  "source_consistency": "consistent",
  "summary": "System ranks job applicants; Annex III employment use case."
}
```

The validator re-fetches both sources, re-runs the extraction, and compares:

- risk tier
- prohibited-practice flag
- Annex III domain
- transparency flag
- source consistency

The free-text summary is stored for auditability but is not part of consensus.
The final decision and obligation list are computed after consensus in
deterministic code.

## Why this is a GenLayer primitive

- AI Act classification depends on live, unstructured public documentation.
- Vendors can change their documentation after a procurement decision.
- A private compliance tool is mutable and not callable by other contracts.
- Every caller can request a fresh assessment without trusting a vendor's
  self-declaration.
- The LLM is constrained to a fixed evidence record; deterministic code owns
  the tier policy and the obligations.
- Validators independently repeat the external reads and the extraction.
- Unknown or conflicting evidence fails closed instead of becoming a silent
  approval.

## Integration

Other contracts can call:

- `is_clear(system_id)` for minimal-risk systems only;
- `is_admissible(system_id)` for minimal-risk and disclosure-only systems;
- `required_obligations(system_id)` for the fixed obligation list;
- `get_assessment(system_id)` for the full public record.

## Example

```text
system_id: acme-support-agent
system_url: https://docs.example.com/acme-support-agent
deployment_url: https://deploy.example.com/acme-support-agent/terms
role: 1
```

Then call `assess("acme-support-agent")`.

Use real official documentation for a live deployment. Placeholder hosts are
only used in tests.

## Repository layout

```text
contracts/ai_act_risk_gate.py
tests/direct/test_ai_act_risk_gate.py
deploy/deployScript.ts
gltest.config.yaml
SUBMISSION.md
```

## Local verification

```shell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
genvm-lint check contracts/ai_act_risk_gate.py
pytest tests/direct/ -v
```

On Windows, `tests/direct/conftest.py` contains a cleanup shim for a
`gltest-direct` temporary-file issue. It does not affect contract behavior.

## Deploy

### Studio

1. Open <https://studio.genlayer.com/>.
2. Select the current GenLayer testnet shown in Studio.
3. Paste `contracts/ai_act_risk_gate.py` and deploy with no constructor
   arguments.
4. Register a real system with two official documentation URLs.
5. Call `assess(system_id)`.
6. Save the contract address, deployment transaction, and successful assessment
   transaction.

### CLI

```shell
npm install
genlayer network
genlayer deploy
```

## Security notes

- Only HTTPS evidence URLs are accepted.
- Source documents are treated as untrusted data, never as instructions.
- Each source is capped at 12,000 characters before prompting.
- Conflicting or insufficient evidence fails closed.
- The contract records a risk-screening signal. It is not legal advice, a
  conformity assessment, or a certification decision.
