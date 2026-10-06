# X1 — Virtuals External Consequential Transition Validation

Status: OPEN — LEVEL 0 CLOSED; X1-R0 PREPURCHASE FREEZE; SPEND UNAUTHORIZED  
Classification: external_architecture_validation_research  
Gating for B2-REAL: false  
Kernel mutation: prohibited  
Execution authority: none  
PayGod mode: observational / shadow only

## Purpose

P0 established a pre-kernel evidence-admission boundary in a simulated gas-maintenance workflow.

X1 asks:

> Can the same bounded PayGod primitives compose with a consequential state transition owned by an external protocol that PayGod did not design?

## Current rail selection

Level 0 found two distinct ACP generations. The default target for new X1 workflow acquisition is the official Node v2 rail captured by the frozen Level 0 references below. These pins preserve the research baseline; they are not a claim that the pinned commits are the latest upstream HEADs.

- Level 0 pinned SDK: `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- Level 0 pinned CLI: `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`
- Base chain id: `8453`
- SDK-configured Base ACP contract: `0x238E541BfefD82238730D00a2208E5497F1832E0`
- current ACP server: `https://api.acp.virtuals.io`

The earlier modular ACP v2 source/router remains a historical witness rail only.

See `CURRENT_RAIL_SELECTION.md` and `DEPLOYMENT_INVENTORY.md`.

## Initial current-rail transition target

Preferred first transition:

```text
SUBMITTED → COMPLETED
```

with an explicit non-zero evaluator.

The current SDK exposes evaluator tools only at `submitted`, where `complete` and `reject` become available. The underlying EVM ABI exposes `complete(uint256,bytes32,bytes)` and emits `JobCompleted`.

X1 does not infer on-chain authority solely from SDK role gating; deployed-contract behavior must be independently bound.

## Evidence zones

Current ACP Node v2 separates evidence naturally:

- public/native chain evidence;
- authenticated participant history from ACP chat/event services.

Because `getHistory` is authentication-gated, X1 must not assume arbitrary historical requirements and deliverables are public.

Level 0 therefore selects a **prospective bounded real ACP job** as the preferred route to the first fully reconstructable workflow if public historical evidence remains incomplete. The first such job is classified `X1-R0` and is an instrumentation case, not architecture proof.

No live purchase is authorized until the maximum economic exposure, provider/offering, requirement criteria, evaluator identity, and capture procedure are explicitly frozen. See `LEVEL0_ACQUISITION_DECISION.md` and `CASE_PROTOCOL.md`.

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

The existing PayGod kernel remains unchanged.

## What a strong X1 result would show

- real external predecessor state reconstructed with a frozen method;
- evidence admitted without semantic coercion;
- a reproducible PayGod shadow decision when executable;
- an independently observable external native transition;
- disagreement diagnosed without changing the kernel merely to obtain agreement.

## Hypothesis-only items

Not current PayGod guarantees:

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

X1 does not currently establish a production PayGod/Virtuals integration, authority to block ACP transitions, payment-control authority, post-flight conformance, protocol independence, market demand, or willingness to pay.

## Stop-build interaction

Virtuals may challenge the architecture.

Virtuals may not redesign the kernel by suggestion alone.
