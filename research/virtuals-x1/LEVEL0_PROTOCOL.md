# X1 Level 0 Protocol — Research Freeze

Status: OPEN

Purpose: establish external facts and freeze the first current-rail experiment before observing PayGod outcomes.

## Current source references

- `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`

Current official SDK configuration identifies Base chain 8453 and ACP contract `0x238E541BfefD82238730D00a2208E5497F1832E0`.

Earlier modular ACP v2 references are retained as historical witnesses, not the default rail for new case acquisition.

A source constant is not proof of historical/live implementation identity. X1 must bind source/deployment state at sampled blocks before making stronger claims.

## Questions to resolve before freezing the first case sample

1. Independently confirm the current Base contract and its deployed implementation/proxy state.
2. Confirm the native current-rail transition semantics around SUBMITTED, COMPLETED, and REJECTED.
3. Determine which fields of `getJob`, transaction logs, and hook state are reconstructable at a historical block.
4. Determine exactly what evaluator identity/authority can be proved from native state.
5. Separate public on-chain evidence from participant-authenticated ACP history.
6. Define what requirement, deliverable, reason, and message evidence is available before evaluator action.
7. Define a cut-off that excludes information created after the evaluator decision.
8. Decide whether public historical cases can satisfy the evidence package.
9. If not, define a bounded real purchased workflow with an independent provider.
10. Freeze the candidate selection rule before observing PayGod outputs.

## Initial preferred transition

```text
SUBMITTED → COMPLETED
```

Requirements:

- current Node v2 rail;
- explicit non-zero evaluator;
- evidence available before evaluator action;
- economically consequential job where practical;
- no PayGod control of execution during the first comparison.

`SUBMITTED → REJECTED` remains a useful companion outcome but is not required for the first case.

## Required Level 0 exit artifacts

Level 0 does not close until the repository records:

- current-rail deployment inventory;
- chain/contract and implementation identity method;
- event/state reconstruction notes;
- target transition confirmation;
- public-vs-authenticated evidence boundary;
- historical cut-off definition;
- frozen candidate sampling rule;
- explicit exclusions;
- a statement of what cannot be observed or independently verified;
- no kernel change.

## Stop conditions

Pause X1 rather than coding around the problem if:

- current rail cannot be independently identified;
- target transition semantics cannot be pinned;
- the required pre-decision evidence cannot be obtained lawfully as observer/participant;
- a faithful predecessor snapshot cannot be reconstructed;
- the first useful experiment would require kernel mutation before observational evidence exists.

A Level 0 STOP is a valid research result.
