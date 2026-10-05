# X1-RW-001 Evidence Capture Record

Status: EMPTY TEMPLATE

This record is populated from the real workflow. Empty fields are not evidence.

## Selection freeze

- freeze timestamp:
- current source pins:
- query used:
- eligible offerings returned:
- selected offering:
- selection reason under frozen rule:
- provider address:
- quoted price:
- economic cap:
- hook configuration:
- exclusions:

## Requirement commitment

- requirement artifact/reference:
- canonical bytes rule:
- SHA-256:
- create-job transaction:
- job id:
- creation block:
- creation block hash:

## Actors and native state

- client:
- provider:
- evaluator:
- evaluator non-zero:
- evaluator != provider:
- evaluator != client:
- ACP contract:
- implementation/proxy witness:
- payment token:
- budget:
- expiry:
- relevant hook:

## Provider submission

- submit transaction:
- submit block:
- submit block hash:
- native status after submission:
- deliverable reference:
- deliverable bytes preserved:
- deliverable SHA-256:
- authenticated history export preserved:
- history export SHA-256:

## Historical cut-off

- cutoff timestamp:
- cutoff anchor:
- evidence classified AVAILABLE_BEFORE_CUTOFF:
- evidence classified AFTER_CUTOFF:
- evidence classified UNPROVEN_AT_CUTOFF:

## Frozen human evaluator intent

- reviewer role:
- decision: COMPLETE | REJECT | DEFER
- freeze timestamp:
- evidence refs relied upon:
- acceptance criteria failed, if any:
- uncertainties:
- PayGod output visible before freeze: MUST BE NO

## Evidence Admission

- representability:
- withheld fields/claims:
- unrepresentable evidence:
- admission result: ADMIT | WITHHELD
- executability: EXECUTABLE | NOT_RUN
- reason:

## PayGod shadow

Populate only after human intent freeze and only if executable.

- run timestamp:
- policy/research contract reference:
- input commitment:
- decision:
- receipt commitment:
- bundle commitment:

## Native action

Populate only after the human native intent was already frozen.

- action: COMPLETE | REJECT | NONE
- transaction:
- block:
- block hash:
- successor native status:
- payout/refund transfers:

## Comparison

- human frozen intent:
- PayGod: NOT_RUN | decision
- native executed action:
- successor state:
- agreement status:
- primary diagnostic class:
- secondary notes:

Do not infer causal PayGod authority from temporal ordering in shadow mode.
