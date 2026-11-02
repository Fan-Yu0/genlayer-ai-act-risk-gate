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
- Contract: `0x3f8B4C5cBEA84Ebb90687F497bb1130D1815EeEf`
- Contract Explorer:
  https://explorer-studio.genlayer.com/address/0x3f8B4C5cBEA84Ebb90687F497bb1130D1815EeEf
- Deployment transaction:
  `0x8f3cfc91f5bc88670d16cbb2f9bdfcf4958e147d9e1af3e12e16d2aa077ce233`
- Deployment Explorer:
  https://explorer-studio.genlayer.com/tx/0x8f3cfc91f5bc88670d16cbb2f9bdfcf4958e147d9e1af3e12e16d2aa077ce233
- System registration transaction:
  `0xe5097eb14d8519a41199d62495c05da1499c907476ca8c39189d90d0b602c6c4`
- Registration Explorer:
  https://explorer-studio.genlayer.com/tx/0xe5097eb14d8519a41199d62495c05da1499c907476ca8c39189d90d0b602c6c4
- Successful assessment transaction:
  `0xac18a4c61b430d5b58a814d4584ccc26acadc34bcebb087a6f588761ea0b3be7`
- Assessment Explorer:
  https://explorer-studio.genlayer.com/tx/0xac18a4c61b430d5b58a814d4584ccc26acadc34bcebb087a6f588761ea0b3be7
- Recorded decision: `DISCLOSURE_REQUIRED` (`decision = 2`), risk tier
  `limited` (`risk_tier = 2`), `transparency_required = true`,
  `source_consistency = consistent`, round `1`.
- Live system: `gemma-2-9b-it`
- System documentation: https://huggingface.co/google/gemma-2-9b-it
- Deployment documentation: https://arxiv.org/html/2408.00118

## First live example

Use these values in the deployed Studio contract:

```text
system_id: gemma-2-9b-it
system_url: https://huggingface.co/google/gemma-2-9b-it
deployment_url: https://arxiv.org/html/2408.00118
role: 1
```

Then call `assess("gemma-2-9b-it")`.

The live call returned `DISCLOSURE_REQUIRED` with risk tier `limited`,
`transparency_required = true`, and the limited-risk obligation set.

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
