#!/usr/bin/env python3
"""Record an ACTUALLY INVOKED native Trivy scan in a separately signed statement.

Research-only first-party CI instrumentation, not a trusted execution enclave.
The native GH attestations on both report AND statement bind bytes to a pinned
workflow source, but cannot prove independent scanner coverage or factual truth.
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

SHA_SUBJECT=re.compile(r"^.+@sha256:[a-f0-9]{64}$")
SHA40=re.compile(r"^[a-f0-9]{40}$")
ARGS=["image","--scanners","vuln","--format","json","--exit-code","0"]

def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--subject",required=True)
    a.add_argument("--output-dir",required=True,type=Path)
    args=a.parse_args()
    if not SHA_SUBJECT.fullmatch(args.subject):
        raise ValueError("Immutable OCI repository digest is mandatory")
    commit=os.environ.get("GITHUB_SHA","")
    if not SHA40.fullmatch(commit) or os.environ.get("GITHUB_ACTIONS")!="true":
        raise ValueError("Refuse unauthenticated local/unknown Actions identity")
    workflow_ref=os.environ.get("GITHUB_REF","")
    if workflow_ref!="refs/heads/research/trivy-signed-execution-statement-20261016":
        raise ValueError("Workflow source ref unexpected")
    binary=shutil.which("trivy")
    if binary is None:
        raise ValueError("Trivy executable unavailable")
    binary_path=Path(binary).resolve()
    binary_hash=sha(binary_path.read_bytes())
    version=subprocess.run([str(binary_path),"--version"],capture_output=True,text=True,timeout=20,check=True)
    if not re.search(r"\bVersion:\s*0\.75\.0\b",version.stdout):
        raise ValueError("Actual Trivy version does not match expected 0.75.0")

    out=args.output_dir
    out.mkdir(parents=True,exist_ok=True)
    report=out/"trivy.json"
    # Only these executable arguments are permitted in this research witness.
    # No --severity, --ignore-status, ignorefile or skip flags in the invocation.
    argv=[str(binary_path),*ARGS,"--output",str(report),args.subject]
    actual=subprocess.run(argv,capture_output=True,timeout=180,check=False)
    (out/"trivy-stdout.txt").write_bytes(actual.stdout)
    (out/"trivy-stderr.txt").write_bytes(actual.stderr)
    if actual.returncode!=0 or not report.exists():
        raise ValueError("Native Trivy scan failed; no signed execution statement")
    raw=report.read_bytes()
    if not raw or len(raw)>5_000_000:
        raise ValueError("Unexpected/oversized Trivy report")
    parsed=json.loads(raw.decode("utf-8"))
    if parsed.get("ArtifactName")!=args.subject or parsed.get("SchemaVersion")!=2:
        raise ValueError("Native output schema/subject did not match")
    statement={
        "statement_type":"paygod.research.trivy-observed-execution.v0",
        "status":"observed_completed",
        "source_scope":"first_party_github_actions_only",
        "scanner":"Trivy",
        "scanner_version_stdout":version.stdout.strip(),
        "scanner_binary_sha256":binary_hash,
        "scanner_executable":"trivy",
        "argv":["trivy",*ARGS,"--output","native-source/trivy.json",args.subject],
        "native_exit_code":actual.returncode,
        "subject":args.subject,
        "report_sha256":sha(raw),
        "report_size_bytes":len(raw),
        "workflow_repository":os.environ.get("GITHUB_REPOSITORY",""),
        "workflow_ref":workflow_ref,
        "workflow_commit":commit,
        "workflow_run_id":os.environ.get("GITHUB_RUN_ID",""),
        "workflow_run_attempt":os.environ.get("GITHUB_RUN_ATTEMPT",""),
        "scan_completeness_independently_attested":False,
        "source_truth_independently_verified":False,
    }
    (out/"scan-execution.json").write_text(
        json.dumps(statement,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8"
    )
    (out/"subject.txt").write_text(args.subject+"\n",encoding="utf-8")
    print(json.dumps({
        "kind":"NATIVE_TRIVY_EXECUTION_STATEMENT_CREATED",
        "report_sha256":statement["report_sha256"],
        "binary_sha256":binary_hash,
        "source_authenticated":False,
        "statement_signed":False,
        "native_exit_code":actual.returncode,
    },sort_keys=True))
    return 0

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except (ValueError,OSError,TimeoutError,subprocess.SubprocessError,json.JSONDecodeError) as e:
        print(f"WITHHELD_NOT_RUN: {e}",file=sys.stderr)
        raise SystemExit(2)
