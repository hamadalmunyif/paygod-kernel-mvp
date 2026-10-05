# X1 Current Rail Selection

Status: PROVISIONAL — LEVEL 0
Decision date: 2026-10-05

## Decision

For new X1 workflow acquisition, use the current official ACP Node v2 rail as the primary target unless Level 0 verification disproves the configuration.

Pinned current references:

- `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`
- Base chain id `8453`
- SDK-configured ACP contract `0x238E541BefD82238730D00a2208E5497F1832E0`

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

That is not yet authorized as a purchase by this document. Level 0 must first freeze:

- offering selection criteria;
- maximum economic exposure;
- requirement schema;
- evidence policy;
- evaluator identity;
- cut-off;
- candidate retention;
- data capture plan.

Only after that freeze may Level 1 workflow acquisition begin.

## Non-decision

This selection does not authorize:

- kernel changes;
- ACP adapter implementation;
- automated payments;
- authority gating;
- post-flight conformance;
- any purchase before Level 0 experimental controls are frozen.
