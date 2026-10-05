# X1 Current Runtime Witness 001 — Auto-Completion on Base

Status: OBSERVED — CURRENT RUNTIME — EXCLUDED FROM EVALUATOR-MEDIATED SAMPLE
Chain: Base mainnet
ACP core: `0x238E541BfefD82238730D00a2208E5497F1832E0`
Job id: `13868`

## Transaction

`0xc767da642b7647c7b3b8324f404cf5270532a43bcc084c355077ef1c8ab0d880`

Explorer:
`https://basescan.org/tx/0xc767da642b7647c7b3b8324f404cf5270532a43bcc084c355077ef1c8ab0d880`

The decoded receipt exposes, from the current ACP core:

- `JobSubmitted(jobId=13868, ...)`;
- `JobCompleted(jobId=13868, evaluator=0x0000000000000000000000000000000000000000, ...)`;
- `PaymentReleased(jobId=13868, provider=0xDF5e15C898c869340135F39040bdf451a93f9dD8, amount=9500)`;
- Base USDC transfers from the ACP core, including 9500 base units to the provider and 500 base units to another recipient.

Under the 6-decimal Base USDC token used by the current SDK, those two transfers sum to 0.01 USDC.

## Interpretation

The current runtime can reach completion and release funds with the evaluator recorded as the zero address.

This witness therefore does not exercise the evaluator-mediated decision boundary X1 wants to study.

It is an exclusion witness.

## Why it matters

X1 must not assume:

```text
COMPLETED
⇒ an evaluator made a decision
```

The first frozen candidate sample must explicitly require:

```text
evaluator != 0x0000000000000000000000000000000000000000
```

and must reconstruct a distinct pre-completion `SUBMITTED` state.

## What this witness does not establish

It does not establish:

- independent evaluation;
- the evaluator evidence basis;
- a PayGod-comparable decision;
- predecessor-state completeness;
- PayGod executability;
- post-flight conformance.

It establishes only that the current deployed economic rail contains real completion and payment-release behavior, and that evaluator-zero completion must be excluded from the first evaluator-mediated X1 sample.
