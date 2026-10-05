# X1 Deployment Inventory — Preliminary

Status: PARTIAL — LEVEL 0
Observed: 2026-10-05
Purpose: establish external deployment facts before selecting or evaluating X1 cases.

This record distinguishes official source configuration, independently observable on-chain event sources, and unresolved deployment facts. It is not a claim that every observed contract is pinned to a specific source implementation at every historical block.

## Pinned upstream source repositories

| Repository | Pinned commit | Role |
| --- | --- | --- |
| `Virtual-Protocol/agent-commerce-protocol` | `7b490591b2162dbcebed7af47845cad2b0e29cc7` | Solidity protocol source |
| `Virtual-Protocol/acp-python` | `398241f6f132129b41cfadb20b3401a4f968b596` | Official Python SDK/config |
| `Virtual-Protocol/acp-cli` | `5c01771b964e0e431e6c4bea5a4d481514a30e24` | Current CLI/workflow surface |

## Official SDK configuration

The pinned `acp-python` configuration defines:

- chain: Base mainnet
- chain id: `8453`
- ACP v2 router: `0xa6C9BA866992cfD7fd6460ba912bfa405adA9df0`
- Base USDC: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- ACP API: `https://acpx.virtuals.io/api`
- default config: `BASE_MAINNET_CONFIG_V2`

Source:
`https://github.com/Virtual-Protocol/acp-python/blob/398241f6f132129b41cfadb20b3401a4f968b596/virtuals_acp/configs/configs.py`

The same SDK does not hard-code the principal v2 sub-manager addresses. `ACPContractClientV2` reads `jobManager()`, `memoManager()`, and `accountManager()` from the router at runtime.

Source:
`https://github.com/Virtual-Protocol/acp-python/blob/398241f6f132129b41cfadb20b3401a4f968b596/virtuals_acp/contract_clients/contract_client_v2.py`

Implication for X1: sub-manager identity must be snapshotted from external state for the relevant block/period rather than assumed from a timeless static configuration.

## Independently observable Base event sources

These addresses are supported by decoded BaseScan event records. They are useful Level 0 observations, but X1 still needs a reproducible method to bind each address and implementation identity to the sampled block.

| Observed address | Observed role/evidence | Level 0 status |
| --- | --- | --- |
| `0x9c690c267f20c385f8a053f62bc8c7e2d4b83744` | emits `JobCreated`, `BudgetSet`, `JobPhaseUpdated` | observed JobManager event source |
| `0x9c6c5a7125934cc6a711a7bf44f3cdcccf91f30c` | emits `NewMemo`, `MemoSigned`, `PayableMemoExecuted` | observed MemoManager event source |
| `0x14dab2b846a4c07b3f52c37e3fd7265c2bcdf485` | emits `AccountJobCountUpdated` | observed AccountManager candidate |
| `0xEF4364Fe4487353dF46eb7c811D4FAc78b856c7F` | emits `PaymentReleased`; is source of USDC transfers on completion | observed PaymentManager candidate |

Example BaseScan records:

- `https://basescan.org/tx/0xdea8b0aee5692ecf3f5794b1f7bf5a7c2153bd51269280b3ac29e1f157eba0b2`
- `https://basescan.org/tx/0x369363a969500904360b1f2bb02c837acf4f0cb059238a929bb372edc3d1a17c`
- `https://basescan.org/tx/0x3ad11b52551db0be23b058861cfb2b31b8e28bb2fd9e4dffec942e4704152e2d`

## Upgradeability boundary

The pinned protocol source uses upgradeable contracts/modules. Therefore an address alone is insufficient for historical X1 binding.

For every future sampled case, X1 must bind at minimum:

- chain id;
- block number and block hash;
- router address;
- relevant manager addresses;
- implementation identity or an equivalent reproducible proxy-state witness at that block;
- source/version relationship only when it can be demonstrated.

A current source repository commit MUST NOT be treated as proof that a historical transaction executed that exact implementation.

## Still unresolved

Level 0 remains open because the following are not yet frozen:

- a reproducible proxy/implementation identity method for historical sampled blocks;
- authoritative block-bound AccountManager and PaymentManager binding;
- AssetManager identity where relevant;
- a live candidate sampling window;
- a complete job reconstruction method from creation through evaluation/completion;
- which off-chain memo content is publicly retrievable and stable at historical cut-off;
- whether the ACP API exposes sufficient historical metadata without authenticated/private context.

No PayGod code change is authorized by this inventory.
