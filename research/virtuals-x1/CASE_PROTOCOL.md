# X1 Case Protocol — Current ACP Rail

Status: DRAFT FROZEN METHOD FOR R0  
Applies to: current ACP Node v2 / AgenticCommerceV3 rail

## Target transition

Primary transition:

`SUBMITTED → COMPLETED`

with explicit non-zero evaluator.

Companion outcomes may include `SUBMITTED → REJECTED`, expiry, or NOT RUN, but they must not be deleted or replaced merely because they are inconvenient.

## Case identity

Every candidate case records:

- x1_case_id;
- chain_id;
- ACP contract address;
- proxy/implementation identity when reproducibly available;
- creation block/tx;
- submission block/tx;
- evaluator-action block/tx;
- job_id;
- client;
- provider;
- evaluator;
- hook;
- budget;
- payment token;
- expiry;
- offering/service identifier where available.

## Evidence surfaces

Each evidence item is classified exactly once as:

- `PUBLIC_CHAIN`
- `AUTHENTICATED_ACP`
- `EXTERNAL_REFERENCE`
- `POST_DECISION`
- `UNAVAILABLE`

Evidence source class is separate from evidence truth.

## Pre-decision cut-off

For a prospective R0 case:

1. wait until the provider has submitted and the native job is in `SUBMITTED`;
2. before the evaluator executes `complete` or `reject`, capture:
   - current chain/block reference;
   - current job state;
   - participant roles;
   - job-room history then visible to the participant;
   - requirement;
   - deliverable/reference;
   - any external references permitted by the frozen criteria;
3. hash/commit the captured evidence package;
4. freeze the native human/evaluator decision without exposing the PayGod result;
5. only then perform PayGod mapping/admission and shadow decision;
6. native evaluator action is executed according to the already-frozen native decision;
7. observe the resulting transaction and successor state.

This ordering prevents PayGod output from contaminating the native comparison decision.

## Evidence Admission

For each PayGod-relevant claim:

```text
source fact
→ semantic representability
→ temporal/provenance admission
→ admitted value | WITHHELD
```

If a required frozen input cannot be assigned without inference or coercion:

`WITHHELD → NOT RUN`

NOT RUN is not a PayGod verdict.

## Comparison record

Only if PayGod runs, record:

- frozen native evaluator decision;
- PayGod shadow decision;
- agreement/disagreement;
- decision reasons;
- actual ACP transaction;
- actual successor state;
- economic settlement outcome.

If PayGod does not run, comparison is N/A.

## Diagnosis

Any material difference is classified only after evidence review.

Allowed primary diagnostic classes begin with the existing PayGod taxonomy where applicable:

- policy_ambiguity
- missing_evidence
- human_error
- contract_gap
- provenance_gap
- kernel_defect
- out_of_contract_scope

X1 may add an external-protocol-specific diagnostic only through a later explicit protocol update; do not improvise new classes case by case.

## Non-claims

A single R0 case cannot prove:

- protocol independence;
- market demand;
- evaluator quality;
- external evidence truth;
- PayGod causal authority;
- post-flight conformance;
- next-transition eligibility;
- production readiness.
