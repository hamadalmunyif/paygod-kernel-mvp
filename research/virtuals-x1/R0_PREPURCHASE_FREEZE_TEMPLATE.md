# X1-R0 Pre-Purchase Freeze Template

Status: NOT YET COMPLETE  
Use: complete this record from the live current ACP offering immediately before any real job is created.

## Provider

- provider name:
- provider wallet:
- ACP agent id / URL:
- independent from PayGod/X1 operator: yes/no
- prior activity observed:
- current offering object captured at:

## Offering

- offering name:
- current price:
- SLA:
- requirement schema:
- deliverable description/schema:
- required funds/hook:
- chain:
- offering commitment/hash:

## Frozen request

- exact requirement payload:
- requirement commitment:
- reason this payload was selected:

The payload MUST be selected before provider output is observed.

## Frozen acceptance criteria

Acceptance criteria must be objective enough to apply before seeing the deliverable.

For a structured data offering, criteria SHOULD separate:

### Contract/shape criteria

- response is parseable in the advertised format;
- required advertised fields are present where applicable;
- requested filter is respected;
- result count does not exceed the frozen limit;
- no undisclosed execution action is required.

### External factual cross-check

If a public external source is used, record:

- source:
- retrieval time:
- matching rule:
- tolerance/known publication lag:
- whether cross-check is required for native evaluator decision or only diagnostic.

Do not silently turn source disagreement into FALSE unless the frozen rule says exactly how it is interpreted.

## Actors

- client address:
- evaluator address:
- evaluator relationship to client:
- provider address:

Evaluator MUST be explicit and non-zero for the intended R0 decision boundary.

## Economic authorization

- listed service price:
- estimated transaction/platform overhead:
- maximum total approved exposure:
- approval record/reference:

If maximum total approved economic exposure is blank, **STOP**.

## Evidence capture

Before evaluator action capture and commit:

- job creation tx/block;
- current implementation/proxy witness;
- JobCreated/native job state;
- requirement message;
- budget/funding state;
- provider submission tx/block;
- deliverable/reference;
- authenticated job-room history visible to participant;
- external references allowed by the frozen policy;
- cut-off block/time;
- evidence-package digest.

For each preserved evidence item also record independent classification dimensions:

- source: PUBLIC_CHAIN | AUTHENTICATED_ACP | EXTERNAL_REFERENCE | EXPERIMENT_RECORD | UNKNOWN_SOURCE;
- timing: PRE_CUTOFF | POST_CUTOFF | UNKNOWN_TIMING;
- availability: AVAILABLE | UNAVAILABLE | UNPROVEN.

## Decision freeze

Before any PayGod evaluation, create a native decision artifact containing:

- x1_case_id:
- evidence cut-off reference:
- native evaluator decision: COMPLETE / REJECT / HOLD-NO-ACTION
- native evaluator reason:
- evidence refs relied upon:
- evaluator identity/role:
- decision timestamp:
- PayGod output visible before commitment: MUST BE NO

Then preserve and record:

- canonicalization rule or exact committed bytes:
- native decision artifact SHA-256:
- immutable/versioned native decision artifact reference:
- native decision commitment reference:
- native decision commitment time:

**STOP** if the native decision is only stored in an editable field without a digest and immutable/versioned commitment that predates PayGod evaluation.

Only after this commitment exists may the X1 PayGod shadow mapping/admission begin.

## PayGod shadow

- representability:
- evidence admission:
- WITHHELD fields:
- executable:
- PayGod run:
- PayGod decision:
- receipt/bundle refs if run:
- PayGod run artifact reference:
- PayGod run artifact SHA-256:
- PayGod run commitment reference:
- shared chronology reference:

If PayGod runs, its output artifact MUST reference the native decision commitment and be committed after it in the same append-only/versioned chronology.

Required recorded order:

```text
evidence package commitment
→ native decision commitment
→ PayGod run commitment
→ native ACP action / successor observation
```

The shared chronology demonstrates recorded ordering only. It does not constitute trusted external time.

**STOP** if the chronology cannot substantiate that the native decision commitment precedes the PayGod run commitment.

## Native execution / outcome

Execute only the already-committed native evaluator decision.

Record:

- native action tx:
- successor state:
- settlement outcome:
- post-decision evidence kept separate:

## Comparison / diagnosis

- comparison applicable:
- native decision commitment verified:
- PayGod run commitment verified:
- chronology order verified:
- agreement/disagreement:
- primary diagnostic class:
- operational importance:
- candidate architecture implication:
- kernel change authorized: NO
