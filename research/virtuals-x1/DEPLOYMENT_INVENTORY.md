# X1 Deployment Inventory — Level 0

Status: LEVEL 0 DEPLOYMENT BINDING CAPTURED — R0 SPEND STILL UNAUTHORIZED  
Observed/reconciled: 2026-10-05  
Purpose: establish external deployment facts and preserve the exact remaining boundary before Level 1 acquisition.

This record distinguishes two ACP generations that MUST NOT be conflated:

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

The preferred first current-rail X1 transition is:

```text
on-chain: SUBMITTED → COMPLETED
SDK/transport: submitted → completed
action: complete(jobId, reason, optParams)
```

with an explicit non-zero evaluator.

`CURRENT_RUNTIME_WITNESS_001.md` separately records a real current-rail job that submitted, completed, and released payment with evaluator = zero. That witness is intentionally excluded from evaluator-mediated comparison and establishes that `COMPLETED` alone does not prove evaluator judgment.

SDK role gating remains evidence about intended workflow. X1 still requires block-bound deployment identity and must not promote SDK behavior alone into a stronger historical on-chain authorization claim.

## Authentication-gated off-chain history boundary

The current Node v2 transport's `getHistory(chainId, jobId)` first authenticates the agent by signing an `acp-auth:<timestamp>` message, then calls:

`/chats/{chainId}/{jobId}/history`.

Established:

- history retrieval is authentication-gated in the pinned client;
- arbitrary public reconstructability of requirements/messages/deliverables MUST NOT be assumed.

Not established:

- whether every authenticated agent may read every job;
- whether access is restricted to job participants;
- the exact authorization result for an unrelated job.

Therefore this inventory uses **authenticated ACP history**, not **participant-authorized history**, unless a specific access test proves the narrower scope.

For the prospective R0 path selected in `LEVEL0_ACQUISITION_DECISION.md`, X1 will operate as a legitimate participant and preserve the history actually available to that participant. Authorization scope for unrelated jobs is not required to be guessed.

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

An address or SDK constant alone is insufficient to prove implementation identity at a sampled block.

The reproducible method is now frozen in `DEPLOYMENT_BINDING_METHOD.md`.

For every qualifying current-rail case it requires, at the sampled predecessor block:

- chain id;
- block number and block hash;
- ACP proxy address;
- ERC-1967 implementation-slot response;
- recovered implementation address;
- proxy bytecode and hash;
- implementation bytecode and hash;
- raw evidence references.

A current repository commit MUST NOT be treated as proof that a historical transaction executed that exact source.

## External corroboration — non-qualifying research lead

A 2026-09-24 independent technical analysis of AgenticCommerceV3 reports that the same Base address is a UUPS proxy, gives deployment block `44,427,013`, describes an implementation abbreviated as `0x8e86…77bc`, and reports no observed upgrade.

Reference:
`https://llm4agents.com/blog/erc-8183-agentic-commerce-job-escrow-audit`

X1 does NOT promote those statements into deployment facts merely because they are plausible and independently published.

They remain corroborating research leads only. The independent block-bound witness is now captured separately; the external analysis is not promoted into source-equivalence or upgrade-history proof.

## Level 0 status reconciliation

### Resolved / frozen

The repository now records:

- current rail and source pins;
- current ACP contract candidate from official SDK configuration;
- target transition `SUBMITTED → COMPLETED` with explicit non-zero evaluator;
- a current-runtime exclusion witness showing why evaluator = zero does not qualify;
- public/native-chain vs authentication-gated ACP evidence separation;
- a prospective bounded real job as the preferred first fully reconstructable path;
- pre-purchase provider/offering selection controls;
- evidence cut-off and Evidence Admission ordering;
- native-decision commitment before PayGod;
- PayGod-run commitment after the native decision in a common recorded chronology;
- independent evidence source/timing/availability classification;
- a machine-readable case register;
- a reproducible ERC-1967 deployment-binding method;
- no kernel/pack/schema/receipt/ledger mutation.

### Level 0 deployment witness — captured

The frozen method was executed and then re-executed against the exact pinned reference block:

```text
chain_id = 8453
block_number = 52189048
block_hash = 0x565c9c7f6ac17d383f14c8453c1d369c0ffb55a2afcbe31d55c5daa39bf55151
proxy = 0x238E541BfefD82238730D00a2208E5497F1832E0
implementation = 0x8e86fbef4a4c927561cb6447ced77fffbf3b77bc
proxy_keccak256 = 0xfc16c7f571d8b1443fb5ef7a46304acb87f7a1f6d065d9d3162ec0af13f42aae
implementation_keccak256 = 0xc47c1f4ca03bd0be464d0a94eb2b6e4c9c112306b42b22d8400b8dada47848b5
```

Canonical material is preserved under `witnesses/DEPLOYMENT_WITNESS_001/`.

The reference deployment-binding blocker is therefore closed. This does not authorize spending and does not replace case-specific binding at the real R0 predecessor block.

### Unresolved but not required to guess before prospective R0

These remain explicit limitations rather than silently inferred facts:

- exact authorization scope of authenticated ACP history for unrelated jobs;
- full reconstructability of arbitrary historical job-room evidence;
- historical implementation identity for the old modular witness beyond evidence already recorded;
- source-code equivalence to deployed implementation unless separately reproduced.

Case-specific deployment binding MUST be repeated at the real R0 predecessor block even after the Level 0 reference witness succeeds.

No paid action is authorized by this inventory.
No PayGod code change is authorized by this inventory.
