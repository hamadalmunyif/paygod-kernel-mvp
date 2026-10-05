# X1 Level 0 Protocol — Research Freeze

Status: OPEN

Purpose: establish external facts and freeze the first experiment before observing PayGod outcomes.

## Primary current references

- current runtime SDK: `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- current CLI: `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`
- Base mainnet chain id: `8453`
- current SDK Base ACP core: `0x238E541BfefD82238730D00a2208E5497F1832E0`

Historical/legacy references are recorded separately in `VERSION_BOUNDARY.md`.

A repository commit or SDK constant is a source/config reference. It is not by itself proof of the implementation that executed a historical transaction.

## Current preferred transition

`SUBMITTED → COMPLETED`, explicit non-zero evaluator only.

The pinned current SDK defines the on-chain JobStatus values as OPEN=0, FUNDED=1, SUBMITTED=2, COMPLETED=3, REJECTED=4, EXPIRED=5.

The CLI's `budget_set` label is a derived workflow status and is not a separate current on-chain JobStatus value.

## Questions to resolve before acquiring the frozen comparison sample

1. What proxy/implementation identity was active for the ACP core at each sampled block?
2. Can `JobCreated`, `BudgetSet`, `JobFunded`, `JobSubmitted`, and `JobCompleted/Rejected` be reconstructed reliably from public chain data?
3. Can the client, provider, evaluator, expiry, hook, budget, description, and deliverable commitment be reconstructed at the predecessor block?
4. Which evidence is public on-chain, which evidence is only in authenticated ACP job-room history, and which evidence is unavailable?
5. Can the evaluator's evidence cut-off be defined before completion/rejection without using later state?
6. Can a candidate population be frozen before PayGod output is observed?
7. Can a second independent reconstruction of the same case reproduce the same decision-relevant snapshot?
8. Can explicit non-zero-evaluator jobs be located in sufficient number?
9. If historical public cases do not expose the full evidence basis, can a bounded real service be purchased from an independent provider while capturing requirements, messages, deliverable, and evaluator-visible evidence prospectively?
10. Can all of the above be done without kernel mutation?

## Evidence-surface rule

Do not treat the authenticated ACP API/chat history as equivalent to public chain evidence.

The current SDK's `getHistory(chainId, jobId)` authenticates to the ACP server before retrieving room history.

For every X1 case, record each evidence item as one of:

- PUBLIC_CHAIN;
- AUTHENTICATED_ACP;
- EXTERNAL_REFERENCE;
- UNAVAILABLE;
- POST_DECISION.

Only evidence demonstrably available at the frozen decision cut-off may enter Evidence Admission.

## Required Level 0 exit artifacts

Level 0 does not close until the repository records:

- current runtime/version boundary;
- deployment/core identity record;
- proxy/implementation identity method;
- event/state reconstruction notes;
- target transition confirmation;
- evidence-surface classification;
- evidence-cutoff definition;
- frozen candidate sampling rule;
- explicit exclusions, including evaluator-zero auto-completion;
- a statement of what is not observable;
- no kernel change.

## Stop conditions

Pause X1 rather than coding around the problem if:

- the current runtime/deployment cannot be pinned;
- the target transition semantics cannot be bound to the sampled deployment;
- necessary evidence exists only after the decision;
- a faithful predecessor snapshot cannot be reconstructed;
- historical cases require private evidence that cannot be accessed or captured prospectively;
- the first useful experiment would require kernel mutation before observational evidence exists.

A Level 0 STOP is a valid research result.
