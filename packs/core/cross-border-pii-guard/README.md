# Cross-border PII Guard (Community Pack)

Flags cross-border PII transfers that lack an approved transfer mechanism reference.

## Why
A common audit failure is cross-border data movement without documented legal mechanism.

## Evidence
This pack is **references-only**: provide `evidence_refs` and `transfer_mechanism_ref` as references.

## Tests
```bash
dotnet run --project src/PayGod.Cli -- test --pack packs/core/cross-border-pii-guard
```
