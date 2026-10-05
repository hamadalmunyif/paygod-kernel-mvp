# X1 External Witness 001 — Legacy Modular ACP Transition

Status: OBSERVED — LEGACY/HISTORICAL PATH — NOT AN X1 QUALIFYING CASE
Chain: Base mainnet
Purpose: preserve the first external transition witness while explicitly separating it from the current primary ACP runtime.

## Version-boundary note

This witness was discovered against the older modular ACP path represented by:

- `Virtual-Protocol/agent-commerce-protocol@7b490591b2162dbcebed7af47845cad2b0e29cc7`;
- the older Python SDK's Base modular-router configuration.

Subsequent Level 0 review established that the current official CLI v2 flow is powered by `acp-node-v2` and the Base core `0x238E541BfefD82238730D00a2208E5497F1832E0`.

Therefore this witness is retained as historical evidence of a real ACP economic transition, but it is outside the primary current-runtime X1 comparison target.

## Observed legacy job

Job id: `1003349284`

Submission/move toward evaluation:

`0xc4f0db3beb0b9c702150141d7f7312b95b069383d852ce6ba32e15b5f7aaa8c0`

Observed decoded records included:

- a `NewMemo` record;
- `jobId = 1003349284`;
- `nextPhase = 4`;
- content reference `https://acpx.virtuals.io/api/memo-contents/505689`;
- `JobPhaseUpdated` `2 → 3`.

Completion/economic release:

`0x369363a969500904360b1f2bb02c837acf4f0cb059238a929bb372edc3d1a17c`

Observed decoded records included:

- `JobPhaseUpdated` `3 → 4`;
- USDC transfers;
- `PaymentReleased` for the same job.

## What this witness establishes

It establishes that a prior ACP runtime contained a real external state transition with an economic consequence.

## What it does not establish

It does not establish:

- current `acp-node-v2` semantics;
- current production-core state;
- a current-runtime evaluator-mediated transition;
- a complete predecessor-state snapshot;
- a frozen evidence basis;
- PayGod executability;
- causal PayGod authorization;
- post-flight conformance.

## Research significance

The fact that X1 encountered two materially different ACP runtime shapes before its first comparison case is itself a useful result.

It strengthens the requirement that any PayGod decision over an external protocol must bind to the actual protocol/deployment state being governed rather than to a timeless product name such as "Virtuals ACP".
