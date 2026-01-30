# Schema Stability

Schemas in `contracts/schemas/` are the project’s public contracts.

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
