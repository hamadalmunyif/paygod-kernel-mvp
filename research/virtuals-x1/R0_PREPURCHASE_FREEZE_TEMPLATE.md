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

If maximum total approved exposure is blank, **STOP**.

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

## Decision freeze

Before PayGod evaluation:

- native evaluator decision: COMPLETE / REJECT / HOLD-NO-ACTION
- native evaluator reason:
- decision artifact/reference:
- decision frozen at:
- PayGod output visible before freeze: MUST BE NO

Only after this block is frozen may the X1 PayGod shadow mapping/admission begin.

## PayGod shadow

- representability:
- evidence admission:
- WITHHELD fields:
- executable:
- PayGod run:
- PayGod decision:
- receipt/bundle refs if run:

## Native execution / outcome

Execute only the already-frozen native evaluator decision.

Record:

- native action tx:
- successor state:
- settlement outcome:
- post-decision evidence kept separate:

## Comparison / diagnosis

- comparison applicable:
- agreement/disagreement:
- primary diagnostic class:
- operational importance:
- candidate architecture implication:
- kernel change authorized: NO
