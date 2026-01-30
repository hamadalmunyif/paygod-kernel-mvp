# GHG Scope 1 & 2 Guard (Community Pack)

This pack enforces **references-only** evidence requirements for Scope 1 & 2 emissions reporting.

## Why
Scope 1 & 2 reporting often fails audits because evidence and emission factor references are missing.

## Inputs
- `ghg_report` observation: includes `methodology_ref`, `emission_factor_refs`, `evidence_refs`.

## Decisions
- `deny` when evidence/methodology references are missing.
- `flag` when emission factors references are missing.

## Tests
Run:
```bash
dotnet run --project src/PayGod.Cli -- test --pack packs/core/ghg-scope-1-2-guard
```
