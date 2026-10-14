#!/usr/bin/env python3
"""Synthetic saved-report -> admission -> canonical CLI evidence.

No GitHub API access, live scanner, external mutation, authorization, or local
decision/receipt construction. The original report's SHA is producer-asserted
metadata, NOT a verifier-validated source authenticity guarantee.
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

REPO_ROOT = Path(__file__).resolve().parents[2]
PACK = Path(__file__).resolve().parent / "pack"
ADMIT = REPO_ROOT / "tools" / "eik_admit.py"
EXPECTED_FIELDS = {
    "fixture_kind", "scanner", "run_state", "scanner_result",
    "scanner_exit_code", "report_complete", "source_commit",
    "findings_count", "critical_count",
}
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")


def emit(status: str, code: str, detail: str, **extra: object) -> int:
    print(json.dumps({
        "eik_reference": "synthetic-github-actions-v0",
        "status": status,
        "code": code,
        "detail": detail,
        "source_authenticity": "not_verified",
        "deployment_authority": "not_claimed",
        **extra,
    }, sort_keys=True))
    return 0 if status == "KERNEL_EXECUTED" else 2


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for name, item in pairs:
        if name in value:
            raise ValueError(f"duplicate JSON field: {name}")
        value[name] = item
    return value


def reject_number(value: str) -> object:
    raise ValueError(f"unsupported numeric representation: {value}")


def admissible_source(source_bytes: bytes) -> tuple[dict[str, object], dict[str, object]]:
    raw = json.loads(
        source_bytes.decode("utf-8"),
        object_pairs_hook=no_duplicates,
        parse_float=reject_number,
        parse_constant=reject_number,
    )
    if not isinstance(raw, dict) or set(raw) != EXPECTED_FIELDS:
        raise ValueError("required source fields missing or unknown source fields")
    if raw["fixture_kind"] != "paygod-eik-synthetic-scan-v0":
        raise ValueError("this reference accepts synthetic saved reports only")
    if raw["scanner"] != "synthetic-ci-scan":
        raise ValueError("scanner kind unsupported")
    if raw["run_state"] != "completed" or raw["scanner_result"] != "ok":
        raise ValueError("source scanner did not complete successfully")
    if type(raw["scanner_exit_code"]) is not int or raw["scanner_exit_code"] != 0:
        raise ValueError("source scanner exit code is not success")
    if raw["report_complete"] is not True:
        raise ValueError("source report is not complete")
    if not isinstance(raw["source_commit"], str) or not COMMIT_RE.fullmatch(raw["source_commit"]):
        raise ValueError("source commit is not an exact hex SHA")
    findings, critical = raw["findings_count"], raw["critical_count"]
    if type(findings) is not int or type(critical) is not int or not (0 <= critical <= findings <= 1000000):
        raise ValueError("finding counts missing, noninteger, negative or inconsistent")
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    admitted = {
        "scan_report": {
            "secrets_found": findings,
            "critical_count": critical,
            "completed": True,
            "scanner_status": "completed",
            "source_sha256": source_hash,
            "source_commit": raw["source_commit"],
        }
    }
    note = {
        "raw_source_sha256": source_hash,
        "admission": "source-shape-and-declared-completion-only",
        "source_authenticity": "not_verified",
        "source_truth": "not_verified",
        "source_clock": "not_independently_verified",
        "raw_source_in_canonical_bundle": False,
    }
    return admitted, note


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Existing authorized local synthetic report JSON")
    parser.add_argument("--cli", required=True, type=Path, help="Path to built canonical PayGod CLI")
    parser.add_argument("--out", required=True, type=Path, help="New output directory; must not exist")
    args = parser.parse_args()

    if args.out.exists():
        return emit("WITHHELD_NOT_RUN", "OUTPUT_EXISTS", "output path exists; refusing stale evidence reuse",
                    kernel_invoked=False)
    try:
        source_bytes = args.source.read_bytes()
        admitted, note = admissible_source(source_bytes)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return emit("WITHHELD_NOT_RUN", "SOURCE_REJECTED", str(exc), kernel_invoked=False)

    with tempfile.TemporaryDirectory(prefix="eik-admission-") as tmp:
        staged = Path(tmp) / "input.json"
        staged.write_text(json.dumps(admitted, indent=2) + "\n", encoding="utf-8")
        check = subprocess.run(
            [sys.executable, str(ADMIT), "--pack", str(PACK), "--input", str(staged)],
            capture_output=True, text=True, check=False,
        )
        if check.returncode != 0:
            return emit("WITHHELD_NOT_RUN", "STRUCTURAL_ADMISSION_REJECTED",
                        check.stdout.strip() or check.stderr.strip(), kernel_invoked=False)

        try:
            shape = json.loads(check.stdout)
            if shape.get("status") != "STRUCTURAL_ONLY_PASS":
                raise ValueError("structural admission was not a pass")
        except (ValueError, AttributeError):
            return emit("WITHHELD_NOT_RUN", "STRUCTURAL_ADMISSION_UNREADABLE",
                        "unrecognized structural admission report", kernel_invoked=False)

        if not args.cli.is_file():
            return emit("WITHHELD_NOT_RUN", "CLI_MISSING", "canonical CLI path missing", kernel_invoked=False)
        if not os.environ.get("PAYGOD_CLOCK"):
            return emit("WITHHELD_NOT_RUN", "DEMO_CLOCK_REQUIRED",
                        "set an explicit producer-supplied PAYGOD_CLOCK for this reference", kernel_invoked=False)

        args.out.mkdir(parents=True, exist_ok=False)
        (args.out / "input.json").write_bytes(staged.read_bytes())
        (args.out / "source-report.json").write_bytes(source_bytes)
        (args.out / "admission-note.json").write_text(json.dumps(note, indent=2) + "\n", encoding="utf-8")
        run = subprocess.run(
            [str(args.cli.resolve()), "run", "--pack", str(PACK.resolve()),
             "--input", str((args.out / "input.json").resolve()),
             "--out", str((args.out / "evidence").resolve())],
            capture_output=True, text=True, check=False, env=os.environ.copy(),
        )
    if run.returncode != 0 or not (args.out / "evidence" / "receipt.json").is_file():
        # The only writer of canonical outputs is the CLI. Do not retain a partial bundle.
        shutil.rmtree(args.out / "evidence", ignore_errors=True)
        return emit("KERNEL_FAILED", "CANONICAL_RUN_FAILED",
                    f"CLI return code {run.returncode}; no evidence accepted", kernel_invoked=True)
    digest = hashlib.sha256((args.out / "evidence" / "receipt.json").read_bytes()).hexdigest()
    return emit("KERNEL_EXECUTED", "CANONICAL_OUTPUT", "synthetic fixture only",
                kernel_invoked=True, receipt_sha256=digest, source_sha256=note["raw_source_sha256"])


if __name__ == "__main__":
    sys.exit(main())
