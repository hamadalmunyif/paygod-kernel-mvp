# X1 Deployment Inventory — Preliminary

Status: PARTIAL — LEVEL 0
Observed: 2026-10-05
Purpose: establish external deployment facts before selecting or evaluating X1 cases.

This record now distinguishes two ACP generations that MUST NOT be conflated:

1. the **current ACP Node v2 / AgenticCommerceV3 rail** used by the current official Node SDK/CLI; and
2. the **earlier modular ACP v2 rail** used by the older Python SDK and represented by the separate `agent-commerce-protocol` repository.

Discovery of this version/deployment split is itself a Level 0 finding: source, deployment, lifecycle, and case evidence must be pinned before PayGod comparison.

## Pinned upstream references

| Repository | Pinned commit | X1 role |
| --- | --- | --- |
| `Virtual-Protocol/acp-node-v2` | `0f4b678516c354c1541b92aa08db11ece3506261` | current Node v2 SDK, current EVM ABI/address registry, current workflow semantics |
| `Virtual-Protocol/acp-cli` | `5c01771b964e0e431e6c4bea5a4d481514a30e24` | current CLI and job-history/workflow surface |
| `Virtual-Protocol/agent-commerce-protocol` | `7b490591b2162dbcebed7af47845cad2b0e29cc7` | earlier modular Solidity ACP v2 source; historical reference |
| `Virtual-Protocol/acp-python` | `398241f6f132129b41cfadb20b3401a4f968b596` | older modular ACP v2 Python SDK/config; historical reference |

## Current X1 target rail — ACP Node v2 / AgenticCommerceV3

The pinned `acp-node-v2` source registry defines for Base mainnet:

- chain id: `8453`
- ACP contract: `0x238E541BfefD82238730D00a2208E5497F1832E0`
- Base USDC: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- ACP server: `https://api.acp.virtuals.io`

Source:
`Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261/src/core/constants.ts`

The pinned EVM ABI identifies this contract surface as `AgenticCommerceV3` and exposes:

- `createJob`
- `setBudget`
- `fund`
- `submit`
- `complete`
- `reject`
- `claimRefund`
- `getJob`

It also exposes `JobCreated`, `JobFunded`, `JobSubmitted`, `JobCompleted`, `JobRejected`, `PaymentReleased`, and `Upgraded` events.

The SDK's on-chain status enum is:

- OPEN = 0
- FUNDED = 1
- SUBMITTED = 2
- COMPLETED = 3
- REJECTED = 4
- EXPIRED = 5

The current CLI adds a derived/off-chain `budget_set` status from the event/history transport. X1 MUST therefore distinguish protocol-native on-chain job status from the richer SDK/transport lifecycle.

## Current evaluator boundary

The current Node v2 SDK exposes role-gated tools:

- provider / funded → `submit`
- evaluator / submitted → `complete` or `reject`

The preferred first current-rail X1 transition is therefore:

```text
on-chain: SUBMITTED → COMPLETED
SDK/transport: submitted → completed
action: complete(jobId, reason, optParams)
```

with an explicit non-zero evaluator.

This SDK role gating is useful evidence about the intended workflow. X1 still requires independent binding to the deployed contract semantics before treating SDK behavior alone as proof of on-chain authorization.

## Authenticated off-chain history boundary

The current Node v2 transport's `getHistory(chainId, jobId)` first authenticates the agent by signing an `acp-auth:<timestamp>` message, then calls:

`/chats/{chainId}/{jobId}/history`.

Therefore X1 MUST NOT assume that full requirements, messages, or deliverables for arbitrary historical jobs are publicly reconstructable.

This creates two evidence zones for X1:

- public/native chain evidence: contract state, transactions, logs, commitments;
- participant-authorized ACP history: requirements/messages/deliverable context available to an authenticated participant.

This is a strong reason to prefer a deliberately created, bounded real job if public historical cases cannot supply a faithful pre-decision evidence package.

## Current hook surface observed in the pinned SDK

Base mainnet registry entries include:

- FundTransferHook: `0x0EaD25150985Bce0B4925c54E4ee1D856381A86B`
- MultiHookRouter: `0x77F67252a8d3A6b049f4383FD50Fb9Bf784D29D1`
- SubscriptionHook: `0xD087363615f36F2b0265Bb4AC78Cd730C6C0cc1D`
- SubscriptionState: `0x52c2C68f4f7fF3C70760E3D0B9b2FA91CFE443Ad`

These are configuration observations, not X1 requirements. The first experiment SHOULD avoid unnecessary hook complexity unless the selected real offering requires it.

## Earlier modular ACP v2 — historical rail

The older pinned `acp-python` configuration defines:

- Base chain id: `8453`
- modular ACP v2 router: `0xa6C9BA866992cfD7fd6460ba912bfa405adA9df0`
- older API: `https://acpx.virtuals.io/api`

The older client reads JobManager/MemoManager/AccountManager addresses dynamically from that router. Public decoded Base records also exposed modular manager activity associated with that generation.

This rail is retained only for historical/external-witness analysis. It is NOT the default target for new X1 workflow acquisition.

## Historical modular event sources observed

| Observed address | Observed role/evidence | X1 treatment |
| --- | --- | --- |
| `0x9c690c267f20c385f8a053f62bc8c7e2d4b83744` | `JobCreated`, `BudgetSet`, `JobPhaseUpdated` | historical modular JobManager event source |
| `0x9c6c5a7125934cc6a711a7bf44f3cdcccf91f30c` | `NewMemo`, `MemoSigned`, `PayableMemoExecuted` | historical modular MemoManager event source |
| `0x14dab2b846a4c07b3f52c37e3fd7265c2bcdf485` | `AccountJobCountUpdated` | historical modular AccountManager candidate |
| `0xEF4364Fe4487353dF46eb7c811D4FAc78b856c7F` | `PaymentReleased`; USDC source on completion | historical modular PaymentManager candidate |

## Upgradeability / source-binding boundary

Both the current ABI and the earlier modular source expose upgradeability concerns. An address or SDK constant alone is insufficient to prove historical implementation identity.

For every future sampled X1 case, bind as far as the external system permits:

- chain id;
- block number and block hash;
- ACP contract address;
- implementation/proxy identity at that block where applicable;
- job id;
- client/provider/evaluator;
- native job status before action;
- relevant hook configuration;
- budget/payment token;
- evidence commitments available before the evaluator action.

A current repository commit MUST NOT be treated as proof that a historical transaction executed that exact source.

## Still unresolved

Level 0 remains open because X1 still needs:

- independent current-rail on-chain binding for `0x238E541BefD82238730D00a2208E5497F1832E0` at sampled blocks;
- a reproducible historical proxy/implementation identity method;
- a frozen current-rail candidate sampling rule;
- a complete current job reconstruction method;
- a decision on whether public historical evidence is sufficient or a participant-controlled real job is required;
- an explicit evidence cut-off for authenticated ACP chat/history material;
- a statement of which off-chain evidence is mutable, unavailable, or unverifiable outside ACP.

No PayGod code change is authorized by this inventory.
