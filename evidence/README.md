# Deployment evidence

- Contract: `0x3f8B4C5cBEA84Ebb90687F497bb1130D1815EeEf`
- Contract Explorer: https://explorer-studio.genlayer.com/address/0x3f8B4C5cBEA84Ebb90687F497bb1130D1815EeEf
- Deployment tx: `0x8f3cfc91f5bc88670d16cbb2f9bdfcf4958e147d9e1af3e12e16d2aa077ce233`
- Deployment Explorer: https://explorer-studio.genlayer.com/tx/0x8f3cfc91f5bc88670d16cbb2f9bdfcf4958e147d9e1af3e12e16d2aa077ce233
- `register_system` tx: `0xe5097eb14d8519a41199d62495c05da1499c907476ca8c39189d90d0b602c6c4`
- Registration Explorer: https://explorer-studio.genlayer.com/tx/0xe5097eb14d8519a41199d62495c05da1499c907476ca8c39189d90d0b602c6c4
- `assess` tx: `0xac18a4c61b430d5b58a814d4584ccc26acadc34bcebb087a6f588761ea0b3be7`
- Assessment Explorer: https://explorer-studio.genlayer.com/tx/0xac18a4c61b430d5b58a814d4584ccc26acadc34bcebb087a6f588761ea0b3be7

## Live result

- System: `gemma-2-9b-it`
- System documentation: https://huggingface.co/google/gemma-2-9b-it
- Deployment documentation: https://arxiv.org/html/2408.00118
- Decision: `DISCLOSURE_REQUIRED` (`decision = 2`)
- Risk tier: `limited` (`risk_tier = 2`)
- Transparency required: `true`
- Source consistency: `consistent`
- Round: `1`
- Obligations: `ai_interaction_disclosure`, `synthetic_content_marking`,
  `deepfake_disclosure`, `emotion_recognition_disclosure`

## Screenshot

- `studio-assessment.png` — GenLayer Studio after the finalized `assess`
  transaction, showing the deployed contract, transaction log, and accepted
  `get_assessment` response.

## Portal form

- `portal-form-top.png` — Intelligent Contracts category and weekly quota (0/2 used).
- `portal-form-description.png` — title and the 996/1000 description with the
  source repository URL.
- `portal-form-middle.png` — contract Explorer and transaction evidence.
- `portal-form-filled.png` — final evidence cards, reCAPTCHA, and submit button.
- Evidence list: raw README URL (`Other`), contract Explorer
  (`GenLayer Explorer Contract`), deployment tx, `register_system` tx,
  `assess` tx, and Studio Contract import URL (`GenLayer Studio Contract`).
- The two required evidence groups are satisfied by the Studio Contract import
  URL and the contract Explorer URL.
- The source repository URL is in the description because the portal client
  redacts `github.com/...` values in evidence inputs; the raw README URL is
  included as supporting GitHub evidence.
- Final reCAPTCHA and `提交贡献` remain with the user.
