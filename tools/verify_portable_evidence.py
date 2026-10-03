#!/usr/bin/env python3
"""Independent verifier for a transferred Paygod evidence bundle.

This verifier deliberately does not execute the pack or require producer workspace state.
It verifies bundle integrity from artifact bytes only. Issuer authenticity, replay, and
trusted time are separate verification dimensions and are not implied by integrity.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

try:
    from issuer_auth import load_trust_store, verify_detached_signature
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from issuer_auth import load_trust_store, verify_detached_signature

VERIFIER_VERSION = "0.4.0"
CANONICALIZATION_PROFILE = "paygod-c14n-v1"
SAFE_INTEGER_MAX = 9_007_199_254_740_991
_HEX64 = re.compile(r"^[a-f0-9]{64}$")
_CANONICAL_VERDICTS = {"allow", "deny", "flag", "error"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _ordinal_key(value: str) -> bytes:
    # Match .NET StringComparer.Ordinal by sorting UTF-16 code units.
    return value.encode("utf-16-be", "surrogatepass")


def _profile_string(value: str) -> str:
    # paygod-c14n-v1 preserves string values exactly; it does not normalize them.
    # Non-ASCII UTF-16 code units are escaped to keep the profile byte-stable across runtimes.
    units = value.encode("utf-16-be", "surrogatepass")
    out = ['"']
    index = 0
    while index < len(units):
        unit = (units[index] << 8) | units[index + 1]
        if 0xD800 <= unit <= 0xDBFF:
            if index + 3 >= len(units):
                raise ValueError("unpaired Unicode surrogate")
            next_unit = (units[index + 2] << 8) | units[index + 3]
            if not (0xDC00 <= next_unit <= 0xDFFF):
                raise ValueError("unpaired Unicode surrogate")
        elif 0xDC00 <= unit <= 0xDFFF:
            previous_unit = (units[index - 2] << 8) | units[index - 1] if index >= 2 else None
            if previous_unit is None or not (0xD800 <= previous_unit <= 0xDBFF):
                raise ValueError("unpaired Unicode surrogate")
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
        index += 2
    out.append('"')
    return "".join(out)


def canonical_json(value) -> str:
    """Encode the restricted paygod-c14n-v1 JSON profile.

    Accepted values: null, booleans, strings, arrays, objects, and safe integers.
    Object/property names MUST already be NFC. String values are preserved without
    normalization. Floats/decimals and unsafe integers fail closed.
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return _profile_string(value)
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("JSON object keys must be strings")
        for key in value:
            if unicodedata.normalize("NFC", key) != key:
                raise ValueError("JSON object key is not NFC-normalized")
        keys = sorted(value, key=_ordinal_key)
        return "{" + ",".join(
            f"{_profile_string(key)}:{canonical_json(value[key])}" for key in keys
        ) + "}"
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, int):
        if abs(value) > SAFE_INTEGER_MAX:
            raise ValueError("integer outside paygod-c14n-v1 safe range")
        return str(value)
    if isinstance(value, float):
        raise ValueError("floating-point numbers are not allowed by paygod-c14n-v1")
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


def _dimensions(
    integrity: str,
    time_authority: str = "failed",
    issuer_authenticity: str = "not_verified",
) -> dict:
    return {
        "integrity": integrity,
        "issuer_authenticity": issuer_authenticity,
        "replay": "not_performed",
        "time_authority": time_authority,
    }


