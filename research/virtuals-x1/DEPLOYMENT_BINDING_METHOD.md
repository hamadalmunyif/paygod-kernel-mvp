# X1 Deployment Binding Method — Current ACP Rail

Status: FROZEN METHOD — EXECUTION WITNESS STILL REQUIRED  
Applies to: Base mainnet / current ACP Node v2 / AgenticCommerceV3  
Chain id: `8453`  
Current ACP proxy candidate: `0x238E541BfefD82238730D00a2208E5497F1832E0`

## Purpose

Define a reproducible method for binding an X1 case to the contract code that existed at a specific Base block.

This method exists because:

```text
SDK constant
≠ deployed proxy identity
≠ implementation identity at block B
≠ deployed bytecode/source equivalence
```

A current SDK commit MUST NOT be used as a substitute for an on-chain deployment witness.

## Required block anchor

For every qualifying current-rail X1 case, choose a block `B` at or immediately before the predecessor-state/evidence cut-off.

Record:

- chain id;
- block number `B`;
- block hash `H(B)`;
- ACP proxy address;
- block timestamp as chain metadata only.

The block timestamp is not an independent trusted time authority.

## ERC-1967 implementation read

For an ERC-1967/UUPS candidate, read the implementation storage slot at block `B`:

`0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`

This is the ERC-1967 logic-contract slot:

`bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1)`

Preserve the raw request and raw response.

Interpret the implementation address only from the returned storage word. Do not copy it from an explorer label or SDK source.

If the implementation slot is zero, do not guess. Check whether the deployment uses the ERC-1967 beacon slot and document that branch explicitly before proceeding.

## Bytecode binding

At the same block `B`, retrieve code for:

1. the ACP proxy address;
2. the implementation address recovered from the storage slot.

Preserve:

- raw proxy bytecode;
- proxy bytecode hash;
- raw implementation bytecode;
- implementation bytecode hash.

The hash algorithm and exact bytes MUST be recorded. X1 SHOULD use Keccak-256 for EVM bytecode identity and may additionally record SHA-256 for artifact packaging.

A non-empty implementation slot without implementation bytecode at `B` is a failed binding.

## Upgrade corroboration

Query `Upgraded(address)` events up to block `B` when available.

Events are corroborating evidence. The storage-slot value at `B` is the case-binding value.

Do not infer "never upgraded" merely because an explorer UI does not show an upgrade.

## Source/ABI relationship

Verified source, explorer ABI, and pinned SDK ABI may be retained as separate evidence.

They do not become equivalent merely because names match.

A stronger source-equivalence claim requires a reproducible compiler/settings/metadata or bytecode comparison. Until then X1 may claim only:

- proxy bytecode identity at `B`;
- implementation bytecode identity at `B`;
- observed callable/event surface where independently decoded.

## Minimum deployment witness

A deployment witness is complete only when it contains:

```text
chain_id = 8453
block_number = B
block_hash = H(B)

proxy_address
implementation_slot
raw_slot_value
implementation_address

proxy_code
proxy_code_hash
implementation_code
implementation_code_hash

raw evidence references
method/version
limitations
```

## Case repetition

A Level 0 reference-block witness proves only that the method works and identifies the deployment at that reference block.

Every real X1 case MUST repeat the binding at its own sampled predecessor block. Do not inherit an implementation identity from a prior case.

## Failure semantics

If X1 cannot recover and preserve the deployment identity at the required block:

`DEPLOYMENT_BINDING_UNPROVEN → CASE NOT QUALIFYING`

Do not modify PayGod to work around this failure.

## External corroboration is not the witness

Secondary/explorer research may identify likely proxy type, deployment block, or implementation candidates. Such material is a research lead only until reproduced through the block-bound method above.

## Non-claims

This method does not establish:

- source correctness;
- contract safety;
- administrator trustworthiness;
- evaluator quality;
- off-chain evidence authenticity;
- trusted external time;
- PayGod authority.

It establishes only a reproducible deployment-identity boundary for the sampled block.
