#!/usr/bin/env python3
"""Check contracts/schema-manifest.json matches current schema SHA-256 digests.

Usage:
  python3 tools/check_schema_manifest.py
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
MANIFEST_PATH = ROOT / "contracts" / "schema-manifest.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def main() -> int:
    if not MANIFEST_PATH.exists():
        print("❌ Missing contracts/schema-manifest.json. Run tools/update_schema_manifest.py")
        return 2
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    ok = True
    schemas = manifest.get("schemas", {})
    for p in sorted(SCHEMAS_DIR.glob("*.json")):
        expected = schemas.get(p.name, {}).get("sha256")
        actual = sha256_file(p)
        if expected != actual:
            ok = False
            print(f"❌ {p.name}: manifest={expected} actual={actual}")
    # Detect removed schemas in repo vs manifest
    repo_names = {p.name for p in SCHEMAS_DIR.glob('*.json')}
    manifest_names = set(schemas.keys())
    missing = repo_names - manifest_names
    extra = manifest_names - repo_names
    for name in sorted(missing):
        ok = False
        print(f"❌ {name}: missing from manifest")
    for name in sorted(extra):
        ok = False
        print(f"❌ {name}: present in manifest but missing from repo")
    if ok:
        print(f"✅ Schema manifest matches ({len(repo_names)} schemas)")
        return 0
    print("ℹ️ If schema changes are intentional, run: python3 tools/update_schema_manifest.py")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
