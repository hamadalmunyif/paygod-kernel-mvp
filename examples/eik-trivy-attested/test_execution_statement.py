#!/usr/bin/env python3
"""Hermetic execution-statement validation only; does not authenticate GH signatures."""
import copy
import hashlib
from execution_statement import check, COMMAND, SOURCE_REF

REPORT=b'{"SchemaVersion":2,"ArtifactName":"synthetic"}'
SUBJECT="example.invalid/app@sha256:"+"a"*64
COMMIT="b"*40
REPO="hamadalmunyif/paygod-kernel-mvp"

def specimen():
    return {
        "statement_type":"paygod.research.trivy-observed-execution.v0",
        "status":"observed_completed",
        "source_scope":"first_party_github_actions_only",
        "scanner":"Trivy",
        "scanner_version_stdout":"Version: 0.75.0",
        "scanner_binary_sha256":"c"*64,
        "scanner_executable":"trivy",
        "argv":COMMAND+[SUBJECT],
        "native_exit_code":0,
        "subject":SUBJECT,
        "report_sha256":hashlib.sha256(REPORT).hexdigest(),
        "report_size_bytes":len(REPORT),
        "workflow_repository":REPO,
        "workflow_ref":SOURCE_REF,
        "workflow_commit":COMMIT,
        "workflow_run_id":"123456",
        "workflow_run_attempt":"1",
        "scan_completeness_independently_attested":False,
        "source_truth_independently_verified":False,
    }

def rejects(case, value):
    sample=specimen()
    if case=="missing":
        del sample["scanner_binary_sha256"]
    elif case=="extra":
        sample["unknown_claim"]="allowed"
    else:
        sample[case]=value
    try:
        check(sample,REPORT,SUBJECT,REPO,COMMIT)
    except ValueError:
        return
    raise AssertionError("Invalid execution statement incorrectly accepted: "+case)

def main():
    assert check(specimen(), REPORT, SUBJECT,REPO,COMMIT)["status"]=="OBSERVED_EXECUTION_STATEMENT_BOUND"
    negatives=[
        ("native_exit_code",1),
        ("native_exit_code",False),
        ("scanner_version_stdout","Version: 0.74.0"),
        ("scanner_binary_sha256","not-a-hash"),
        ("argv",COMMAND+["--severity","HIGH",SUBJECT]),
        ("argv",COMMAND+["example.invalid/wrong@sha256:"+"d"*64]),
        ("report_sha256","0"*64),
        ("report_size_bytes",len(REPORT)+1),
        ("workflow_commit","c"*40),
        ("workflow_repository","another/owner"),
        ("workflow_ref","refs/heads/main"),
        ("workflow_run_attempt","not-number"),
        ("source_truth_independently_verified",True),
        ("scan_completeness_independently_attested",True),
        ("missing",None),
        ("extra",None),
    ]
    for key,val in negatives:
        rejects(key,val)
    try:
        check(specimen(),REPORT+b" ",SUBJECT,REPO,COMMIT)
    except ValueError:
        pass
    else:
        raise AssertionError("Modified raw bytes escaped execution binding")
    print(f"PASS: signed-execution statement structural contract ({len(negatives)+1} negatives). Native GH authentication tested in workflow separately.")

if __name__=="__main__":
    main()
