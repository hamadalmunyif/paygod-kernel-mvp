# Build & Run

This repo targets reproducible verification and proof workflows.
You can build either locally (.NET) or using Docker.

## Prerequisites

- .NET SDK (see `global.json` if present)
- Python 3.10+ (for spec verification tools)

## Local build (recommended for contributors)

```bash
dotnet build src/PayGod.sln
dotnet test src/PayGod.sln
```

## CLI quickstart

Validate JSON + canonical hash:

```bash
dotnet run --project src/PayGod.Cli -- validate --input sample.json
```

Run pack tests:

```bash
dotnet run --project src/PayGod.Cli -- test --pack packs/core/critical-cve-blocker
```

Run a pack and emit loop artifacts:

```bash
dotnet run --project src/PayGod.Cli -- run --pack packs/core/critical-cve-blocker --input sample.json --out ./out
# out/plan.json, out/findings.json, out/ledger.jsonl
```

Generate a new pack skeleton:

```bash
dotnet run --project src/PayGod.Cli -- pack init --category security --name my-pack
```

## Spec vectors (canonicalization / ledger chaining)

```bash
python3 -m pip install -r tools/requirements.txt
python3 tools/verify_spec.py
```

## Schema stability gate

```bash
python3 tools/check_schema_manifest.py
# If you intentionally changed schemas:
python3 tools/update_schema_manifest.py
```

## Common errors

- **Pack evaluation does not match tests**:
  - ensure conditions use the supported DSL (see `docs/STARTER_PACKS.md`)
- **Schema manifest check fails**:
  - you changed a schema; update the manifest using `tools/update_schema_manifest.py`
- **Canonical hash mismatch**:
  - verify `spec/test-vectors` first, then `PayGod.Cli.Core.Canonicalizer`
