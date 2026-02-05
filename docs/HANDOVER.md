# Paygod Kernel MVP — Phase 1 Closed Handover

## Direction Lock (Non-Negotiable)

- Phase 1: **CLOSED** at baseline commit $baselineCommit
- Baseline branch: **main only**
- Canonical Truth:
  - contracts/ = Law
  - docs/ = Literal reflection of contracts (no opinion)
  - CI = Execution gate / enforcement
- No re-interpretation of Phase 1 decisions is allowed.

## Repository Snapshot (as generated)

- Repository (origin): $originUrl
- Branch: $branch
- Baseline Commit: $headCommitShort
- Generated At (UTC): $utcNow

## What is Locked

- Contracts-first baseline at $baselineCommit
- BAP + Envelope contract alignment
- Schema governance (hash source-of-truth = Git HEAD blobs)
- CI as the enforcement mechanism

## What is NOT Implemented Yet (Explicitly Out of Phase 1)

- Persistent services
- External APIs
- Runtime ledger infrastructure
- Multi-pack composition engine

## Phase 2 Entrypoint (Single Goal)

Ship **one deterministic Proof Run** using:
- packs/core/bap-output-validator-guard

Outputs must be verifiable and enforced by CI:
- decision
- vidence (refs-only; no raw payload; no PII)
- ledger_entry (hash-chained)

## Phase 2 Composition Rule (Law-only, no implementation yet)

Phase 2 early execution uses **single-pack authority**.  
Multi-pack composition deferred.  
Future default: **deny-wins + reason aggregation**.