#!/usr/bin/env python3
"""Independent verifier for a transferred Paygod evidence bundle.

This verifier deliberately does not execute the pack or require producer workspace state.
It verifies the manifest lock, decision-critical receipt binding, and ledger hash chain
from artifact bytes only.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unicodedata

VERIFIER_VERSION = "0.2.0"
_HEX64 = re.compile(r"^[a-f0-9]{64}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _ordinal_key(value: str) -> bytes:
    # Match .NET StringComparer.Ordinal by sorting UTF-16 code units.
    return value.encode("utf-16-be", "surrogatepass")


def _jcs_string(value: str) -> str:
    # Match the producer's current Canonicalizer.cs behavior exactly:
    # NFC normalize, then JSON-escape all non-ASCII UTF-16 code units.
    value = unicodedata.normalize("NFC", value)
    units = value.encode("utf-16-be", "surrogatepass")
    out = ['"']
    for index in range(0, len(units), 2):
        unit = (units[index] << 8) | units[index + 1]
        if unit == 0x22:
            out.append('\\\"')
        elif unit == 0x5C:
            out.append("\\\\")
        elif unit == 0x08:
            out.append("\\b")
        elif unit == 0x0C:
            out.append("\\f")
        elif unit == 0x0A:
            out.append("\\n")
        elif unit == 0x0D:
            out.append("\\r")
        elif unit == 0x09:
            out.append("\\t")
        elif unit < 0x20 or unit > 0x7E:
            out.append(f"\\u{unit:04x}")
        else:
            out.append(chr(unit))
    out.append('"')
    return "".join(out)


def canonical_json(value) -> str:
    """Mirror src/PayGod.Cli/Core/Canonicalizer.cs for ledger verification."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return _jcs_string(value)
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("JSON object keys must be strings")
        keys = sorted(value, key=_ordinal_key)
        return "{" + ",".join(f"{_jcs_string(key)}:{canonical_json(value[key])}" for key in keys) + "}"
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite number")
        if value == 0:
            return "0"
        rendered = format(value, ".17g").replace("E", "e")
        return re.sub(r"e([+-])0+(\\d+)$", r"e\\1\\2", rendered)
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


def _invalid(errors: list[str], **extra) -> dict:
    result = {
        "status": "invalid",
        "portable": False,
        "verifier_version": VERIFIER_VERSION,
        "errors": errors,
    }
    result.update(extra)
    return result


def _parse_instant(value) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def verify_ledger(path: Path, errors: list[str]) -> dict | None:
    if not path.exists():
        return None

    previous = "0" * 64
    expected_index = 0
    last_entry: dict | None = None

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as exc:
        errors.append(f"ledger read failed: {exc}")
        return None

    for line_no, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        try:
            entry = json.loads(raw)
        except Exception as exc:
            errors.append(f"ledger line {line_no}: invalid JSON: {exc}")
            return None
        if not isinstance(entry, dict):
            errors.append(f"ledger line {line_no}: entry must be an object")
            return None

        if entry.get("entry_index") != expected_index:
            errors.append(f"ledger line {line_no}: unexpected entry_index")
        if entry.get("previous_hash") != previous:
            errors.append(f"ledger line {line_no}: previous_hash mismatch")

        payload = {
            "previous_hash": entry.get("previous_hash"),
            "timestamp": entry.get("timestamp"),
            "data": entry.get("data"),
        }
        try:
            calculated = sha256_bytes(canonical_json(payload).encode("utf-8"))
        except Exception as exc:
            errors.append(f"ledger line {line_no}: canonicalization failed: {exc}")
            return None

        record_hash = entry.get("record_hash")
        if record_hash != calculated:
            errors.append(f"ledger line {line_no}: record_hash mismatch")
        previous = record_hash if isinstance(record_hash, str) else ""
        expected_index += 1
        last_entry = entry

    return last_entry


def _safe_manifest_name(name: str) -> bool:
    path = Path(name)
    return bool(name) and not path.is_absolute() and path.name == name and name not in {".", ".."}


