# Portal submission draft

## Category

Builder -> Intelligent Contract

## Contribution date

Use the actual deployment date. Do not select a future date.

## Description (English, under 1,000 characters)

AI Act Risk Gate is a reusable GenLayer primitive for public, reproducible EU AI
Act screening. A publisher registers a system ID, official system
documentation, deployment documentation, and provider/deployer role. Anyone can
trigger an assessment. Validators independently fetch both sources; an LLM
extracts only the risk tier, prohibited-practice flag, Annex III domain,
transparency flag, and source consistency. Deterministic code applies a fixed
policy: prohibited practices are blocked, high-risk systems are conditional,
limited-risk systems require disclosure, minimal-risk systems are clear, and
conflicting or unknown evidence requires review. The contract also returns the
fixed obligation catalog for the tier and role. Other contracts can consume
`is_clear`, `is_admissible`, and `required_obligations`. The repository includes
source, tests, and deployment instructions for AI marketplaces, agent
registries, procurement, and DAOs.

## Live evidence

- Public source repository:
  https://github.com/Fan-Yu0/genlayer-ai-act-risk-gate
- Contract: TBD
- Contract Explorer: TBD
- Deployment transaction: TBD
- Deployment Explorer: TBD
- Successful assessment transaction: TBD
- Assessment Explorer: TBD
- Recorded decision: TBD

## First live example

Use these values in the deployed Studio contract:

```text
system_id: acme-support-agent
system_url: https://docs.example.com/acme-support-agent
deployment_url: https://deploy.example.com/acme-support-agent/terms
role: 1
```

Then call `assess("acme-support-agent")`.

Replace the placeholder URLs with two real official documentation pages before
the live call.

## Submission notes

The contract is intentionally not a project or frontend submission. The core
deliverable is the reusable on-chain state machine, constrained evidence
extraction, and independent validator comparison. The live example should use
two real official documentation URLs.

## Reviewer checklist

- Persistent state and a clear lifecycle.
- Publisher-only registration and withdrawal.
- Permissionless evidence refresh.
- Validator independently re-fetches both sources and re-runs extraction.
- The LLM returns only a constrained evidence record.
- The final decision and obligations are deterministic.
- Conflicting or unknown evidence fails closed.
- Source, tests, documentation, and deployment instructions are public.
