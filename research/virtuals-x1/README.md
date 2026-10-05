# X1 — Virtuals External Consequential Transition Validation

Status: OPEN — LEVEL 0 RESEARCH  
Classification: external_architecture_validation_research  
Gating for B2-REAL: false  
Kernel mutation: prohibited  
Execution authority: none  
PayGod mode: observational / shadow only

## Purpose

P0 established a pre-kernel evidence-admission boundary in a simulated gas-maintenance workflow.

X1 asks a different and harder question:

> Can the same bounded PayGod primitives compose with a consequential state transition owned by an external protocol that PayGod did not design?

The first target is Virtuals Agent Commerce Protocol (ACP).

## Current primary runtime target

Level 0 found an important version boundary.

The current CLI path is powered by `acp-node-v2`, not by the older modular ACP router path that X1 initially inspected.

Primary pinned references:

- `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`

The current SDK config identifies Base mainnet chain `8453` and ACP core:

`0x238E541BfefD82238730D00a2208E5497F1832E0`

The SDK ABI names that core `AgenticCommerceV3`.

The older sources remain useful as historical/legacy references:

- `Virtual-Protocol/agent-commerce-protocol@7b490591b2162dbcebed7af47845cad2b0e29cc7`
- `Virtual-Protocol/acp-python@398241f6f132129b41cfadb20b3401a4f968b596`

They MUST NOT be treated as the current production runtime without an explicit historical binding.

See `VERSION_BOUNDARY.md`.

## Current on-chain lifecycle

The pinned current SDK defines:

```text
OPEN       = 0
FUNDED     = 1
SUBMITTED  = 2
COMPLETED  = 3
REJECTED   = 4
EXPIRED    = 5
```

The CLI additionally exposes a derived workflow status `budget_set`, but that is not a separate value in the current on-chain JobStatus enum.

## Initial transition target

Preferred first evaluator-mediated transition:

```text
SUBMITTED → COMPLETED
```

Initial scope is limited to jobs with an explicit non-zero evaluator.

Jobs that complete with evaluator = zero are useful external observations but are excluded from the first evaluator-mediated X1 comparison sample.

## External-system ownership

ACP remains owner of:

- agents/accounts and jobs;
- native job state;
- client/provider/evaluator roles;
- requirements/deliverable transport;
- escrow and USDC settlement;
- hooks and protocol-native controls;
- transaction execution.

PayGod does not reimplement these functions.

## Candidate validation path

```text
External State[n]
      +
Candidate Evidence
      ↓
Evidence Admission
  ├── WITHHELD → NOT RUN
  └── ADMIT
          ↓
      Frozen Policy
          ↓
   Shadow Decision
          ↓
Observed ACP Action
          ↓
External State[n+1]
          ↓
Compare / Diagnose
```

The existing kernel remains unchanged.

## Important evidence-surface boundary

The current SDK/CLI separates on-chain state from authenticated job-room history.

The on-chain core exposes job state and settlement events, while `acp-node-v2` retrieves message/history through an authenticated ACP HTTP/SSE transport.

Therefore X1 MUST distinguish:

```text
public chain evidence
≠ authenticated ACP room evidence
≠ evidence available to the evaluator at cutoff
```

If historical public cases cannot provide the full pre-decision evidence basis, X1 may prospectively create a bounded real job with an independent provider so the complete evidence history can be captured before the evaluator acts.

That is a Level 1 workflow-acquisition step, not a kernel change.

## What a strong X1 result would show

- a real external predecessor state can be reconstructed with a frozen method;
- evidence available before the decision can be separated from later information;
- evidence can be admitted without semantic coercion;
- a PayGod shadow decision can be reproduced from the frozen state/evidence;
- the external native transition can later be observed independently;
- disagreement can be diagnosed without changing the kernel merely to obtain agreement.

## Hypothesis-only items

The following are not current PayGod primitives or guarantees:

- predecessor-state binding;
- causal binding between PayGod decision and external execution;
- post-flight conformance;
- next-transition eligibility;
- protocol-independent authority.

## Levels

- Level 0 — Research Freeze
- Level 1 — Real Workflow Acquisition
- Level 2 — State Reconstruction
- Level 3 — Evidence Admission
- Level 4 — Shadow Decision
- Level 5 — Outcome Observation
- Level 6 — Diagnosis
- Level 7 — Go/Stop

No level may be skipped.

## Non-claims

X1 does not currently establish:

- a PayGod/Virtuals production integration;
- authority to block or permit ACP transitions;
- payment-control authority;
- complete public reconstruction of ACP job-room evidence;
- post-flight conformance;
- protocol independence;
- market demand or willingness to pay.

## Stop-build interaction

Virtuals may challenge the architecture.

Virtuals may not redesign the kernel by suggestion alone.
