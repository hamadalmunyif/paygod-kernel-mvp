# X1 Evaluator Prevalence — External Research Note

Status: SECONDARY EXTERNAL EVIDENCE — NOT INDEPENDENTLY REPRODUCED BY PAYGOD
Observed: 2026-10-05
Purpose: inform Level 0 experiment design without promoting third-party measurements into repository guarantees.

## Reported measurement

A public Ethereum Magicians post dated 2026-08-19 reports an indexed sample of 62,953 Virtuals ACP jobs on Base and states:

- 72.50% had no evaluator set;
- 27.48% used the client as evaluator;
- 0.02% — ten jobs in that sample — used an evaluator independent from the client;
- 76.1% of settled USDC volume was self-evaluated.

Source:
https://ethereum-magicians.org/t/erc-8183-agentic-commerce/27902/393

A separate 2026-09-24 analysis reports reading 81,095 jobs from AgenticCommerceV3 and states that its overlapping sample reproduced the same evaluator proportions. It identifies the production Base contract as `0x238E541BfefD82238730D00a2208E5497F1832E0`.

Source:
https://llm4agents.com/blog/erc-8183-agentic-commerce-job-escrow-audit

## X1 treatment

These measurements are **not** an X1 witness because PayGod has not independently reproduced the scans, pinned the exact query code/data, or verified all denominators.

They are retained only as a research lead.

If the reported distribution is directionally correct, arbitrary historical sampling is unlikely to yield many independently evaluated jobs with reconstructable pre-decision evidence.

That strengthens — but does not yet authorize — the Level 0 proposal to create a bounded real job where X1 deliberately controls:

- the requirement freeze;
- the evidence cut-off;
- an explicit non-zero evaluator;
- the data-capture path;
- the economic cap;
- preservation of the external provider's independent work.

## Architectural relevance

The reported scarcity of independent evaluation does not prove that PayGod is needed.

It identifies a potentially valuable falsification question:

> When ACP supplies a native evaluator slot and economic settlement, does an explicit evidence-admission / decision-basis layer add material information beyond the evaluator address and the final complete/reject transaction?

X1 must answer that with its own controlled evidence.

## Non-claims

This note does not claim:

- that the reported percentages remain current;
- that every ACP rail uses the same evaluator distribution;
- that self-evaluation is invalid;
- that PayGod would improve these outcomes;
- that an independent evaluator is required by ACP;
- that any reported weakness is a kernel requirement.
