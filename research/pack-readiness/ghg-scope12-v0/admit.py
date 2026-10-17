#!/usr/bin/env python3
"""Experimental GHG Scope 1/2 pre-kernel shape admission; never mints a verdict.

NOT production security enforcement: direct CLI invocation can bypass this opt-in
wrapper, and no cryptographic provenance/measurement authenticity is established.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SCHEMA = HERE / "input.schema.json"
PACK = REPO_ROOT / "packs" / "core" / "ghg-scope-1-2-guard"
MAX_BYTES = 256 * 1024


class AdmissionError(ValueError):
    pass


def reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise AdmissionError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def reject_float(value):
    raise AdmissionError(f"fractional/exponent JSON number not admitted: {value}")


def reject_constant(value):
    raise AdmissionError(f"non-JSON numeric constant rejected: {value}")


def check_payload(raw: bytes) -> list[str]:
    if len(raw) > MAX_BYTES:
        return ["input exceeds bounded research profile (256 KiB)"]
    try:
        payload = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (ValueError, UnicodeError) as exc:
        return [f"INPUT_INVALID: {exc}"]
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: (tuple(map(str, error.absolute_path)), error.message),
    )
    return [
        f"{'/'.join(str(v) for v in e.absolute_path) or '$'}: {e.message}"
        for e in errors
    ]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--cli", type=Path, help="Optional canonical PayGod CLI; do not use any alternate policy executor")
    p.add_argument("--out", type=Path, help="Required with --cli; fresh output location")
    args = p.parse_args()
    if bool(args.cli) != bool(args.out):
        p.error("--cli and --out must be used together")
    try:
        raw = args.input.read_bytes()
    except OSError as exc:
        print(json.dumps({"admission": "NOT_RUN", "reason": str(exc)}, ensure_ascii=False))
        return 2

    errors = check_payload(raw)
    digest = hashlib.sha256(raw).hexdigest()
    if errors:
        print(json.dumps({
            "admission": "WITHHELD",
            "kernel": "NOT_RUN",
            "source_bytes_sha256": digest,
            "errors": errors,
            "scope": "shape_only_research_v0",
        }, ensure_ascii=False, sort_keys=True))
        return 2

    # The digest identifies supplied bytes only. It does not authenticate the meter,
    # actor, institution, reporting methodology, emissions factor, or historical time.
    if not args.cli:
        print(json.dumps({
            "admission": "SHAPE_PASSED_ONLY",
            "kernel": "NOT_RUN",
            "source_bytes_sha256": digest,
            "scope": "shape_only_research_v0",
        }, sort_keys=True))
        return 0

    if args.out.exists() and any(args.out.iterdir()):
        print(json.dumps({"admission": "WITHHELD", "kernel": "NOT_RUN",
                          "errors": ["output directory is not empty"]}))
        return 2
    if not PACK.is_dir():
        print(json.dumps({"admission": "WITHHELD", "kernel": "NOT_RUN",
                          "errors": ["canonical GHG Pack not present"]}))
        return 2

    command = [
        str(args.cli), "run", "--pack", str(PACK),
        "--input", str(args.input.resolve()), "--out", str(args.out.resolve()),
    ]
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except OSError as exc:
        print(json.dumps({"admission": "SHAPE_PASSED_ONLY", "kernel": "FAILED",
                          "errors": [str(exc)]}))
        return 2
    print(json.dumps({
        "admission": "SHAPE_PASSED_ONLY",
        "kernel": "EXECUTED_CANONICAL_CLI" if result.returncode == 0 else "FAILED",
        "source_bytes_sha256": digest,
        "scope": "shape_only_research_v0",
        "exit_code": result.returncode,
        "stderr": result.stderr[-3000:],
    }, sort_keys=True))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
