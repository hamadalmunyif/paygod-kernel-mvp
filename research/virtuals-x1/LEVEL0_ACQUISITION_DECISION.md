# X1 Level 0 Acquisition Decision

Status: PROVISIONAL — LIVE PURCHASE NOT YET AUTHORIZED  
Decision date: 2026-10-05  
Scope: current ACP Node v2 rail on Base

## Finding

Public on-chain data is sufficient to observe native job state, roles, lifecycle events, deliverable commitments, and settlement.

It is not sufficient by itself to prove the complete evidence basis visible to an evaluator.

The current `acp-node-v2` transport retrieves job-room history only after agent authentication. Requirements, messages, and other evaluator-visible context can therefore be participant-scoped.

That creates a hard X1 boundary:

```text
public chain history
≠ complete evaluator evidence package
```

A historical public job may be a useful external witness while remaining non-qualifying for a PayGod comparison.

## Decision

The preferred route to the first fully reconstructable X1 workflow is a **prospective bounded real ACP job** in which X1 is a legitimate participant and the provider is independent.

This decision selects the acquisition method only. It does not authorize spending, wallet creation, agent creation, or transaction submission.

## First real workflow class

The first live workflow SHOULD be:

- current ACP Node v2 rail;
- Base mainnet, chain id `8453`;
- explicit non-zero evaluator;
- independent external provider;
- objectively checkable requirement/deliverable where practical;
- low economic exposure;
- no custom settlement hook unless required by the chosen offering;
- complete participant-visible history captured prospectively;
- PayGod shadow-only;
- provider and evaluator must not see the PayGod result before the native evaluator decision is frozen.

## R0 instrumentation case

The first real job is classified:

`X1-R0 — instrumentation case`

Its purpose is to prove that the complete external state/evidence capture method works.

R0 does **not** establish protocol independence or production value by itself and does not justify a kernel change.

If R0 succeeds, X1 may freeze a later multi-case validation sample before observing those PayGod outputs.

## Required pre-purchase freeze

Before any live purchase, record:

1. provider/offering selection criteria;
2. exact requirement schema or acceptance criteria;
3. maximum approved economic exposure;
4. client address;
5. evaluator address and relationship to client;
6. evidence capture plan;
7. pre-decision cut-off procedure;
8. human/native evaluator decision-freeze procedure;
9. PayGod shadow policy and mapping;
10. what counts as WITHHELD / NOT RUN;
11. retention of all candidate outcomes, including failure/expiry/rejection;
12. explicit non-claims.

## Spending gate

Maximum approved economic exposure is currently:

`UNSET — EXPLICIT USER APPROVAL REQUIRED`

No USDC transfer, job creation, wallet funding, or paid provider engagement is authorized by this record.

## Stop-build

This acquisition decision does not authorize:

- an ACP adapter in the kernel;
- new PayGod semantics;
- new receipt/schema semantics;
- conditional-release code;
- post-flight conformance code;
- automatic payment control.

Observe first. Build only after a separately recorded witness justifies it.
