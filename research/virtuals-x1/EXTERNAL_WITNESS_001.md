# X1 External Witness 001 — Real ACP Completion Transition

Status: OBSERVED — NOT YET AN X1 QUALIFYING CASE
Chain: Base mainnet
Purpose: establish that the candidate transition exists in real external execution with economic consequence.

## Observed job

Job id: `1003349284`

The following public Base transactions expose a real lifecycle segment for this job.

### Submission / move into evaluation

Transaction:

`0xc4f0db3beb0b9c702150141d7f7312b95b069383d852ce6ba32e15b5f7aaa8c0`

Observed decoded events include:

- `NewMemo` from the observed MemoManager event source;
- `jobId = 1003349284`;
- `nextPhase = 4` (COMPLETED target under the pinned source enum);
- content reference `https://acpx.virtuals.io/api/memo-contents/505689`;
- `JobPhaseUpdated` for the same job from phase `2 → 3` (TRANSACTION → EVALUATION under the pinned source enum).

### Completion and economic release

Transaction:

`0x369363a969500904360b1f2bb02c837acf4f0cb059238a929bb372edc3d1a17c`

Observed decoded events include:

- `JobPhaseUpdated` for `jobId = 1003349284`;
- phase `3 → 4` (EVALUATION → COMPLETED under the pinned source enum);
- USDC transfers from `0xEF4364Fe4487353dF46eb7c811D4FAc78b856c7F`;
- `PaymentReleased` for the same job;
- released recipient `0xd478a8B40372db16cA8045F28C6FE07228F3781A`;
- released amount `8000` base units of Base USDC, with a separate `2000` base-unit transfer visible in the same completion transaction.

This is sufficient to establish a real external state transition with an economic consequence.

## What this witness does not yet establish

This record does NOT yet establish:

- the full predecessor-state snapshot;
- the job's creation event and evaluator identity within this same frozen witness;
- the exact deployed implementation identity at each relevant block;
- the complete requirement/deliverable evidence available before the completion decision;
- that the off-chain memo content reference is immutable, independently available, or admissible;
- that PayGod would have been executable for this job;
- that PayGod caused, authorized, or influenced the completion;
- post-flight conformance.

Therefore this is an external transition witness, not an X1 comparison case.

## Why it matters

P0 tested the refusal boundary before the kernel.

This witness demonstrates that X1's target environment contains the next required ingredient:

```text
real external state
    ↓
real transition into EVALUATION
    ↓
real EVALUATION → COMPLETED transition
    ↓
real payment release
```

The next Level 0 task is not to build an adapter. It is to determine whether this or another job can be reconstructed faithfully enough to freeze:

```text
State[n]
+ evidence available before evaluator action
+ actor/authority context
+ target transition
```

without relying on post-decision information.

## Source-code caution

The phase labels above are interpreted against the pinned source enum in:

`Virtual-Protocol/agent-commerce-protocol@7b490591b2162dbcebed7af47845cad2b0e29cc7`

The deployed implementation at the historical block has not yet been cryptographically/source-bound to that commit. The numeric transitions are observed facts; their semantic labels remain subject to that Level 0 binding task.
