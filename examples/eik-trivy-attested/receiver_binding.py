#!/usr/bin/env python3
"""Receiver-side *separate* binding check; no repository checkout or Kernel replay.

Native GitHub attestation and PayGod portable evidence checks MUST also pass
independently. A binding check is neither scanner truth nor authorization.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from verify_portable_evidence import canonical_json  # separately transferred code
from eik_trivy_shadow import examine, no_duplicates
from execution_statement import check as validate_scan_execution

def read_json(path):
    return json.loads(Path(path).read_bytes().decode("utf-8"),
                      object_pairs_hook=no_duplicates,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite JSON")))

def verify(report_file, input_file, receipt_file, statement_file, repo, commit):
    raw=Path(report_file).read_bytes()
    sha=hashlib.sha256(raw).hexdigest()
    report=read_json(report_file)
    statement=read_json(statement_file)
    validate_scan_execution(statement,raw,report['ArtifactName'],repo,commit)
    admitted=read_json(input_file)
    receipt=read_json(receipt_file)
    scan=admitted.get("scan_report",{})
    if not isinstance(scan,dict) or scan.get("source_sha256")!=sha:
        raise ValueError("RAW_SOURCE_DIGEST_NOT_BOUND_TO_INPUT")
    subject=scan.get("artifact_name","")
    shadow=examine(report, subject, 0, ["image","--scanners=vuln","--format=json"],sha)
    if shadow["status"]!="SHADOW_BLOCK_CANDIDATE":
        raise ValueError("REPORT_NOT_ADMISSIBLE_AS_SEVERE_SOURCE")
    normalized=[]
    for f in shadow["findings"]:
        if not isinstance(f["trivy_status"],str) or not f["trivy_status"]:
            raise ValueError("SOURCE_STATUS_MISSING")
        normalized.append({
            "cve_id":f["vulnerability_id"],"severity":f["severity"],
            "installed_version":f["installed_version"],"trivy_status":f["trivy_status"]
        })
    if sorted(scan.keys())!=["artifact_name","source_sha256","vulnerabilities"]:
        raise ValueError("UNEXPECTED_ADMITTED_FIELD")
    if scan["vulnerabilities"]!=normalized:
        raise ValueError("ADMITTED_FINDINGS_DIVERGE_FROM_RAW_TRIVY")
    input_digest=hashlib.sha256(canonical_json(admitted).encode("utf-8")).hexdigest()
    if receipt.get("input",{}).get("canonical_hash") != input_digest:
        raise ValueError("CANONICAL_INPUT_NOT_BOUND_TO_RECEIPT")
    if receipt.get("verdict",{}).get("value")!="deny":
        raise ValueError("NON_DENY_DECISION_IN_RESEARCH_SOURCE")
    return {"report_sha256":sha,"canonical_input_sha256":input_digest,
            "reported_finding_count":len(normalized),
            "high_or_critical":shadow["details"]["high_or_critical"]}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--report",required=True)
    p.add_argument("--input",required=True)
    p.add_argument("--receipt",required=True)
    p.add_argument("--statement",required=True)
    p.add_argument("--repository",required=True)
    p.add_argument("--source-commit",required=True)
    a=p.parse_args()
    try:
        out=verify(a.report,a.input,a.receipt,a.statement,a.repository,a.source_commit)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, RecursionError) as e:
        print("BINDING_FAILED: "+str(e),file=sys.stderr)
        return 2
    print(json.dumps({"status":"BOUNDED_BINDING_VERIFIED",**out,
                      "native_github_attestation":"verify_separately",
                      "canonical_bundle_integrity":"verify_separately",
                      "real_world_source_truth":"not_verified"},sort_keys=True))
    return 0

if __name__=="__main__":
    sys.exit(main())
