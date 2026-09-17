#!/usr/bin/env python3
"""Independent verifier for a transferred Paygod evidence bundle.

This verifier deliberately does not execute the pack or require producer workspace state.
It verifies the manifest lock, receipt binding, and ledger hash chain from artifact bytes only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value) -> str:
    # Matches the subset used by the current ledger records: sorted keys, compact UTF-8 JSON.
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def verify_ledger(path: Path, errors: list[str]) -> None:
    if not path.exists():
        return
    previous = "0" * 64
    expected_index = 0
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            entry = json.loads(raw)
        except Exception as exc:
            errors.append(f"ledger line {line_no}: invalid JSON: {exc}")
            return
        if entry.get("entry_index") != expected_index:
            errors.append(f"ledger line {line_no}: unexpected entry_index")
        if entry.get("previous_hash") != previous:
            errors.append(f"ledger line {line_no}: previous_hash mismatch")
        payload = {
            "previous_hash": entry.get("previous_hash"),
            "timestamp": entry.get("timestamp"),
            "data": entry.get("data"),
        }
        calculated = sha256_bytes(canonical_json(payload).encode("utf-8"))
        if entry.get("record_hash") != calculated:
            errors.append(f"ledger line {line_no}: record_hash mismatch")
        previous = entry.get("record_hash", "")
        expected_index += 1


def verify(bundle: Path) -> dict:
    errors: list[str] = []
    manifest_path = bundle / "manifest.json"
    receipt_path = bundle / "receipt.json"
    for required in (manifest_path, receipt_path):
        if not required.is_file():
            errors.append(f"missing {required.name}")
    if errors:
        return {"status": "invalid", "portable": False, "errors": errors}

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return {"status": "invalid", "portable": False, "errors": [f"invalid control JSON: {exc}"]}

    entries = manifest.get("files") or []
    digest_lines: list[str] = []
    for entry in sorted(entries, key=lambda item: item.get("name", "")):
        name = entry.get("name")
        expected = entry.get("sha256")
        if not name or not expected:
            errors.append("manifest contains malformed file entry")
            continue
        path = bundle / name
        if not path.is_file():
            errors.append(f"missing manifest file: {name}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"sha256 mismatch: {name}")
        digest_lines.append(f"{name}={expected}\n")

    calculated_bundle = sha256_bytes("".join(digest_lines).encode("utf-8"))
    manifest_bundle = (manifest.get("bundle") or {}).get("bundle_digest")
    if calculated_bundle != manifest_bundle:
        errors.append("manifest bundle_digest mismatch")

    receipt_bundle = receipt.get("bundle") or {}
    if receipt_bundle.get("bundle_digest") != manifest_bundle:
        errors.append("receipt bundle_digest does not bind manifest bundle")
    if receipt_bundle.get("manifest_sha256") != sha256_file(manifest_path):
        errors.append("receipt manifest_sha256 mismatch")

    # Receipt repeats the manifest file lock; require exact agreement.
    if receipt_bundle.get("files") != entries:
        errors.append("receipt files do not match manifest files")

    verify_ledger(bundle / "ledger.jsonl", errors)

    return {
        "status": "valid" if not errors else "invalid",
        "portable": not errors,
        "bundle_digest": manifest_bundle,
        "manifest_sha256": sha256_file(manifest_path),
        "verified_files": len(entries),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--result", type=Path, default=Path("verification-result.json"))
    args = parser.parse_args()
    result = verify(args.bundle)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    sys.exit(main())
