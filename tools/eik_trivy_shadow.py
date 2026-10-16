#!/usr/bin/env python3
"""Read-only EIK research: cautious Trivy report admission, NEVER a Kernel decision.

This does not invoke PayGod CLI, mint a receipt or prove scanner provenance.
A self-reported exit code / invocation supplied by the caller is *not* trusted
scanner-execution evidence. Only a separately authenticated producer witness
can satisfy a real-world release admission requirement.

See examples/eik-trivy-readonly/README.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SHA256_SUBJECT = re.compile(r"^.+@sha256:[a-f0-9]{64}$")
SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"}
FORBIDDEN_SCAN_SWITCHES = {
    "--ignore-unfixed", "--ignore-status", "--severity",
    "--skip-files", "--skip-dirs", "--ignorefile",
}
MAX_REPORT_BYTES = 5_000_000
MAX_FINDINGS = 50_000

class DuplicateKeyError(ValueError):
    pass

def no_duplicates(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise DuplicateKeyError("duplicate key")
        result[k] = v
    return result

def output(status, reasons, source_digest=None, findings=None, extra=None):
    return {
        "kind": "EIK_TRIVY_SHADOW_DIAGNOSTIC",
        "version": "0.1-research",
        "status": status,
        "reason_codes": reasons,
        "raw_report_sha256": source_digest,
        "findings": findings or [],
        "details": extra or {},
        "source_attested": False,
        "kernel_called": False,
        "paygod_decision": None,
        "receipt_issued": False,
    }

def examine(data, expected_artifact, exit_code, command_args, source_digest):
    if exit_code != 0:
        return output("WITHHELD_NOT_RUN", ["SCANNER_EXIT_NOT_ZERO"], source_digest)
    if any(
        arg.split("=")[0] in FORBIDDEN_SCAN_SWITCHES
        for arg in command_args
    ):
        return output("WITHHELD_NOT_RUN", ["UNSUPPORTED_SCAN_FILTER"], source_digest)
    if not isinstance(data, dict) or type(data.get("SchemaVersion")) is not int or data["SchemaVersion"] != 2:
        return output("WITHHELD_NOT_RUN", ["UNKNOWN_TRIVY_SCHEMA"], source_digest)
    if not isinstance(data.get("ArtifactName"), str) or data["ArtifactName"] != expected_artifact:
        return output("WITHHELD_NOT_RUN", ["SUBJECT_MISMATCH"], source_digest)
    if not SHA256_SUBJECT.fullmatch(expected_artifact):
        return output("WITHHELD_NOT_RUN", ["SUBJECT_NOT_DIGEST_PINNED"], source_digest)
    metadata = data.get("Metadata")
    repo_digests = metadata.get("RepoDigests") if isinstance(metadata, dict) else None
    if not isinstance(repo_digests, list) or expected_artifact not in repo_digests:
        return output("WITHHELD_NOT_RUN", ["REPO_DIGEST_BINDING_UNPROVEN"], source_digest)
    if type(data.get("Results")) is not list or not data["Results"]:
        return output("WITHHELD_NOT_RUN", ["SCAN_RESULTS_ABSENT"], source_digest)

    findings = []
    total = 0
    incomplete = False
    for result in data["Results"]:
        if not isinstance(result, dict) or not isinstance(result.get("Target"), str) or not result["Target"]:
            return output("WITHHELD_NOT_RUN", ["INVALID_SCAN_TARGET"], source_digest)
        vulns = result.get("Vulnerabilities")
        if vulns is None:
            continue  # Documented Trivy clean target, NOT proof scan completeness.
        if not isinstance(vulns, list):
            return output("WITHHELD_NOT_RUN", ["INVALID_VULNERABILITY_LIST"], source_digest)
        for v in vulns:
            total += 1
            if total > MAX_FINDINGS:
                return output("WITHHELD_NOT_RUN", ["FINDINGS_LIMIT_EXCEEDED"], source_digest)
            if not isinstance(v, dict):
                return output("WITHHELD_NOT_RUN", ["INVALID_VULNERABILITY_ENTRY"], source_digest)
            for required in ("VulnerabilityID", "PkgName", "InstalledVersion", "Severity"):
                if not isinstance(v.get(required), str) or not v[required]:
                    return output("WITHHELD_NOT_RUN", ["VULNERABILITY_FIELD_MISSING"], source_digest)
            severity = v["Severity"]
            if severity not in SEVERITIES:
                return output("WITHHELD_NOT_RUN", ["UNSUPPORTED_SEVERITY"], source_digest)
            if severity == "UNKNOWN":
                incomplete = True
            status = v.get("Status")
            if status is not None and not isinstance(status, str):
                return output("WITHHELD_NOT_RUN", ["INVALID_TRIVY_STATUS"], source_digest)
            fixed = v.get("FixedVersion")
            if fixed is not None and not isinstance(fixed, str):
                return output("WITHHELD_NOT_RUN", ["INVALID_FIXED_VERSION"], source_digest)
            findings.append({
                "target": result["Target"],
                "vulnerability_id": v["VulnerabilityID"],
                "package_name": v["PkgName"],
                "installed_version": v["InstalledVersion"],
                "trivy_status": status,
                "fixed_version": fixed,
                "severity": severity,
                "remediation_proven": False,
            })

    # Trivy.Status=fixed means an available fix; findings remain present.
    # We only identify a conservative shadow candidate to *block* on severity;
    # the scanner's optional CVSS scores were not interpreted as PayGod policy.
    severe = sum(f["severity"] in ("HIGH", "CRITICAL") for f in findings)
    if incomplete:
        return output("WITHHELD_NOT_RUN", ["UNKNOWN_SEVERITY"], source_digest,
                      findings, {"high_or_critical": severe})
    if severe:
        return output("SHADOW_BLOCK_CANDIDATE", ["REPORTED_HIGH_OR_CRITICAL"], source_digest,
                      findings, {"high_or_critical": severe, "fix_available_is_not_fixed": True})
    # Absence of a high/critical finding is not independently evidenced
    # completion, non-filtering or source authenticity. In particular NO ALLOW.
    return output("WITHHELD_NOT_RUN", ["SCAN_COMPLETENESS_UNATTESTED"], source_digest,
                  findings, {"high_or_critical": 0})

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--expected-artifact", required=True)
    parser.add_argument("--scanner-exit-code", type=int, required=True)
    parser.add_argument("--scanner-arg", action="append", default=[])
    a = parser.parse_args()

    digest = None
    try:
        report = Path(a.report)
        if report.stat().st_size > MAX_REPORT_BYTES:
            result = output("WITHHELD_NOT_RUN", ["REPORT_TOO_LARGE"])
        else:
            raw = report.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            data = json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=no_duplicates,
                parse_constant=lambda _: (_ for _ in ()).throw(
                    ValueError("non-finite number is not JSON")
                ),
            )
            result = examine(data, a.expected_artifact, a.scanner_exit_code,
                             a.scanner_arg, digest)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RecursionError):
        result = output("WITHHELD_NOT_RUN", ["INVALID_OR_UNAVAILABLE_REPORT"], digest)

    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
    return 0  # A diagnostic classification, never permission to release.

if __name__ == "__main__":
    raise SystemExit(main())
