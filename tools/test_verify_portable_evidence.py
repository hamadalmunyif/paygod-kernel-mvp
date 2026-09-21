#!/usr/bin/env python3
import json
from pathlib import Path
import tempfile
import unittest

from tools.verify_portable_evidence import canonical_json, verify


class VerifierRegressionTests(unittest.TestCase):
    def test_canonical_json_matches_producer_unicode_behavior(self):
        value = {"text": "e\\u0301", "arabic": "سلام"}
        self.assertEqual(
            canonical_json(value),
            '{"arabic":"\\\\u0633\\\\u0644\\\\u0627\\\\u0645","text":"\\\\u00e9"}',
        )

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
