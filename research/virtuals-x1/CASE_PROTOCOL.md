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

## Evidence classification

Evidence is not forced into one mutually exclusive label. Each item is classified across separate dimensions.

### Source

One of:

- `PUBLIC_CHAIN`
- `AUTHENTICATED_ACP`
- `EXTERNAL_REFERENCE`
- `EXPERIMENT_RECORD`
- `UNKNOWN_SOURCE`

### Timing

One of:

- `PRE_CUTOFF`
- `POST_CUTOFF`
- `UNKNOWN_TIMING`

### Availability

One of:

- `AVAILABLE`
- `UNAVAILABLE`
- `UNPROVEN`

These dimensions are independent. For example, an evaluator transaction may be both `PUBLIC_CHAIN` and `POST_CUTOFF`; authenticated ACP history may be `AUTHENTICATED_ACP` and `UNAVAILABLE` if it was not successfully preserved.

Source class, timing, and availability do not establish truth, authenticity, or semantic admissibility.

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
4. create the native human/evaluator decision artifact without exposing the PayGod result;
5. canonicalize and commit that decision artifact before any PayGod evaluation by recording:
   - exact canonical artifact bytes or canonicalization rule;
   - SHA-256 digest;
   - immutable/versioned reference;
   - commitment timestamp/reference;
6. only after the native-decision commitment exists, perform PayGod mapping/admission and any shadow decision;
7. native evaluator action is executed according to the already-committed native decision;
8. observe the resulting transaction and successor state.

The native decision is not considered frozen merely because an editable field says COMPLETE or REJECT. The pre-PayGod commitment must make later alteration detectable.

## Native decision commitment

The committed artifact MUST contain at least:

- x1_case_id;
- evidence_cutoff_ref;
- native evaluator decision: COMPLETE | REJECT | HOLD-NO-ACTION;
- evaluator reason;
- evidence references relied upon;
- evaluator identity/role;
- decision timestamp;
- `paygod_output_visible_before_commit = false`.

The record MUST additionally preserve:

- artifact SHA-256;
- immutable or versioned artifact reference created before PayGod evaluation.

A Git commit/object, append-only evidence store entry, signed artifact, or equivalent versioned commitment is acceptable if the later comparison can prove that the committed bytes predate PayGod evaluation.

If this commitment cannot be produced, the case MUST NOT claim a blinded native comparison.

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

- native decision artifact reference;
- native decision artifact SHA-256;
- native decision commitment reference/time;
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
