#!/usr/bin/env python3
"""Synthetic adversarial fixtures for standalone Trivy shadow diagnostic.

No Trivy executable is invoked here. No Kernel is invoked or permitted to
generate any PayGod bundle/decision. The fixture's claimed scanner status is
NOT external proof and no source acceptance is asserted.
"""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "eik_trivy_shadow.py"
DIGEST = "example.invalid/checkout@sha256:" + "a" * 64

GOOD = {
    "SchemaVersion": 2,
    "ArtifactName": DIGEST,
    "Metadata": {"RepoDigests": [DIGEST]},
    "Results": [{
        "Target": "checkout (alpine 3.21)",
        "Class": "os-pkgs",
        "Type": "alpine",
        "Vulnerabilities": [{
            "VulnerabilityID": "CVE-2099-9001",
            "PkgName": "openssl",
            "InstalledVersion": "3.3.2-r0",
            "FixedVersion": "3.3.3-r0",
            "Status": "fixed",
            "Severity": "CRITICAL"
        }]
    }]
}

def call(file_content, expected_status, reason=None, *, exit_code=0, extra=(),
         expected_artifact=DIGEST):
    with tempfile.TemporaryDirectory(prefix="pg-trivy-shadow-") as tmp:
        file = Path(tmp) / "report.json"
        if isinstance(file_content, bytes):
            file.write_bytes(file_content)
        else:
            file.write_text(json.dumps(file_content), encoding="utf-8")
        p = subprocess.run([
            sys.executable, str(SCRIPT), "--report", str(file),
            "--expected-artifact", expected_artifact,
            "--scanner-exit-code", str(exit_code), *extra
        ], capture_output=True, text=True, check=True)
        out = json.loads(p.stdout)
        assert out["status"] == expected_status, (expected_status, out)
        if reason:
            assert reason in out["reason_codes"], (reason, out)
        assert out["source_attested"] is False
        assert out["kernel_called"] is False
        assert out["paygod_decision"] is None
        assert out["receipt_issued"] is False
        assert len(out["raw_report_sha256"] or "") in (0, 64)
        return out

def main():
    # Core RED counterexample: Trivy Status=fixed is advisory availability.
    out = call(GOOD, "SHADOW_BLOCK_CANDIDATE", "REPORTED_HIGH_OR_CRITICAL")
    assert len(out["findings"]) == 1
    assert out["findings"][0]["trivy_status"] == "fixed"
    assert out["findings"][0]["installed_version"] == "3.3.2-r0"
    assert out["findings"][0]["fixed_version"] == "3.3.3-r0"
    assert out["findings"][0]["remediation_proven"] is False
    print("PASS: raw fixed-status retained; no inferred installed remediation")

    for status in ("affected", "will_not_fix", None):
        item = copy.deepcopy(GOOD)
        item["Results"][0]["Vulnerabilities"][0]["Status"] = status
        call(item, "SHADOW_BLOCK_CANDIDATE", "REPORTED_HIGH_OR_CRITICAL")
    print("PASS: high/critical must not be silently dismissed for any Trivy Status")

    clean = copy.deepcopy(GOOD)
    clean["Results"][0]["Vulnerabilities"] = None
    call(clean, "WITHHELD_NOT_RUN", "SCAN_COMPLETENESS_UNATTESTED")
    clean["Results"][0]["Vulnerabilities"] = []
    call(clean, "WITHHELD_NOT_RUN", "SCAN_COMPLETENESS_UNATTESTED")
    print("PASS: no vulnerabilities does not grant allow without trusted completeness")

    unknown = copy.deepcopy(GOOD)
    unknown["Results"][0]["Vulnerabilities"][0]["Severity"] = "UNKNOWN"
    call(unknown, "WITHHELD_NOT_RUN", "UNKNOWN_SEVERITY")
    missing = copy.deepcopy(GOOD)
    del missing["Results"][0]["Vulnerabilities"][0]["InstalledVersion"]
    call(missing, "WITHHELD_NOT_RUN", "VULNERABILITY_FIELD_MISSING")
    typo = copy.deepcopy(GOOD)
    typo["Results"][0]["Vulnerabilities"][0]["Status"] = False
    call(typo, "WITHHELD_NOT_RUN", "INVALID_TRIVY_STATUS")
    print("PASS: unknown, incomplete and wrong-typed records withheld")

    call(GOOD, "WITHHELD_NOT_RUN", "SCANNER_EXIT_NOT_ZERO", exit_code=4)
    call(GOOD, "WITHHELD_NOT_RUN", "UNSUPPORTED_SCAN_FILTER",
         extra=("--scanner-arg=--ignore-unfixed",))
    call(GOOD, "WITHHELD_NOT_RUN", "UNSUPPORTED_SCAN_FILTER",
         extra=("--scanner-arg=--severity=CRITICAL",))
    call(GOOD, "WITHHELD_NOT_RUN", "SUBJECT_MISMATCH",
         expected_artifact="example.invalid/other@sha256:" + "b" * 64)
    bind = copy.deepcopy(GOOD)
    bind["Metadata"]["RepoDigests"] = []
    call(bind, "WITHHELD_NOT_RUN", "REPO_DIGEST_BINDING_UNPROVEN")
    print("PASS: failed/filtered scan and wrong target are refused")

    call(b'{"SchemaVersion":2,"SchemaVersion":2}', "WITHHELD_NOT_RUN",
         "INVALID_OR_UNAVAILABLE_REPORT")
    call(b'{"SchemaVersion":2,"extra":NaN}', "WITHHELD_NOT_RUN",
         "INVALID_OR_UNAVAILABLE_REPORT")
    wrong_schema = copy.deepcopy(GOOD)
    wrong_schema["SchemaVersion"] = 2.0
    call(wrong_schema, "WITHHELD_NOT_RUN", "UNKNOWN_TRIVY_SCHEMA")
    call(b'\xff\xfe', "WITHHELD_NOT_RUN", "INVALID_OR_UNAVAILABLE_REPORT")
    call(b'{', "WITHHELD_NOT_RUN", "INVALID_OR_UNAVAILABLE_REPORT")
    call((b"[" * 1200) + b"0" + (b"]" * 1200), "WITHHELD_NOT_RUN",
         "INVALID_OR_UNAVAILABLE_REPORT")
    empty = copy.deepcopy(GOOD)
    empty["Results"] = []
    call(empty, "WITHHELD_NOT_RUN", "SCAN_RESULTS_ABSENT")
    print("PASS: duplicate/nonfinite/deep JSON, schema type, bad UTF-8 and empty results withheld")
    print("PASS: all shadow diagnostics are non-authoritative and emit no PayGod artifacts")

if __name__ == "__main__":
    main()
