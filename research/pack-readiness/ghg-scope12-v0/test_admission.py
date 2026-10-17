#!/usr/bin/env python3
"""Isolated negative admission cases. Does not imply physical-source provenance."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ghg_admit", HERE / "admit.py")
admit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admit)
GOOD = json.loads((HERE / "fixtures" / "complete-synthetic.json").read_text(encoding="utf-8"))


def check(obj):
    return admit.check_payload(json.dumps(obj, ensure_ascii=False).encode("utf-8"))


class Scope12AdmissionResearchTests(unittest.TestCase):
    def test_complete_synthetic_passes_shape_only(self):
        self.assertEqual(check(GOOD), [])
        item = copy.deepcopy(GOOD)
        item["ghg_report"]["scope1_kgco2e"] = 0
        self.assertEqual(check(item), [], "zero is a legitimate integer, not missing")

    def test_missing_and_incorrect_required_fields_fail_closed(self):
        for key in ("reporting_year", "scope1_kgco2e", "scope2_kgco2e",
                    "methodology_ref", "emission_factor_refs", "evidence_refs"):
            with self.subTest(field=key):
                item = copy.deepcopy(GOOD)
                del item["ghg_report"][key]
                self.assertTrue(check(item))
        for key, value in [
            ("scope1_kgco2e", "100000"),
            ("scope2_kgco2e", True),
            ("scope1_kgco2e", -1),
            ("scope1_kgco2e", 9007199254740992),
            ("reporting_year", "2025"),
            ("methodology_ref", ""),
            ("methodology_ref", "https://example.com/claimed"),
            ("emission_factor_refs", []),
            ("evidence_refs", [""]),
            ("evidence_refs", ["ref:e/1", "ref:e/1"]),
        ]:
            with self.subTest(key=key, value=value):
                item = copy.deepcopy(GOOD)
                item["ghg_report"][key] = value
                self.assertTrue(check(item))

    def test_no_silent_rounding_exponent_nans_or_duplicate_keys(self):
        original = json.dumps(GOOD)
        bad = [
            original.replace("100000", "100000.25"),
            original.replace("100000", "1e5"),
            original.replace("100000", "NaN"),
            original.replace('"reporting_year": 2025', '"reporting_year": 2025, "reporting_year": 2024'),
            '{"ghg_report":{"reporting_year":2025,"scope1_kgco2e":100000}}',
            '[]',
            '{"ghg_report":null}',
        ]
        for raw in bad:
            with self.subTest(raw=raw[:100]):
                self.assertTrue(admit.check_payload(raw.encode("utf-8")))

    def test_unknown_fields_and_malformed_utf8_fail(self):
        item = copy.deepcopy(GOOD)
        item["ghg_report"]["unreviewed_metadata"] = "pass"
        self.assertTrue(check(item))
        self.assertTrue(admit.check_payload(b"\xff"))
        self.assertTrue(admit.check_payload(b" " * (admit.MAX_BYTES + 1)))

    def test_invalid_input_never_launches_kernel(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            input_path = tmp / "bad.json"
            input_path.write_text('{"ghg_report":{"scope1_kgco2e":1.5}}', encoding="utf-8")
            out = tmp / "artifacts"
            cmd = [sys.executable, str(HERE / "admit.py"), "--input", str(input_path),
                   "--cli", str(tmp / "nonexistent-cli"), "--out", str(out)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["admission"], "WITHHELD")
            self.assertEqual(data["kernel"], "NOT_RUN")
            self.assertFalse(out.exists())

    def test_shape_only_does_not_claim_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "good.json"
            p.write_text(json.dumps(GOOD), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(HERE / "admit.py"), "--input", str(p)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            outcome = json.loads(result.stdout)
            self.assertEqual(outcome["admission"], "SHAPE_PASSED_ONLY")
            self.assertEqual(outcome["kernel"], "NOT_RUN")
            self.assertNotIn("verdict", outcome)


if __name__ == "__main__":
    unittest.main()