def _validate_receipt_semantics(
    manifest: dict,
    receipt: dict,
    ledger_entry: dict | None,
    manifest_sha: str,
    errors: list[str],
) -> None:
    if receipt.get("api_version") != "paygod/v1":
        errors.append("receipt api_version mismatch")
    if receipt.get("kind") != "Receipt":
        errors.append("receipt kind mismatch")

    clock = receipt.get("clock")
    if not isinstance(clock, dict):
        errors.append("receipt clock must be an object")
        clock = {}
    if clock.get("source") != "env:PAYGOD_CLOCK":
        errors.append("receipt clock source mismatch")
    if receipt.get("generated_at") != clock.get("value"):
        errors.append("receipt generated_at does not match clock.value")

    canonicalization = receipt.get("canonicalization")
    if not isinstance(canonicalization, dict) or canonicalization.get("json") != "rfc8785":
        errors.append("receipt canonicalization declaration mismatch")

    if receipt.get("pack") != manifest.get("pack"):
        errors.append("receipt pack does not match manifest pack")
    if receipt.get("input") != manifest.get("input"):
        errors.append("receipt input does not match manifest input")

    entries = manifest.get("files")
    manifest_bundle = manifest.get("bundle")
    receipt_bundle = receipt.get("bundle")
    if not isinstance(manifest_bundle, dict):
        errors.append("manifest bundle must be an object")
        manifest_bundle = {}
    if not isinstance(receipt_bundle, dict):
        errors.append("receipt bundle must be an object")
        receipt_bundle = {}

    if receipt_bundle.get("bundle_digest") != manifest_bundle.get("bundle_digest"):
        errors.append("receipt bundle_digest does not bind manifest bundle")
    if receipt_bundle.get("manifest_sha256") != manifest_sha:
        errors.append("receipt manifest_sha256 mismatch")
    if receipt_bundle.get("files") != entries:
        errors.append("receipt files do not match manifest files")

    verdict = receipt.get("verdict")
    if not isinstance(verdict, dict):
        errors.append("receipt verdict must be an object")
        verdict = {}

    if ledger_entry is None:
        errors.append("missing ledger entry for receipt decision binding")
        return

    ledger_data = ledger_entry.get("data")
    if not isinstance(ledger_data, dict):
        errors.append("ledger data must be an object")
        return

    if verdict.get("value") != ledger_data.get("verdict"):
        errors.append("receipt verdict does not match locked ledger verdict")
    if verdict.get("rule_name") != ledger_data.get("rule_name"):
        errors.append("receipt rule_name does not match locked ledger")
    if verdict.get("reason") != ledger_data.get("reason"):
        errors.append("receipt reason does not match locked ledger")
    if receipt.get("pack") != ledger_data.get("pack"):
        errors.append("receipt pack does not match locked ledger")

    receipt_input = receipt.get("input")
    receipt_input_hash = receipt_input.get("canonical_hash") if isinstance(receipt_input, dict) else None
    if receipt_input_hash != ledger_data.get("input_hash"):
        errors.append("receipt input hash does not match locked ledger")

    manifest_time = _parse_instant(manifest.get("generated_at"))
    ledger_time = _parse_instant(ledger_entry.get("timestamp"))
    receipt_time = _parse_instant(clock.get("value"))
    if manifest_time is None or ledger_time is None or receipt_time is None:
        errors.append("invalid or timezone-naive decision timestamp")
    elif not (manifest_time == ledger_time == receipt_time):
        errors.append("receipt clock does not match locked manifest/ledger time")


def verify(bundle: Path) -> dict:
    errors: list[str] = []
    manifest_path = bundle / "manifest.json"
    receipt_path = bundle / "receipt.json"

    for required in (manifest_path, receipt_path):
        if not required.is_file():
            errors.append(f"missing {required.name}")
    if errors:
        return _invalid(errors)

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return _invalid([f"invalid control JSON: {exc}"])

    if not isinstance(manifest, dict):
        return _invalid(["manifest must be an object"])
    if not isinstance(receipt, dict):
        return _invalid(["receipt must be an object"])

    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        return _invalid(["manifest files must be a non-empty array"])

    digest_lines: list[str] = []
    seen_names: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"manifest file entry {index} must be an object")
            continue
        name = entry.get("name")
        expected = entry.get("sha256")
        expected_bytes = entry.get("bytes")
        if not isinstance(name, str) or not _safe_manifest_name(name):
            errors.append(f"manifest file entry {index} has invalid name")
            continue
        if name in seen_names:
            errors.append(f"duplicate manifest file: {name}")
            continue
        seen_names.add(name)
        if not isinstance(expected, str) or not _HEX64.fullmatch(expected):
            errors.append(f"manifest file entry {index} has invalid sha256")
            continue
        if not isinstance(expected_bytes, int) or expected_bytes < 0:
            errors.append(f"manifest file entry {index} has invalid byte count")
            continue

        path = bundle / name
        if not path.is_file():
            errors.append(f"missing manifest file: {name}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"sha256 mismatch: {name}")
        if path.stat().st_size != expected_bytes:
            errors.append(f"byte count mismatch: {name}")
        digest_lines.append(f"{name}={expected}\\n")

    manifest_bundle_obj = manifest.get("bundle")
    if not isinstance(manifest_bundle_obj, dict):
        errors.append("manifest bundle must be an object")
        manifest_bundle_obj = {}
    if manifest.get("api_version") != "paygod/v1":
        errors.append("manifest api_version mismatch")
    if manifest.get("kind") != "Manifest":
        errors.append("manifest kind mismatch")
    if manifest_bundle_obj.get("algorithm") != "sha256":
        errors.append("manifest bundle algorithm mismatch")
    if manifest_bundle_obj.get("file_count") != len(entries):
        errors.append("manifest file_count mismatch")

    manifest_bundle = manifest_bundle_obj.get("bundle_digest")
    calculated_bundle = sha256_bytes("".join(sorted(digest_lines)).encode("utf-8"))
    if calculated_bundle != manifest_bundle:
        errors.append("manifest bundle_digest mismatch")

    ledger_entry = verify_ledger(bundle / "ledger.jsonl", errors)
    manifest_sha = sha256_file(manifest_path)
    _validate_receipt_semantics(manifest, receipt, ledger_entry, manifest_sha, errors)

    return {
        "status": "valid" if not errors else "invalid",
        "portable": not errors,
        "verifier_version": VERIFIER_VERSION,
        "bundle_digest": manifest_bundle,
        "manifest_sha256": manifest_sha,
        "verified_files": len(entries),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERIFIER_VERSION}")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--result", type=Path, default=Path("verification-result.json"))
    args = parser.parse_args()

    try:
        result = verify(args.bundle)
    except Exception as exc:
        result = _invalid([f"verifier failure: {type(exc).__name__}: {exc}"])

    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    sys.exit(main())
