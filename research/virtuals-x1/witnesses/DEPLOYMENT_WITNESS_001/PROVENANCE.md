# X1 Deployment Witness 001 — Provenance

Status: CANONICAL LEVEL 0 REFERENCE WITNESS  
Captured: 2026-10-05  
Scope: read-only Base mainnet deployment binding only

## Canonical pinned execution

- GitHub Actions workflow: `Virtuals X1 Deployment Binding Witness`
- workflow run id: `37256667972`
- PR head SHA at capture: `bf3aa2a602a80ceb536840f849544e08956a5f26`
- workflow artifact id: `11322404369`
- workflow artifact digest: `sha256:720f7ae42b27324bf4f562f4b581e8decff912d2ce8b37f7a0b11361ad92ec7b`
- reference block: `52189048` / `0x31c5778`
- block hash: `0x565c9c7f6ac17d383f14c8453c1d369c0ffb55a2afcbe31d55c5daa39bf55151`
- endpoint used: `https://mainnet.base.org`
- raw RPC artifact SHA-256: `0xd68233c15e68b4e908eb92b9d2f56a13135cdce04cddab2c601bd582fc9262e3`

The workflow was re-run after `DEPLOYMENT_REFERENCE_BLOCK.txt` was pinned to the exact block above. This pinned run, not the earlier moving `finalized` probe, is the canonical Level 0 witness.

## Selection probe

The preceding successful probe used the RPC `finalized` tag only to select a stable candidate reference block:

- workflow run id: `37256567348`
- head SHA: `1415ab136072f71c091c2113b69389c45812239d`
- selected block: `52189048`
- selected block hash: `0x565c9c7f6ac17d383f14c8453c1d369c0ffb55a2afcbe31d55c5daa39bf55151`

It is corroborating acquisition history, not the canonical pinned witness.

## Boundary

This record proves only that the frozen deployment-binding method executed successfully against the sampled block and recovered non-empty proxy/implementation code bound through the ERC-1967 implementation slot.

It does not prove source equivalence, contract correctness, trusted external time, evaluator quality, Virtuals governance quality, or PayGod authority.

Every qualifying real X1 case MUST repeat deployment binding at its own predecessor block.
