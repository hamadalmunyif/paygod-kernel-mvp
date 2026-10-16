#!/usr/bin/env python3
"""Genuine public-image Trivy report -> native GH attestation -> structural
admission -> canonical PayGod CLI -> portable receipt (RESEARCH ONLY).

Does NOT attest scanner command, coverage, vendor advisory correctness,
policy ownership or release authorization. Does not mint PayGod artifacts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from eik_trivy_shadow import (MAX_REPORT_BYTES, no_duplicates, examine)  # noqa: E402
from execution_statement import check as validate_scan_execution  # noqa: E402

PACK = Path(__file__).resolve().parent / "pack"
ADMISSION = ROOT / "tools" / "eik_admit.py"
_HEX64 = re.compile(r"^[a-f0-9]{64}$")

def emit(status, code, *, kernel_invoked=False, receipt_sha256=None):
    result = {
        "kind": "EIK_TRIVY_SIGNED_CANONICAL_RESEARCH",
        "status": status, "code": code,
        "kernel_invoked": kernel_invoked,
        "report_provenance": "github_native_verified" if kernel_invoked else "not_claimed",
        "receipt_sha256": receipt_sha256,
        "deployment_authority": "not_claimed",
        "source_completeness": "workflow_observed_not_independently_attested",
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if status == "KERNEL_EXECUTED_NONPERMIT" else 2

def run(*args):
    return subprocess.run(list(args), capture_output=True, text=True,
                          check=False, timeout=90)

def make_input(source, expected, rawsha, reported_exit, scanner_args):
    """Only a conservative severe observation is eligible for this study."""
    candidate = examine(source, expected, reported_exit, scanner_args, rawsha)
    if candidate["status"] != "SHADOW_BLOCK_CANDIDATE":
        raise ValueError("SOURCE_WITHHELD_" + "_".join(candidate["reason_codes"]))
    normalized = []
    for item in candidate["findings"]:
        # Preserve complete observed list, not just the policy-triggering item.
        if not isinstance(item["trivy_status"], str) or not item["trivy_status"]:
            raise ValueError("TRIVY_STATUS_MISSING")
        normalized.append({
            "cve_id": item["vulnerability_id"],
            "severity": item["severity"],
            "installed_version": item["installed_version"],
            "trivy_status": item["trivy_status"],
        })
    if not normalized:
        raise ValueError("NO_REPORTED_FINDINGS")
    return {"scan_report": {
        "artifact_name": expected,
        "source_sha256": rawsha,
        "vulnerabilities": normalized,
    }}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report", required=True, type=Path)
    p.add_argument("--execution-statement", required=True, type=Path)
    p.add_argument("--expected-artifact", required=True)
    p.add_argument("--scanner-exit-code", required=True, type=int)
    p.add_argument("--scanner-arg", action="append", default=[])
    p.add_argument("--repository", required=True, help="GitHub repo owner/name, trust scope for native verification")
    p.add_argument("--cli", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    a=p.parse_args()

    if a.out.exists():
        return emit("WITHHELD_NOT_RUN", "OUTPUT_NOT_FRESH")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", a.repository):
        return emit("WITHHELD_NOT_RUN", "INVALID_REPOSITORY_SCOPE")
    if os.environ.get("GITHUB_ACTIONS") != "true" or os.environ.get("GITHUB_REPOSITORY") != a.repository:
        return emit("WITHHELD_NOT_RUN", "UNTRUSTED_RESEARCH_EXECUTION_CONTEXT")
    if os.environ.get("PAYGOD_STRICT") != "1" or not os.environ.get("PAYGOD_CLOCK"):
        return emit("WITHHELD_NOT_RUN", "DEMO_KERNEL_ENV_MISSING")
    if not a.cli.is_file():
        return emit("WITHHELD_NOT_RUN", "KERNEL_CLI_MISSING")
    try:
        if a.report.stat().st_size > MAX_REPORT_BYTES:
            raise ValueError("REPORT_TOO_LARGE")
        raw=a.report.read_bytes()
        digest=hashlib.sha256(raw).hexdigest()
        source=json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")))
        normalized=make_input(source,a.expected_artifact,digest,a.scanner_exit_code,a.scanner_arg)
    except (OSError, UnicodeError, ValueError, RecursionError) as e:
        return emit("WITHHELD_NOT_RUN", "SOURCE_INVALID_OR_INCOMPLETE")

    # This *actually calls* GitHub native trust verification, not a caller-supplied
    # --source-attested boolean. It signs/verifies REPORT BYTES (not scanner command).
    # GH CLI <=2.101.0 had an inexact --signer-workflow identity match
    # (GHSA-wjmr-j3rp-mh2g); refuse those clients. Pin workflow/ref/source.
    cli_version=run("gh","--version")
    match=re.search(r"gh version (\d+)\.(\d+)\.(\d+)",cli_version.stdout)
    if cli_version.returncode!=0 or not match or tuple(map(int,match.groups()))<(2,102,0):
        return emit("WITHHELD_NOT_RUN", "GH_ATTESTATION_CLI_PATCH_REQUIRED")
    current_commit=os.environ.get("GITHUB_SHA","")
    if not re.fullmatch(r"[a-f0-9]{40}", current_commit):
        return emit("WITHHELD_NOT_RUN", "SIGNER_SOURCE_COMMIT_NOT_PINNED")
    signer=f"{a.repository}/.github/workflows/trivy-attested-canonical-chain.yml"
    verification=run(
        "gh","attestation","verify",str(a.report.resolve()),
        "--repo",a.repository,
        "--signer-workflow",signer,
        "--source-ref","refs/heads/research/trivy-signed-execution-statement-20261016",
        "--source-digest",current_commit,
        "--format","json",
    )
    if verification.returncode != 0:
        return emit("WITHHELD_NOT_RUN", "NATIVE_ATTESTATION_INVALID")
    statement_bytes=a.execution_statement.read_bytes()
    try:
        record=json.loads(statement_bytes.decode("utf-8"),object_pairs_hook=no_duplicates)
        validate_scan_execution(record,raw,a.expected_artifact,a.repository,current_commit)
    except (UnicodeError, ValueError, TypeError, RecursionError):
        return emit("WITHHELD_NOT_RUN", "SCAN_EXECUTION_RECORD_MISMATCH")

    try:
        att=json.loads(verification.stdout)
        if not isinstance(att,list) or not att:
            raise ValueError("missing authenticated attestation")
    except ValueError:
        return emit("WITHHELD_NOT_RUN", "NATIVE_ATTESTATION_UNREADABLE")

    # Structural admission is a SECOND gate and cannot authenticate completeness.
    with tempfile.TemporaryDirectory(prefix="trivy-eik-validated-") as temp:
        inp=Path(temp)/"input.json"
        inp.write_text(json.dumps(normalized,ensure_ascii=True,separators=(",",":"))+"\n",encoding="utf-8")
        admitted=run(sys.executable,str(ADMISSION),"--pack",str(PACK),"--input",str(inp))
        if admitted.returncode != 0:
            return emit("WITHHELD_NOT_RUN", "STRUCTURAL_INPUT_REJECTED")
        try:
            info=json.loads(admitted.stdout)
            if info.get("status")!="STRUCTURAL_ONLY_PASS" or info.get("kernel_invoked") is not False:
                raise ValueError("invalid structural check")
        except (ValueError, AttributeError):
            return emit("WITHHELD_NOT_RUN", "STRUCTURAL_ADMISSION_UNRECOGNIZED")

        # The CLI is the ONLY producer of plan/ledger/manifest/receipt/bundle ID.
        # Input/report/attestation are retained OUTSIDE the canonical evidence dir.
        a.out.mkdir(parents=True,exist_ok=False)
        side=a.out/"source"
        side.mkdir()
        (side/"trivy.json").write_bytes(raw)
        (side/"input.json").write_bytes(inp.read_bytes())
        (side/"gh-attestation-verification.json").write_text(verification.stdout,encoding="utf-8")
        result=run(str(a.cli.resolve()),"run","--pack",str(PACK.resolve()),
                   "--input",str((side/"input.json").resolve()),"--out",str((a.out/"evidence").resolve()))

    receipt_path=a.out/"evidence"/"receipt.json"
    if result.returncode != 0 or not receipt_path.is_file():
        shutil.rmtree(a.out/"evidence",ignore_errors=True)
        return emit("KERNEL_FAILED", "CANONICAL_RUN_FAILED",kernel_invoked=True)
    try:
        receipt=json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt["verdict"]["value"]!="deny":
            raise ValueError("unexpected canonical policy verdict")
        if not _HEX64.fullmatch(digest):
            raise ValueError("unusable source digest")
    except (OSError, ValueError, KeyError, TypeError):
        shutil.rmtree(a.out/"evidence",ignore_errors=True)
        return emit("KERNEL_FAILED", "UNEXPECTED_VERDICT_NO_EVIDENCE_ACCEPTED",kernel_invoked=True)
    return emit("KERNEL_EXECUTED_NONPERMIT","CANONICAL_DENY_AFTER_NATIVE_ATTESTATION",
                kernel_invoked=True,
                receipt_sha256=hashlib.sha256(receipt_path.read_bytes()).hexdigest())

if __name__=="__main__":
    sys.exit(main())
