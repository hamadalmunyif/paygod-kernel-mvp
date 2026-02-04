#!/usr/bin/env python3
"""
Update contracts/schema-manifest.json with current SHA-256 of schemas.

Governance policy:
- CI truth source = HEAD (non-negotiable)
- Dev truth source = STAGED then HEAD (legal preview before commit)

Note:
This script computes digests from Git objects, not from working tree bytes.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "contracts" / "schema-manifest.json"
SCHEMAS_DIR = ROOT / "contracts" / "schemas"


def _git_bytes(spec: str) -> bytes:
    return subprocess.check_output(["git", "show", spec])


def read_schema_bytes(rel_path: str, prefer_staged: bool) -> bytes:
    if prefer_staged:
        try:
            return _git_bytes(f":{rel_path}")  # staged (index)
        except subprocess.CalledProcessError:
            pass
    return _git_bytes(f"HEAD:{rel_path}")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if not SCHEMAS_DIR.exists():
        print("❌ Missing contracts/schemas directory.")
        return 1

    # In GitHub Actions, env CI=true is set. That forces HEAD-only.
    prefer_staged = (os.getenv("CI", "").lower() != "true")

    schema_files = sorted([p for p in SCHEMAS_DIR.glob("*.json") if p.is_file()])
    if not schema_files:
        print("❌ No schema files found in contracts/schemas/*.json")
        return 1

    schemas = {}
    for p in schema_files:
        name = p.name
        rel = f"contracts/schemas/{name}"
        try:
            data = read_schema_bytes(rel, prefer_staged=prefer_staged)
        except subprocess.CalledProcessError as e:
            print(f"❌ Cannot read {name} from git objects: {e}")
            return 1
        schemas[name] = {"sha256": sha256_hex(data)}

    manifest = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "manifest_version": "1.0.0",
        "schemas": schemas,
    }

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"✅ Updated contracts/schema-manifest.json ({len(schemas)} schemas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())