# X1 Deployment Inventory — Preliminary

Status: PARTIAL — LEVEL 0
Observed: 2026-10-05
Purpose: establish the current external runtime before selecting or evaluating X1 cases.

## Level 0 finding: version boundary

Initial X1 research started from the older modular ACP repository and Python SDK.

Further review of the current official CLI showed that its default v2 flow is powered by `acp-node-v2` and a different current on-chain core.

This distinction is now mandatory for X1.

See `VERSION_BOUNDARY.md`.

## Current primary runtime

Pinned upstream references:

| Repository | Pinned commit | Role |
| --- | --- | --- |
| `Virtual-Protocol/acp-node-v2` | `0f4b678516c354c1541b92aa08db11ece3506261` | current Node v2 runtime/ABI/config |
| `Virtual-Protocol/acp-cli` | `5c01771b964e0e431e6c4bea5a4d481514a30e24` | current CLI/workflow surface |

The pinned `acp-node-v2` constants define:

- Base mainnet chain id: `8453`
- ACP core: `0x238E541BfefD82238730D00a2208E5497F1832E0`
- Base USDC: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- ACP server: `https://api.acp.virtuals.io`

Source:
`Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261/src/core/constants.ts`

The current ABI calls the deployed core `AgenticCommerceV3` and exposes `JobCreated`, `BudgetSet`, `JobFunded`, `JobSubmitted`, `JobCompleted`, `JobRejected`, `PaymentReleased`, and `Upgraded`.

The current SDK JobStatus enum is:

- OPEN = 0
- FUNDED = 1
- SUBMITTED = 2
- COMPLETED = 3
- REJECTED = 4
- EXPIRED = 5

## Current evidence transport

The current runtime has two distinct evidence surfaces:

### Public/native chain surface

The core contract records job roles/state, job lifecycle events, deliverable commitment, and settlement events.

### Authenticated ACP room surface

The current SDK retrieves job-room history through authenticated HTTP/SSE transport.

`getHistory(chainId, jobId)` calls the ACP server only after agent authentication.

Therefore public transaction history alone may be insufficient to reconstruct the evaluator's full evidence basis.

This is a central X1 Level 0 question, not an implementation defect.

## Historical / legacy modular path

Pinned historical references:

| Repository | Pinned commit | Observed role |
| --- | --- | --- |
| `Virtual-Protocol/agent-commerce-protocol` | `7b490591b2162dbcebed7af47845cad2b0e29cc7` | modular ACPRouter/manager source reference |
| `Virtual-Protocol/acp-python` | `398241f6f132129b41cfadb20b3401a4f968b596` | older Python SDK/config |

The pinned older Python SDK configured Base router:

`0xa6C9BA866992cfD7fd6460ba912bfa405adA9df0`

and resolved JobManager/MemoManager/AccountManager dynamically from that router.

Public Base event records observed during the first X1 pass included:

- `0x9c690c267f20c385f8a053f62bc8c7e2d4b83744` — JobManager-like events;
- `0x9c6c5a7125934cc6a711a7bf44f3cdcccf91f30c` — MemoManager-like events;
- `0x14dab2b846a4c07b3f52c37e3fd7265c2bcdf485` — AccountManager candidate;
- `0xEF4364Fe4487353dF46eb7c811D4FAc78b856c7F` — payment-release candidate.

These are retained as a historical/legacy witness set only. They are not the primary current X1 runtime.

## Upgradeability boundary

The current Base core is represented as upgradeable in the current ABI/source surface. An address alone is not enough for a historical X1 case.

For every future sampled case, X1 must bind:

- chain id;
- block number and block hash;
- core/proxy address;
- implementation identity or equivalent reproducible proxy-state witness at that block;
- relevant hook addresses;
- source/version relationship only when demonstrated.

A current SDK/repository commit MUST NOT be treated as proof that a historical transaction executed that exact implementation.

## Still unresolved

Level 0 remains open because the following are not yet frozen:

- a reproducible historical proxy/implementation identity method;
- a frozen current-runtime candidate sampling window;
- sufficient explicit non-zero-evaluator jobs;
- full predecessor-state reconstruction;
- exact public-vs-authenticated evidence availability at cut-off;
- whether historical authenticated room evidence can be retrieved without participating in the job;
- whether a prospective bounded real job is required to capture a complete evidence basis.

No PayGod code change is authorized by this inventory.
