#!/usr/bin/env python3
"""
Check contracts/schema-manifest.json matches current schema SHA-256 digests.

Governance policy:
- CI truth source = HEAD (non-negotiable)
- Dev truth source = STAGED then HEAD (legal preview before commit)
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "contracts" / "schema-manifest.json"
SCHEMAS_DIR = ROOT / "contracts" / "schemas"


def _git_bytes(spec: str) -> bytes:
    # spec example: "HEAD:contracts/schemas/foo.json" or ":contracts/schemas/foo.json" (staged)
    return subprocess.check_output(["git", "show", spec])


def read_schema_bytes(rel_path: str, prefer_staged: bool) -> bytes:
    # CI => prefer_staged=False (HEAD only)
    # Dev => prefer_staged=True  (STAGED then HEAD)
    if prefer_staged:
        try:
            return _git_bytes(f":{rel_path}")  # staged (index)
        except subprocess.CalledProcessError:
            pass
    return _git_bytes(f"HEAD:{rel_path}")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if not MANIFEST_PATH.exists():
        print("❌ Missing contracts/schema-manifest.json. Run tools/update_schema_manifest.py")
        return 1

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to read manifest: {e}")
        return 1

    schemas = manifest.get("schemas") or {}
    if not isinstance(schemas, dict) or not schemas:
        print("❌ Manifest has no schemas.")
        return 1

    # In GitHub Actions, env CI=true is set. That forces HEAD-only.
    prefer_staged = (os.getenv("CI", "").lower() != "true")

    failed = False
    count = 0

    for name, meta in schemas.items():
        count += 1
        expected = (meta or {}).get("sha256")
        if not expected:
            print(f"❌ {name}: missing sha256 in manifest")
            failed = True
            continue

        rel = f"contracts/schemas/{name}"

        # Sanity: file should exist in repo structure (working tree path)
        # but hash is computed from git objects per policy.
        if not (SCHEMAS_DIR / name).exists():
            print(f"❌ {name}: missing schema file on disk at contracts/schemas/{name}")
            failed = True
            continue

        try:
            data = read_schema_bytes(rel, prefer_staged=prefer_staged)
            actual = sha256_hex(data)
        except subprocess.CalledProcessError as e:
            print(f"❌ {name}: cannot read from git objects ({e})")
            failed = True
            continue

        if actual != expected:
            print(f"❌ {name}: manifest={expected} actual={actual}")
            failed = True

    if failed:
        print("ℹ️ If schema changes are intentional, run: python tools/update_schema_manifest.py")
        return 1

    print(f"✅ Schema manifest matches ({count} schemas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())