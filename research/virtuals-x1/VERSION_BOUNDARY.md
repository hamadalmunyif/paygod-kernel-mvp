# X1 Version Boundary — Current Runtime vs Legacy Modular ACP

Status: ACCEPTED LEVEL 0 FINDING
Observed: 2026-10-05

## Finding

"Virtuals ACP" is not a sufficiently precise execution identity for X1.

The initial X1 source review focused on the modular Solidity repository and older Python SDK:

```text
ACPRouter
  ├─ AccountManager
  ├─ JobManager
  ├─ MemoManager
  ├─ PaymentManager
  └─ AssetManager
```

with phases resembling:

```text
REQUEST → NEGOTIATION → TRANSACTION → EVALUATION → COMPLETED
```

Further review of the current official CLI showed that its default current v2 path uses `acp-node-v2` and a current Base core whose SDK ABI names `AgenticCommerceV3`.

The current SDK JobStatus is:

```text
OPEN → FUNDED → SUBMITTED → COMPLETED
                     └────→ REJECTED
plus EXPIRED
```

The CLI adds a derived `budget_set` workflow status between open and funded.

## Current primary X1 target

- `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`
- Base chain id `8453`
- ACP core `0x238E541BfefD82238730D00a2208E5497F1832E0`

The preferred evaluator-mediated transition is now:

```text
SUBMITTED → COMPLETED
```

with an explicit non-zero evaluator.

## Legacy/historical reference

The earlier modular source remains useful for historical and comparative analysis, but it is no longer the primary current-runtime target.

No old modular transition may be labeled as a current-runtime X1 comparison case.

## Architectural consequence

This finding supports a stricter external-state rule:

```text
protocol name
      ≠
deployment identity
      ≠
implementation identity
      ≠
state at decision block
```

For X1, the target of a future decision must be bound to the actual external state/version that existed at the decision cut-off.

This is still a research requirement. It does not promote predecessor-state binding into the PayGod kernel.
