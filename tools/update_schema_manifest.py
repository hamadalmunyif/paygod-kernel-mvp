#!/usr/bin/env python3
"""Update contracts/schema-manifest.json with current SHA-256 of schemas.

Usage:
  python3 tools/update_schema_manifest.py
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "contracts" / "schemas"
MANIFEST_PATH = ROOT / "contracts" / "schema-manifest.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def main() -> None:
    entries = {}
    for p in sorted(SCHEMAS_DIR.glob("*.json")):
        entries[p.name] = {"sha256": sha256_file(p)}
    payload = {
        "manifest_version": "1.0.0",
        "generated_at": __import__("datetime").datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "schemas": entries,
    }
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"✅ Updated {MANIFEST_PATH.relative_to(ROOT)} ({len(entries)} schemas)")

if __name__ == "__main__":
    main()