def _invalid(errors: list[str], **extra) -> dict:
    time_authority = extra.pop("time_authority", "failed")
    result = {
        "status": "invalid",
        "portable": False,
        "verifier_version": VERIFIER_VERSION,
        "verification": _dimensions("failed", time_authority),
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
        if not isinstance(record_hash, str) or not _HEX64.fullmatch(record_hash):
            errors.append(f"ledger line {line_no}: record_hash must be 64 lowercase hex characters")
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
    allow_unbound_clock: bool,
) -> tuple[str, str]:
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
    if not isinstance(canonicalization, dict) or canonicalization.get("json") != CANONICALIZATION_PROFILE:
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

    verdict_value = verdict.get("value")
    verdict_rule = verdict.get("rule_name")
    verdict_reason = verdict.get("reason")
    if verdict_value not in _CANONICAL_VERDICTS:
        errors.append("receipt verdict value must be one of allow/deny/flag/error")
    if not isinstance(verdict_rule, str):
        errors.append("receipt verdict rule_name must be a string")
    if not isinstance(verdict_reason, str):
        errors.append("receipt verdict reason must be a string")

    receipt_pack = receipt.get("pack")
    if not isinstance(receipt_pack, dict):
        errors.append("receipt pack must be an object")
        receipt_pack = {}
    for key in ("name", "version", "path", "digest_sha256"):
        if not isinstance(receipt_pack.get(key), str):
            errors.append(f"receipt pack {key} must be a string")
    if isinstance(receipt_pack.get("digest_sha256"), str) and not _HEX64.fullmatch(receipt_pack["digest_sha256"]):
        errors.append("receipt pack digest_sha256 must be 64 lowercase hex characters")

    receipt_input = receipt.get("input")
    if not isinstance(receipt_input, dict):
        errors.append("receipt input must be an object")
        receipt_input = {}
    receipt_input_hash = receipt_input.get("canonical_hash")
    if not isinstance(receipt_input_hash, str) or not _HEX64.fullmatch(receipt_input_hash):
        errors.append("receipt input canonical_hash must be 64 lowercase hex characters")

    if ledger_entry is None:
        errors.append("missing ledger entry for receipt decision binding")
        return "invalid", "failed"

    ledger_data = ledger_entry.get("data")
    if not isinstance(ledger_data, dict):
        errors.append("ledger data must be an object")
        return "invalid", "failed"

    ledger_verdict = ledger_data.get("verdict")
    ledger_rule = ledger_data.get("rule_name")
    ledger_reason = ledger_data.get("reason")
    ledger_pack = ledger_data.get("pack")
    ledger_input_hash = ledger_data.get("input_hash")

    if ledger_verdict not in _CANONICAL_VERDICTS:
        errors.append("locked ledger verdict must be one of allow/deny/flag/error")
    if not isinstance(ledger_rule, str):
        errors.append("locked ledger rule_name must be a string")
    if not isinstance(ledger_reason, str):
        errors.append("locked ledger reason must be a string")
    if not isinstance(ledger_pack, dict):
        errors.append("locked ledger pack must be an object")
    if not isinstance(ledger_input_hash, str) or not _HEX64.fullmatch(ledger_input_hash):
        errors.append("locked ledger input_hash must be 64 lowercase hex characters")

    if verdict_value != ledger_verdict:
        errors.append("receipt verdict does not match locked ledger verdict")
    if verdict_rule != ledger_rule:
        errors.append("receipt rule_name does not match locked ledger")
    if verdict_reason != ledger_reason:
        errors.append("receipt reason does not match locked ledger")
    if receipt_pack != ledger_pack:
        errors.append("receipt pack does not match locked ledger")
    if receipt_input_hash != ledger_input_hash:
        errors.append("receipt input hash does not match locked ledger")

    manifest_time = _parse_instant(manifest.get("generated_at"))
    ledger_time = _parse_instant(ledger_entry.get("timestamp"))
    if manifest_time is None or ledger_time is None:
        errors.append("invalid or timezone-naive manifest/ledger timestamp")
    elif manifest_time != ledger_time:
        errors.append("manifest and locked ledger decision time mismatch")

    clock_value = clock.get("value")
    if clock_value == "unset":
        if not allow_unbound_clock:
            errors.append("unbound receipt clock requires explicit --allow-unbound-clock")
            return "unbound-rejected", "unbound"
        return "unbound-opt-in", "unbound"

    receipt_time = _parse_instant(clock_value)
    if receipt_time is None:
        errors.append("invalid or timezone-naive injected receipt clock")
        return "invalid", "failed"
    if manifest_time is not None and receipt_time != manifest_time:
        errors.append("receipt clock does not match locked manifest/ledger time")
        return "invalid", "failed"
    return "injected", "producer_supplied"


