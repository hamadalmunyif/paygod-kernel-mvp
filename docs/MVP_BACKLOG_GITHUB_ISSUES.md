# MVP Backlog (GitHub Issues/Milestones)

This document provides a copy-paste backlog aligned with the MVP agreements:
- CLI is the source of truth for pack run/test.
- Ledger is append-only, immutable, strictly non-PII.
- Evidence is references only (hashes + pointers), no raw sensitive payloads.
- Packs are split into `packs/core` (cloud-agnostic) and `packs/providers/<cloud>` (provider-specific).
- Security is gated on PR via GitHub Actions.

## Milestones
- M0: Repo hygiene + tooling baseline
- M1: Contracts enforcement (schema validation)
- M2: Multi-findings + truth decision outputs
- M3: File-based Ledger/Evidence stores + minimal services
- M4: Docker Compose MVP
- M5: Security gate + release discipline
- M6: Tests (xUnit) + regression

## PR plan (a)
1) **PR1 — Structure only (move-only)**
   - packs restructuring (`core/providers/_drafts`)
   - provider lint script + CI step
   - remove nested workflows
   - pin SDK + build hygiene
   - README CLI-only

2) **PR2 — Engine outputs (behavior)**
   - multi-findings + deterministic truth decision
   - schema validation for packs/tests
   - output artifacts always schema-valid (even on error)

3) **PR3 — MVP services**
   - validate/run APIs
   - file-based ledger/evidence stores with chaining + verify
   - docker compose volumes + healthchecks

## Build hygiene (b)
- `global.json` to pin .NET SDK
- `Directory.Build.props` to enforce nullable + analyzers + warnings-as-errors
- Optional CI step: `dotnet format --verify-no-changes`

## Provider separation enforcement
- Lint script: `tools/ci/lint_core_packs_providers.py`
- Config: `tools/ci/provider_lint_config.json`
- Allowlist: `.paygod-provider-lint-allowlist`

## Minimal tests standard (core packs)
A core pack must ship `tests/cases.yaml` that contains:
- at least one **allow** case
- at least one **deny** case
- deny must be triggered by a concrete input difference (not an unrelated sample)

If a pack is a skeleton or has no stable rules yet, it must live in `packs/_drafts/`.
