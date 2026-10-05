# X1 Current Runtime Witness 001 — Evaluator-Zero Auto-Completion

Status: OBSERVED — EXCLUSION WITNESS  
Rail: current ACP Node v2 / AgenticCommerceV3  
Chain: Base mainnet  
ACP contract: `0x238E541BfefD82238730D00a2208E5497F1832E0`

## Observed transaction

Transaction:

`0xc767da642b7647c7b3b8324f404cf5270532a43bcc084c355077ef1c8ab0d880`

Explorer:

`https://basescan.org/tx/0xc767da642b7647c7b3b8324f404cf5270532a43bcc084c355077ef1c8ab0d880`

Decoded receipt records include:

- `JobSubmitted` for job `13868`;
- `JobCompleted` for job `13868`;
- evaluator = `0x0000000000000000000000000000000000000000`;
- `PaymentReleased` for job `13868`;
- provider = `0xDF5e15C898c869340135F39040bdf451a93f9dD8`;
- released provider amount = `9500` Base-USDC base units;
- an additional `500` Base-USDC base-unit transfer from the ACP contract is visible in the same transaction.

The two visible USDC transfers sum to `10000` base units = `0.01 USDC` under the 6-decimal Base USDC used by the current SDK.

## Finding

A current-rail job may complete and release funds with evaluator set to the zero address.

Therefore:

```text
COMPLETED
does not imply
an explicit evaluator made a decision
```

## X1 consequence

The first evaluator-mediated comparison sample MUST require:

`evaluator != 0x0000000000000000000000000000000000000000`

This witness is deliberately excluded from the evaluator-mediated sample.

## Non-claims

This record does not establish:

- evaluator quality;
- a PayGod-comparable evidence package;
- PayGod executability;
- independent evaluation;
- causal PayGod authority;
- post-flight conformance.

Its value is negative-space evidence: it proves why X1 must select the native decision boundary explicitly instead of treating every COMPLETED job as an evaluator decision.
