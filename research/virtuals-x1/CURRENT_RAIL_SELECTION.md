# X1 Current Rail Selection

Status: SELECTED — LEVEL 0 CLOSED; X1-R0 PREPURCHASE FREEZE; SPEND UNAUTHORIZED
Decision date: 2026-10-05

## Decision

For new X1 workflow acquisition, use the official ACP Node v2 rail captured by the frozen Level 0 baseline as the primary target. Level 0 verification is complete; X1-R0 remains the next bounded instrumentation step and no purchase is authorized by this selection.

Level 0 pinned references (frozen research baseline; not a claim of latest upstream HEAD):

- `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`
- Base chain id `8453`
- SDK-configured ACP contract `0x238E541BfefD82238730D00a2208E5497F1832E0`

Preferred transition:

```text
SUBMITTED → COMPLETED
```

with explicit non-zero evaluator.

## Why

The current official SDK/CLI no longer models the primary workflow as the earlier modular REQUEST/NEGOTIATION/TRANSACTION/EVALUATION phase machine.

Current Node v2 exposes a simpler job lifecycle and EVM ABI:

```text
OPEN
→ FUNDED
→ SUBMITTED
→ COMPLETED | REJECTED
```

The CLI/transport also exposes a derived `budget_set` state between open and funded.

For X1, the decision point of interest is still conceptually the same: a provider has submitted a deliverable and an evaluator may cause a consequential completion/rejection transition. The protocol surface changed; the research question did not.

## Historical rail treatment

The earlier modular router `0xa6C9BA866992cfD7fd6460ba912bfa405adA9df0` and its manager contracts remain useful historical evidence.

They MUST NOT be presented as the current ACP Node v2 deployment.

External Witness 001 is therefore classified as a legacy-rail witness and retained unchanged in its underlying observations.

## Experimental implication

Because current ACP chat/history access is participant-authenticated, the strongest first X1 case may require X1 to become a legitimate client/evaluator in a bounded real job with an independent provider.

That is not authorized as a purchase by this document. Level 0 has frozen:

- offering selection criteria;
- maximum economic exposure;
- requirement schema;
- evidence policy;
- evaluator identity;
- cut-off;
- candidate retention;
- data capture plan.

That freeze is complete. Level 1 workflow acquisition still requires the separate explicit economic authorization defined by the X1-R0 pre-purchase gate.

## Non-decision

This selection does not authorize:

- kernel changes;
- ACP adapter implementation;
- automated payments;
- authority gating;
- post-flight conformance;
- any purchase without the separate explicit X1-R0 economic authorization.
