# X1 — Virtuals External Consequential Transition Validation

Status: OPEN — LEVEL 0 RESEARCH  
Classification: external_architecture_validation_research  
Gating for B2-REAL: false  
Kernel mutation: prohibited  
Execution authority: none  
PayGod mode: observational / shadow only

## Purpose

P0 established a pre-kernel evidence-admission boundary in a simulated gas-maintenance workflow.

X1 asks a different question:

> Can the same bounded PayGod primitives compose with a consequential state transition owned by an external protocol that PayGod did not design?

The first target is Virtuals Agent Commerce Protocol (ACP).

Initial source reference:

- repository: `Virtual-Protocol/agent-commerce-protocol`
- observed commit: `7b490591b2162dbcebed7af47845cad2b0e29cc7`
- license: MIT
- observed modular components: ACPRouter, AccountManager, JobManager, MemoManager, PaymentManager, AssetManager

This source reference does not prove a particular live deployment. Level 0 must establish deployment facts before X1 makes operational claims.

## Initial transition target

Preferred first transition:

```text
EVALUATION → COMPLETED
```

Initial scope is limited to jobs with an explicit non-zero evaluator. X1 does not assume that every ACP completion follows this route.

## External-system ownership

ACP remains owner of its accounts, jobs, actors, phases, memos, approvals, escrow/payment handling, cross-chain transport, and transaction execution.

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

## What a strong X1 result would show

- a real external predecessor state can be reconstructed with a frozen method;
- evidence can be admitted without semantic coercion;
- a PayGod shadow decision can be reproduced from that state/evidence;
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

X1 does not currently establish a live Virtuals integration, production ACP deployment identity, real external workflow evidence, authority to block ACP transitions, payment-control authority, post-flight conformance, protocol independence, market demand, or willingness to pay.

## Stop-build interaction

Virtuals may challenge the architecture.

Virtuals may not redesign the kernel by suggestion alone.
