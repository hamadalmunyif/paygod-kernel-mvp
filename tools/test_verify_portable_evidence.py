#!/usr/bin/env python3
import json
from pathlib import Path
import tempfile
import unittest

from verify_portable_evidence import canonical_json, verify


class VerifierRegressionTests(unittest.TestCase):
    def test_canonical_json_matches_producer_unicode_behavior(self):
        value = {"text": "e\u0301", "arabic": "سلام"}
        self.assertEqual(
            canonical_json(value),
            '{"arabic":"\\u0633\\u0644\\u0627\\u0645","text":"\\u00e9"}',
        )

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
            (root / "ledger.jsonl").write_text("", encoding="utf-8")
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
            self.assertTrue(result["errors"])


if __name__ == "__main__":
    unittest.main()
