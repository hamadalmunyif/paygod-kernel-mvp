# X1-RW-001 — First Real Current-Rail Workflow Protocol

Status: DRAFT FREEZE — NO PURCHASE AUTHORIZED
Track: X1 — Virtuals External Consequential Transition Validation
Rail: current ACP Node v2 / AgenticCommerceV3
Chain: Base mainnet (8453)
ACP contract: `0x238E541BfefD82238730D00a2208E5497F1832E0`
Kernel mutation: prohibited
PayGod mode: shadow only when/if the case becomes executable

## Objective

Acquire one economically real ACP workflow from an independent provider while preserving enough pre-decision evidence to test the PayGod boundary without controlling the provider or the ACP execution rail.

The first job is not intended to prove market demand or protocol independence.

It is intended to answer a narrower question:

> Can X1 preserve a real external provider workflow from requirement through submission and evaluator action, freeze the evidence available before that action, and later determine whether PayGod can evaluate the transition without semantic coercion?

## Proposed real task

Task class: **structured technical verification / research**.

Useful task intent:

> Independently verify the current Virtuals ACP Base deployment and evaluator/completion surface, and return a structured evidence-backed report.

The task is deliberately useful to X1 and independently checkable.

### Required deliverable shape

The provider should return machine-readable JSON containing at least:

```json
{
  "chain_id": 8453,
  "acp_contract": "0x...",
  "payment_token": "0x...",
  "native_job_statuses": [],
  "completion_function": "",
  "rejection_function": "",
  "evaluator_condition": "",
  "sources": [
    {
      "type": "official_source|onchain_explorer|other",
      "reference": "",
      "supports": []
    }
  ],
  "uncertainties": []
}
```

A short narrative may accompany the JSON, but the structured fields are the primary deliverable.

The provider is not shown PayGod output or the experiment's expected values.

## Offering-selection freeze

Before browsing live offerings, use the following eligibility rule.

A provider/offering is eligible only if:

- it is discoverable on the current ACP rail;
- the provider is not controlled by the PayGod experiment operator;
- the offering can reasonably perform technical research, data analysis, or structured verification;
- its requirement schema can accept the task without misrepresentation;
- the offering is available on Base mainnet;
- its quoted/budget amount is at or below the separately approved economic cap;
- no subscription or fund-transfer hook is required unless explicitly recorded and approved before funding;
- no credentials, secrets, private data, or privileged access are required.

Preferred discovery query order:

1. `technical research`
2. `data analysis`
3. `research`

Within the first query that returns eligible offerings, rank by the current SDK's available objective metrics in this order where available:

1. successful job count;
2. success rate;
3. recency/online status.

Select the first eligible offering under the economic cap.

Do not skip an eligible offering because its expected result looks inconvenient for PayGod.

If no eligible offering exists, record `X1-RW-001 = STOP_NO_ELIGIBLE_OFFERING`; do not silently change the experiment into an unrelated task.

## Economic control

No payment or job creation is authorized by this document.

Before Level 1 acquisition begins, freeze:

- maximum total USDC exposure;
- gas exposure policy;
- whether a separate evaluator wallet/agent is available;
- who is authorized to fund;
- who is authorized to execute the final ACP evaluator action.

Funding requires explicit human approval.

## Role separation

Required:

- provider address is external to the experiment operator;
- evaluator is non-zero;
- evaluator is not the provider.

Preferred:

- evaluator is distinct from the client;
- the human reviewer controlling/authorizing the evaluator does not see the PayGod result before freezing the human/native decision.

If evaluator == client is necessary, record it and do not claim independent third-party evaluation.

## Pre-job freeze

Before `createJob`, freeze and hash:

- experiment id;
- task requirement;
- deliverable schema;
- acceptance criteria;
- provider-selection rule;
- selected offering identity and quoted price;
- current rail/source pins;
- economic cap;
- evaluator identity;
- evidence cut-off rule.

The provider must not receive hidden acceptance facts beyond the task requirements.

## Acceptance criteria for the human evaluator

The evaluator reviews only evidence available before the evaluator action.

A proposed completion is supportable only when:

- the deliverable parses as the required JSON;
- every required field is present;
- each material claim is linked to at least one source reference;
- the current ACP contract claim is supported by an official/current source or direct chain evidence;
- contradictions are disclosed rather than silently resolved;
- uncertainties are explicitly listed;
- no obviously post-evaluation evidence is used to justify the pre-evaluation decision.

This human policy is frozen before seeing the provider result.

It is not a PayGod pack and does not authorize kernel or pack implementation.

## Evidence cut-off

For X1-RW-001, the cut-off is the instant immediately before the evaluator freezes its native decision.

Evidence is classified:

- AVAILABLE_BEFORE_CUTOFF;
- AFTER_CUTOFF;
- UNPROVEN_AT_CUTOFF.

Only AVAILABLE_BEFORE_CUTOFF may support the frozen evaluator decision or later PayGod shadow input.

## Blind decision sequence

```text
freeze requirement + acceptance policy
        ↓
create / fund real ACP job
        ↓
independent provider works
        ↓
provider submits
        ↓
capture predecessor state + evidence
        ↓
freeze evidence cut-off
        ↓
human evaluator freezes native intent
COMPLETE | REJECT | DEFER
        ↓
human reviewer becomes blind to PayGod result
        ↓
Evidence Admission
        ↓
NOT RUN or PayGod shadow decision
        ↓
execute the already-frozen native ACP action
(if COMPLETE or REJECT)
        ↓
capture tx / events / successor state / payment outcome
        ↓
compare and diagnose
```

PayGod must not cause the first native action.

## Human native-intent semantics

- `COMPLETE`: evidence available at cut-off supports accepting the deliverable under the frozen acceptance criteria.
- `REJECT`: evidence available at cut-off positively supports failure of one or more frozen acceptance criteria.
- `DEFER`: evidence is insufficient or ambiguous for either action at that time.

`DEFER` is an experiment-review state, not an ACP job status.

If the frozen human intent is DEFER, do not manufacture a complete/reject action merely to obtain an economic transition.

## PayGod admission boundary

After the human intent is frozen:

```text
Requirement
+ predecessor state
+ pre-cutoff evidence
        ↓
representability
        ↓
evidence admission
        ↓
WITHHELD → NOT RUN
or
ADMIT → candidate shadow execution
```

No Virtuals-specific kernel behavior is permitted merely to make X1-RW-001 executable.

## Success conditions for the first workflow acquisition

X1-RW-001 counts as a successful Level 1 acquisition if:

- a real external provider accepted and performed the job;
- real ACP state and economic commitment existed;
- the requirement and provider deliverable were preserved;
- the pre-evaluator cut-off was frozen;
- the human native intent was frozen before PayGod output;
- the native outcome, if executed, was observable;
- all evidence limitations were recorded.

PayGod agreement is NOT required for Level 1 success.

## Stop conditions

Stop rather than repair the case if:

- the selected provider is not actually external;
- the job cannot be bound to the current rail;
- requirements or deliverable are unavailable at the cut-off;
- authenticated history cannot be preserved by the legitimate participant;
- evaluator identity cannot be established;
- executing the experiment would exceed the approved economic cap;
- the experiment would require a kernel change before evidence admission is tested.

A STOP result remains part of X1 evidence.
