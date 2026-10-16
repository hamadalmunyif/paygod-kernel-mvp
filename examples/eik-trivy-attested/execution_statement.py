"""Validate independently GH-attested *observed* Trivy execution statement.

Pure validation, no authority to declare scanner coverage or issue a decision.
This helper is copied to no-checkout receivers. Caller must verify a valid
GH-native attestation on the exact statement BYTES (and on raw report) first.
"""
from __future__ import annotations
import hashlib
import re

SHA64=re.compile(r"^[a-f0-9]{64}$")
SHA40=re.compile(r"^[a-f0-9]{40}$")
SUBJECT=re.compile(r"^.+@sha256:[a-f0-9]{64}$")
SOURCE_REF="refs/heads/research/trivy-signed-execution-statement-20261016"
COMMAND=["trivy","image","--scanners","vuln","--format","json",
         "--exit-code","0","--output","native-source/trivy.json"]

def check(record:object, report:bytes, subject:str, repo:str, commit:str,
          expected_run_id:str, expected_run_attempt:str):
    if not isinstance(record,dict):
        raise ValueError("EXECUTION_STATEMENT_NOT_OBJECT")
    fields={
        "statement_type","status","source_scope","scanner","scanner_version_stdout",
        "scanner_binary_sha256","scanner_executable","argv","native_exit_code",
        "subject","report_sha256","report_size_bytes","workflow_repository",
        "workflow_ref","workflow_commit","workflow_run_id","workflow_run_attempt",
        "scan_completeness_independently_attested","source_truth_independently_verified",
    }
    if set(record)!=fields:
        raise ValueError("STATEMENT_FIELDS_MISSING_OR_UNEXPECTED")
    if not SUBJECT.fullmatch(subject) or not SHA40.fullmatch(commit):
        raise ValueError("EXPECTED_SUBJECT_OR_COMMIT_INVALID")
    exact={
        "statement_type":"paygod.research.trivy-observed-execution.v0",
        "status":"observed_completed",
        "source_scope":"first_party_github_actions_only",
        "scanner":"Trivy",
        "scanner_executable":"trivy",
        "native_exit_code":0,
        "subject":subject,
        "workflow_repository":repo,
        "workflow_ref":SOURCE_REF,
        "workflow_commit":commit,
        "scan_completeness_independently_attested":False,
        "source_truth_independently_verified":False,
    }
    for key,expected in exact.items():
        if type(record[key]) is not type(expected) or record[key]!=expected:
            raise ValueError("STATEMENT_FIELD_MISMATCH:"+key)
    if record["argv"]!=COMMAND+[subject]:
        raise ValueError("UNEXPECTED_TRIVY_COMMAND")
    if not isinstance(record["scanner_version_stdout"],str) or not re.search(
        r"\bVersion:\s*0\.75\.0\b",record["scanner_version_stdout"]
    ):
        raise ValueError("UNSUPPORTED_TRIVY_VERSION")
    if not isinstance(record["scanner_binary_sha256"],str) or not SHA64.fullmatch(record["scanner_binary_sha256"]):
        raise ValueError("TRIVY_EXECUTABLE_DIGEST_MISSING")
    if type(record["report_size_bytes"]) is not int or record["report_size_bytes"]!=len(report):
        raise ValueError("REPORT_LENGTH_NOT_BOUND")
    if not isinstance(record["report_sha256"],str) or record["report_sha256"]!=hashlib.sha256(report).hexdigest():
        raise ValueError("RAW_REPORT_SHA_MISMATCH")
    if not isinstance(record["workflow_run_id"],str) or not record["workflow_run_id"].isdigit():
        raise ValueError("RUN_ID_NOT_BOUND")
    if not isinstance(record["workflow_run_attempt"],str) or not record["workflow_run_attempt"].isdigit():
        raise ValueError("RUN_ATTEMPT_NOT_BOUND")
    # An attested file from another run of the SAME commit/ref must not
    # satisfy this particular test. For a third party these expected values
    # need an independently pinned statement, not producer-supplied strings.
    if (not isinstance(expected_run_id,str) or not expected_run_id.isdigit() or
        not isinstance(expected_run_attempt,str) or not expected_run_attempt.isdigit()):
        raise ValueError("EXPECTED_RUN_SCOPE_INVALID")
    if record["workflow_run_id"]!=expected_run_id:
        raise ValueError("EXECUTION_RUN_ID_MISMATCH")
    if record["workflow_run_attempt"]!=expected_run_attempt:
        raise ValueError("EXECUTION_RUN_ATTEMPT_MISMATCH")
    return {
        "status":"OBSERVED_EXECUTION_STATEMENT_BOUND",
        "statement_sha256":None, # caller fills digest only if needed; no signing here
        "report_sha256":record["report_sha256"],
        "scanner_binary_sha256":record["scanner_binary_sha256"],
        "source_completeness":"not_independently_attested",
    }