def verify(
    bundle: Path,
    allow_unbound_clock: bool = False,
    expected_receipt_sha256: str | None = None,
    trusted_issuer_keys_path: Path | None = None,
) -> dict:
    errors: list[str] = []
    manifest_path = bundle / "manifest.json"
    receipt_path = bundle / "receipt.json"

    for required in (manifest_path, receipt_path):
        if not required.is_file():
            errors.append(f"missing {required.name}")
    if errors:
        return _invalid(errors)

    receipt_sha = sha256_file(receipt_path)
    if expected_receipt_sha256 is not None:
        if not _HEX64.fullmatch(expected_receipt_sha256):
            errors.append("expected receipt sha256 must be 64 lowercase hex characters")
        elif receipt_sha != expected_receipt_sha256:
            errors.append("receipt sha256 does not match expected external commitment")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return _invalid(errors + [f"invalid control JSON: {exc}"], receipt_sha256=receipt_sha)

    if not isinstance(manifest, dict):
        return _invalid(errors + ["manifest must be an object"], receipt_sha256=receipt_sha)
    if not isinstance(receipt, dict):
        return _invalid(errors + ["receipt must be an object"], receipt_sha256=receipt_sha)

    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        return _invalid(errors + ["manifest files must be a non-empty array"], receipt_sha256=receipt_sha)

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
        if not isinstance(expected_bytes, int) or isinstance(expected_bytes, bool) or expected_bytes < 0:
            errors.append(f"manifest file entry {index} has invalid byte count")
            continue

        path = bundle / name
        if not path.is_file():
            errors.append(f"missing manifest file: {name}")
            continue
        if path.is_symlink():
            errors.append(f"manifest file must not be a symlink: {name}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"sha256 mismatch: {name}")
        if path.stat().st_size != expected_bytes:
            errors.append(f"byte count mismatch: {name}")
        digest_lines.append(f"{name}={expected}\n")

    allowed_files = {"manifest.json", "receipt.json", "receipt.sig.json"} | seen_names
    try:
        for child in bundle.iterdir():
            if child.is_symlink():
                errors.append(f"unexpected symlink in bundle: {child.name}")
            elif child.is_file() and child.name not in allowed_files:
                errors.append(f"unexpected bundle file: {child.name}")
    except Exception as exc:
        errors.append(f"bundle member enumeration failed: {exc}")

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

    ledger_members = [
        entry for entry in entries
        if isinstance(entry, dict) and entry.get("name") == "ledger.jsonl"
    ]
    if len(ledger_members) != 1:
        errors.append("ledger.jsonl must appear exactly once in manifest files")

    ledger_entry = verify_ledger(bundle / "ledger.jsonl", errors)
    ledger_head = None
    if isinstance(ledger_entry, dict):
        candidate = ledger_entry.get("record_hash")
        if isinstance(candidate, str) and _HEX64.fullmatch(candidate):
            ledger_head = candidate

    manifest_sha = sha256_file(manifest_path)
    clock_binding, time_authority = _validate_receipt_semantics(
        manifest, receipt, ledger_entry, manifest_sha, errors, allow_unbound_clock
    )

    integrity = "verified" if not errors else "failed"

    try:
        trusted_keys = load_trust_store(trusted_issuer_keys_path)
        issuer_authenticity, issuer_signature = verify_detached_signature(
            bundle / "receipt.sig.json",
            receipt_sha,
            trusted_keys,
        )
    except Exception as exc:
        issuer_authenticity = "failed"
        issuer_signature = {
            "present": (bundle / "receipt.sig.json").is_file(),
            "profile": None,
            "algorithm": None,
            "key_id": None,
            "receipt_sha256_matches": False,
            "key_trusted": False,
            "signature_valid": False,
            "reason": f"trust_store_invalid: {exc}",
        }

    return {
        "status": "valid" if not errors else "invalid",
        "portable": not errors,
        "verifier_version": VERIFIER_VERSION,
        "verification": _dimensions(integrity, time_authority, issuer_authenticity),
        "issuer_signature": issuer_signature,
        "bundle_digest": manifest_bundle,
        "manifest_sha256": manifest_sha,
        "receipt_sha256": receipt_sha,
        "ledger_head": ledger_head,
        "verified_files": len(entries),
        "clock_binding": clock_binding,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERIFIER_VERSION}")
    parser.add_argument("bundle", type=Path)
    parser.add_argument(
        "--allow-unbound-clock",
        action="store_true",
        help="Explicitly accept legacy/local bundles whose receipt clock is 'unset'.",
    )
    parser.add_argument(
        "--expect-receipt-sha256",
        help="Fail closed unless receipt.json matches this externally supplied SHA-256 commitment.",
    )
    parser.add_argument(
        "--trusted-issuer-keys",
        type=Path,
        help="External paygod-ed25519-trust-v1 JSON trust store used for receipt.sig.json.",
    )
    parser.add_argument(
        "--require-issuer-authenticity",
        action="store_true",
        help="Return nonzero unless issuer_authenticity is verified. Does not redefine integrity.",
    )
    parser.add_argument("--result", type=Path, default=Path("verification-result.json"))
    args = parser.parse_args()

    try:
        result = verify(
            args.bundle,
            allow_unbound_clock=args.allow_unbound_clock,
            expected_receipt_sha256=args.expect_receipt_sha256,
            trusted_issuer_keys_path=args.trusted_issuer_keys,
        )
    except Exception as exc:
        result = _invalid([f"verifier failure: {type(exc).__name__}: {exc}"])

    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    integrity_ok = result["status"] == "valid"
    issuer_ok = result.get("verification", {}).get("issuer_authenticity") == "verified"
    return 0 if integrity_ok and (not args.require_issuer_authenticity or issuer_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
