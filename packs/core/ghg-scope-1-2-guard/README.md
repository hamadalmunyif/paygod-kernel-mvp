# GHG Scope 1 & 2 Guard (Community Pack)

This pack enforces **references-only** evidence requirements for Scope 1 & 2 emissions reporting.

## Why
Scope 1 & 2 reporting often fails audits because evidence and emission factor references are missing.

## Inputs
- `ghg_report` observation: includes integer `scope1_kgco2e` / `scope2_kgco2e` values plus `methodology_ref`, `emission_factor_refs`, and `evidence_refs`. Kilograms are used so decision-critical emissions remain integer-only under `paygod-c14n-v1`.

## Decisions
- `deny` when evidence/methodology references are missing.
- `flag` when emission factors references are missing.

## Tests
Run:
```bash
dotnet run --project src/PayGod.Cli -- test --pack packs/core/ghg-scope-1-2-guard
```

## Production readiness (2026-10-10)

**Status: IMPLEMENTED COMMUNITY PACK; NOT PRODUCTION-CERTIFIED OR END-TO-END EMISSIONS VALIDATION.**

The `pack.yaml` input schema describes expected fields, but the current canonical `run` path does **not** enforce that embedded input schema before policy evaluation. `test --pack` demonstrates the listed policy examples; it does **not** constitute evidence-admission or operational accreditation.

A deliberately separate [GHG pack-readiness research gate](../../../research/pack-readiness/ghg-scope12-v0/README.md) adds synthetic strict input-shape tests, opt-in pre-kernel rejection, and a canonical-CLI-to-independent-verifier CI demonstration. Its required complete-reference profile **withholds** incomplete reports before Kernel execution. This is distinct from the Pack's lower-level `deny` and `flag` test fixtures, which assume known input meanings.

No source authenticity, externally measured calculation, factor authorization, evidence-reference dereferencing, non-bypassable API integration, independent recipient acceptance or real production reliability has been established. An `allow` from this Pack is a scoped policy result, **not** a verified GHG inventory, environmental certification, or permission to rely on its values.
