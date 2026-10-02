#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from verify_portable_evidence import (
    SAFE_INTEGER_MAX,
    canonical_json,
    sha256_bytes,
    verify,
)


def _write_valid_bundle(root: Path) -> tuple[str, str]:
    run_ts = "2026-02-15T00:00:00+00:00"
    pack = {
        "name": "test-pack",
        "version": "0.1.0",
        "path": "packs/test-pack",
        "digest_sha256": "1" * 64,
    }
    input_hash = "2" * 64
    ledger_data = {
        "verdict": "allow",
        "rule_name": "test-rule",
        "reason": "test reason",
        "pack": pack,
        "input_hash": input_hash,
        "evidence_refs": [],
    }
    ledger_payload = {
        "previous_hash": "0" * 64,
        "timestamp": run_ts,
        "data": ledger_data,
    }
    ledger_head = sha256_bytes(canonical_json(ledger_payload).encode("utf-8"))
    ledger = {
        "entry_index": 0,
        "timestamp": run_ts,
        "previous_hash": "0" * 64,
        "data": ledger_data,
        "record_hash": ledger_head,
    }
    ledger_path = root / "ledger.jsonl"
    ledger_path.write_text(json.dumps(ledger, separators=(",", ":")) + "\n", encoding="utf-8")

    findings_path = root / "findings.json"
    findings_path.write_text('{"kind":"FindingsReport"}\n', encoding="utf-8")

    entries = []
    for path in sorted([findings_path, ledger_path], key=lambda p: p.name):
        entries.append({
            "name": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    bundle_digest = hashlib.sha256(
        "".join(f"{x['name']}={x['sha256']}\n" for x in entries).encode("utf-8")
    ).hexdigest()
    manifest = {
        "api_version": "paygod/v1",
        "kind": "Manifest",
        "generated_at": run_ts,
        "pack": pack,
        "input": {"canonical_hash": input_hash},
        "bundle": {
            "algorithm": "sha256",
            "digest_method": "sha256(join_lines(name='name=sha256' sorted by name))",
            "file_count": len(entries),
            "bundle_digest": bundle_digest,
        },
        "files": entries,
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()

    receipt = {
        "api_version": "paygod/v1",
        "kind": "Receipt",
        "spec_version": "0.2.0",
        "generated_at": run_ts,
        "clock": {"value": run_ts, "source": "env:PAYGOD_CLOCK"},
        "canonicalization": {
            "json": "paygod-c14n-v1",
            "schema_manifest_sha256": "0" * 64,
        },
        "runner": {"image": "paygod/runner:test", "image_digest": "unknown"},
        "pack": pack,
        "input": {"canonical_hash": input_hash},
        "bundle": {
            "bundle_digest": bundle_digest,
            "manifest_sha256": manifest_sha,
            "files": entries,
        },
        "verdict": {"value": "allow", "rule_name": "test-rule", "reason": "test reason"},
        "replay": {"command": "not executed by verifier"},
    }
    receipt_path = root / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    return receipt_sha, ledger_head


class VerifierRegressionTests(unittest.TestCase):
    def test_profile_preserves_arabic_and_decomposed_string_values(self):
        value = {"arabic": "سلام", "text": "e\u0301"}
        self.assertEqual(
            canonical_json(value),
            '{"arabic":"\\u0633\\u0644\\u0627\\u0645","text":"e\\u0301"}',
        )

    def test_profile_rejects_float(self):
        with self.assertRaisesRegex(ValueError, "floating-point"):
            canonical_json({"amount": 0.1})

    def test_profile_rejects_unsafe_integer(self):
        with self.assertRaisesRegex(ValueError, "safe range"):
            canonical_json({"amount": SAFE_INTEGER_MAX + 1})

    def test_profile_rejects_non_nfc_property_name(self):
        with self.assertRaisesRegex(ValueError, "not NFC"):
            canonical_json({"e\u0301": "value"})

    def test_valid_bundle_exposes_scoped_verification_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt_sha, ledger_head = _write_valid_bundle(root)
            result = verify(root, expected_receipt_sha256=receipt_sha)
            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "not_verified")
            self.assertEqual(result["verification"]["replay"], "not_performed")
            self.assertEqual(result["verification"]["time_authority"], "producer_supplied")
            self.assertEqual(result["receipt_sha256"], receipt_sha)
            self.assertEqual(result["ledger_head"], ledger_head)

    def test_expected_receipt_sha_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_valid_bundle(root)
            result = verify(root, expected_receipt_sha256="f" * 64)
            self.assertEqual(result["status"], "invalid")
            self.assertTrue(any("expected external commitment" in e for e in result["errors"]))

    def test_unexpected_bundle_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_valid_bundle(root)
            (root / ".DS_Store").write_bytes(b"noise")
            result = verify(root)
            self.assertEqual(result["status"], "invalid")
            self.assertTrue(any("unexpected bundle file: .DS_Store" in e for e in result["errors"]))

    def test_wrong_canonicalization_declaration_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_valid_bundle(root)
            receipt_path = root / "receipt.json"
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["canonicalization"]["json"] = "rfc8785"
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
            result = verify(root)
            self.assertEqual(result["status"], "invalid")
            self.assertTrue(any("canonicalization declaration mismatch" in e for e in result["errors"]))

    def test_missing_manifest_locked_ledger_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = {
                "api_version": "paygod/v1",
                "kind": "Manifest",
                "generated_at": "2026-02-15T00:00:00+00:00",
                "pack": {},
                "input": {},
                "bundle": {
                    "algorithm": "sha256",
                    "file_count": 1,
                    "bundle_digest": "0" * 64,
                },
                "files": [{
                    "name": "findings.json",
                    "sha256": "0" * 64,
                    "bytes": 0,
                }],
            }
            (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (root / "receipt.json").write_text("{}", encoding="utf-8")
            (root / "findings.json").write_bytes(b"")
            result = verify(root)
            self.assertEqual(result["status"], "invalid")
            self.assertTrue(any("ledger.jsonl must appear exactly once" in e for e in result["errors"]))

    def test_malformed_manifest_returns_machine_readable_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "manifest.json").write_text(
                json.dumps({"files": 1}), encoding="utf-8"
            )
            (root / "receipt.json").write_text("{}", encoding="utf-8")
            result = verify(root)
            self.assertEqual(result["status"], "invalid")
            self.assertFalse(result["portable"])
            self.assertEqual(result["verification"]["integrity"], "failed")
            self.assertTrue(result["errors"])


if __name__ == "__main__":
    unittest.main()
