# X1 External Witness 001 — Legacy Modular ACP Completion Transition

Status: OBSERVED LEGACY-RAIL WITNESS — NOT AN X1 QUALIFYING CASE
Chain: Base mainnet
Protocol generation: earlier modular ACP v2
Purpose: preserve evidence that ACP has produced real economically consequential transitions without confusing the historical rail with the current X1 target.

## Observed job

Job id: `1003349284`

This witness belongs to the earlier modular ACP v2 generation associated with the older Python SDK/router. It does NOT establish activity on the current `acp-node-v2` / AgenticCommerceV3 Base contract.

### Submission / move into evaluation

Transaction:

`0xc4f0db3beb0b9c702150141d7f7312b95b069383d852ce6ba32e15b5f7aaa8c0`

Observed decoded events include:

- `NewMemo` from the historical modular MemoManager event source;
- `jobId = 1003349284`;
- `nextPhase = 4`;
- content reference `https://acpx.virtuals.io/api/memo-contents/505689`;
- `JobPhaseUpdated` for the same job from numeric phase `2 → 3`.

Against the pinned earlier modular source enum, those numeric phases correspond to TRANSACTION → EVALUATION.

### Completion and economic release

Transaction:

`0x369363a969500904360b1f2bb02c837acf4f0cb059238a929bb372edc3d1a17c`

Observed decoded events include:

- `JobPhaseUpdated` for `jobId = 1003349284`;
- numeric phase `3 → 4`;
- USDC transfers from `0xEF4364Fe4487353dF46eb7c811D4FAc78b856c7F`;
- `PaymentReleased` for the same job;
- released recipient `0xd478a8B40372db16cA8045F28C6FE07228F3781A`;
- released amount `8000` base units of Base USDC, with a separate `2000` base-unit transfer visible in the same completion transaction.

Against the pinned earlier modular source enum, numeric phase 3 → 4 corresponds to EVALUATION → COMPLETED.

## What this witness establishes

Only the bounded observation:

```text
historical external ACP state
→ real completion transition
→ real economic release
```

This is useful evidence that ACP is not merely a synthetic state machine.

## What this witness does not establish

It does NOT establish:

- the current ACP Node v2 / AgenticCommerceV3 rail;
- the full predecessor-state snapshot;
- evaluator identity within a frozen X1 package;
- deployed implementation/source equivalence at the historical blocks;
- complete pre-decision requirement/deliverable evidence;
- admissibility or immutability of the off-chain memo content;
- PayGod executability;
- PayGod causation or authorization;
- post-flight conformance.

Therefore this record MUST NOT be used as the first current-rail X1 comparison case.

## Current-rail consequence

After this witness was recorded, Level 0 identified a newer official ACP stack:

- `Virtual-Protocol/acp-node-v2`
- Base current SDK contract `0x238E541BfefD82238730D00a2208E5497F1832E0`
- current workflow `submitted → completed/rejected`

The historical witness remains preserved; the target rail changes rather than rewriting the old observation.

This is exactly why X1 freezes source/deployment context before promoting a transition into a comparison case.
