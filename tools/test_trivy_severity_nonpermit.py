#!/usr/bin/env python3
"""Prove the research severity prototype is non-permitting and its input schema
rejects absent/malformed fields BEFORE Kernel invocation. Not source authentication.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "examples" / "eik-trivy-severity-prototype"
ADMISSION = ROOT / "tools" / "eik_admit.py"

def main():
    pack = yaml.safe_load((PACK_DIR / "pack.yaml").read_text(encoding="utf-8"))
    assert pack["metadata"]["version"].split(".")[0] == "2"
    rules = pack["spec"]["policy"]["rules"]
    assert rules and all(r["decision"] != "allow" for r in rules)
    assert {r["decision"] for r in rules} == {"deny", "flag"}
    for case in yaml.safe_load((PACK_DIR / "tests" / "cases.yaml").read_text(encoding="utf-8"))["cases"]:
        assert case["expected"]["decision"] != "allow", case["name"]

    good = {
        "scan_report": {
            "artifact_name": "registry.example/fixture@sha256:" + "a" * 64,
            "vulnerabilities": [{
                "cve_id": "CVE-2099-0001", "severity": "HIGH",
                "installed_version": "3.3.7-r1", "trivy_status": "fixed",
            }],
        }
    }
    bad_cases = [
        {},
        {"scan_report": {}},
        {"scan_report": {"artifact_name": good["scan_report"]["artifact_name"]}},
        {"scan_report": {"artifact_name": "tag:latest", "vulnerabilities": []}},
        {"scan_report": {"artifact_name": good["scan_report"]["artifact_name"],
                         "vulnerabilities": [{"cve_id": "CVE-2099-0001",
                                              "severity": True,
                                              "installed_version": "3.3.7-r1",
                                              "trivy_status": "fixed"}]}},
        {"scan_report": {"artifact_name": good["scan_report"]["artifact_name"],
                         "vulnerabilities": [{"cve_id": "CVE-2099-0001",
                                              "severity": "HIGH",
                                              "installed_version": "3.3.7-r1"}]}},
        {"scan_report": {"artifact_name": good["scan_report"]["artifact_name"],
                         "vulnerabilities": [{"cve_id": "CVE-2099-0001",
                                              "severity": "PATCHED",
                                              "installed_version": "3.3.7-r1",
                                              "trivy_status": "fixed"}]}},
    ]
    with tempfile.TemporaryDirectory(prefix="paygod-trivy-nonpermit-") as d:
        f = Path(d) / "input.json"
        for name, value, expected_status, exit_code in [
            ("well-typed-high", good, "STRUCTURAL_ONLY_PASS", 0),
            *[(f"invalid-{i}", v, "WITHHELD_NOT_RUN", 2)
              for i, v in enumerate(bad_cases)],
        ]:
            f.write_text(json.dumps(value), encoding="utf-8")
            r = subprocess.run([sys.executable, str(ADMISSION), "--pack",
                                str(PACK_DIR), "--input", str(f)],
                               capture_output=True, text=True)
            assert r.returncode == exit_code, (name, r.stdout, r.stderr)
            result = json.loads(r.stdout)
            assert result["status"] == expected_status, (name, result)
            assert result["kernel_invoked"] is False
            assert result["source_authenticity"] == "not_verified"
            assert result["source_completion"] == "not_verified"
            print(f"PASS {name}: {expected_status}, no Kernel called")

    print("PASS: research v2 Pack has no allow rule; structural admission is opt-in, not source proof")

if __name__ == "__main__":
    main()
