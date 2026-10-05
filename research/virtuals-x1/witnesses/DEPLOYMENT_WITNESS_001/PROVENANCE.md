# X1 Deployment Witness 001 — Provenance

Status: CANONICAL LEVEL 0 REFERENCE WITNESS  
Captured: 2026-10-05  
Scope: read-only Base mainnet deployment binding only

## Canonical pinned execution

- GitHub Actions workflow: `Virtuals X1 Deployment Binding Witness`
- workflow run id: `37257329054`
- PR head SHA at capture: `e1b3fb2e256cc199e751fe0efeb902eb9452243e`
- workflow artifact id: `11323590693`
- workflow artifact digest: `sha256:7da9cbfc2ccdcff567f2f443cf65693f2ee0e56ebd27ec23f834944ffdb2176a`
- reference block: `52189048` / `0x31c5778`
- block hash: `0x565c9c7f6ac17d383f14c8453c1d369c0ffb55a2afcbe31d55c5daa39bf55151`
- endpoint used: `https://mainnet.base.org`
- raw RPC artifact SHA-256: `0xdea036eebf237eeccfeb317b522d383ff3b6549e2a89eb571f930d5e110bf832`
- post-read block-hash recheck: `verified`

The workflow used the exact block in `DEPLOYMENT_REFERENCE_BLOCK.txt`, performed the storage/code reads, and then re-fetched the same numeric block and required its hash to equal the original block hash before emitting `BOUND`.

This hardened pinned run supersedes the earlier reference artifact captured before the post-read block-hash guard was added.

## Failure-evidence behavior

The capture tool records the attempted RPC request before transport, preserves decoded responses or transport/decode errors when available, and writes `raw_rpc.json` with `capture_status = FAILED` before re-raising a capture/validation error. The workflow uploads the capture directory with `if: always()`.

Therefore a failed deployment binding is preserved as evidence rather than disappearing with the failed job.

## Boundary

This record proves only that the frozen deployment-binding method executed successfully against the sampled block and recovered non-empty proxy/implementation code bound through the ERC-1967 implementation slot, with the block hash stable across the state-read interval.

It does not prove source equivalence, contract correctness, trusted external time, evaluator quality, Virtuals governance quality, or PayGod authority.

Every qualifying real X1 case MUST repeat deployment binding at its own predecessor block.
