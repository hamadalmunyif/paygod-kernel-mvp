# Schema Stability

## Hash Source of Truth (Governance)
Schema hashes in contracts/schema-manifest.json are governed by Git, not by local files.
- CI computes hashes from Git blobs (HEAD) as the canonical source of truth.
- Working tree bytes (CRLF/BOM/editor filters) MUST NOT redefine the legal hash.
- Local tooling MAY provide preview using STAGED (index) then fallback to HEAD, but this is not the enforcement truth source.


Schemas in `contracts/schemas/` are the project's public contracts.

## How stability is enforced
- `contracts/schema-manifest.json` stores SHA-256 digests for each schema file.
- CI checks that the manifest matches the current schemas.

## When to update the manifest
Only when a schema change is intentional and compliant with:
- `contracts/versioning/SCHEMA_SEMVER_POLICY.md`

Update:
```bash
python3 tools/update_schema_manifest.py
```

Validate:
```bash
python3 tools/check_schema_manifest.py
```
