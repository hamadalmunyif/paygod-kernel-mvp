# X1 Level 0 Protocol — Research Freeze

Status: OPEN

Purpose: establish external facts and freeze the first experiment before observing PayGod outcomes.

## External reference

- protocol repository: `Virtual-Protocol/agent-commerce-protocol`
- initial observed commit: `7b490591b2162dbcebed7af47845cad2b0e29cc7`
- source license: MIT

The repository commit is a source-code reference only. It is not proof of a particular live deployment or upgrade state.

## Questions to resolve before acquiring cases

1. Which ACP deployment(s), chain(s), router addresses, and module addresses are live and relevant?
2. Which implementation identities are active for the upgradeable contracts at sampled blocks?
3. Can historical Job, Memo, payment, evaluator, and phase-transition state be reconstructed from native/public records?
4. Which transition path is evaluator-mediated in the live version?
5. What evidence is available before the evaluator decision, and what appears only after it?
6. Can the evidence cut-off be defined without relying on PayGod output?
7. Can a candidate sample be frozen before PayGod results are observed?
8. Can the same case be independently reconstructed from the pinned external state?
9. If historical cases are insufficient, can a bounded real service be purchased from an independent provider at low economic risk?

## Initial preferred transition

`EVALUATION → COMPLETED`, explicit non-zero evaluator only.

This remains provisional until the live deployment/version is verified.

## Required Level 0 exit artifacts

Level 0 does not close until the repository records:

- deployment inventory;
- chain and contract/module identity record;
- upgrade/implementation identity method;
- event/state reconstruction notes;
- target transition confirmation;
- evidence-cutoff definition;
- frozen candidate sampling rule;
- explicit exclusions;
- a statement of what is not observable;
- no kernel change.

## Stop conditions

Pause X1 rather than coding around the problem if:

- no live or reconstructable workflow can be verified;
- target transition semantics cannot be pinned;
- necessary evidence exists only after the decision;
- a faithful state snapshot cannot be reconstructed;
- the first useful experiment would require kernel mutation before observational evidence exists.

A Level 0 STOP is a valid research result.
