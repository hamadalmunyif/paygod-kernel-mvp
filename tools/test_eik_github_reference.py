#!/usr/bin/env python3
"""Hermetic synthetic GitHub Actions EIK reference tests; no external network/rails."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "examples" / "eik-github-actions"
PRODUCER = REFERENCE / "eik_reference.py"
VERIFIER = ROOT / "tools" / "verify_portable_evidence.py"


def call(command: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False, env=env, timeout=90)


def require(condition: bool, message: str, result: subprocess.CompletedProcess[str] | None = None) -> None:
    if not condition:
        trace = "" if result is None else f"\nstdout={result.stdout}\nstderr={result.stderr}"
        raise AssertionError(message + trace)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", type=Path, required=True)
    cli = str(parser.parse_args().cli.resolve())
    env = dict(os.environ, PAYGOD_CLOCK="2026-10-14T00:00:00Z", PAYGOD_STRICT="1")

    with tempfile.TemporaryDirectory(prefix="eik-github-reference-") as temp:
        root = Path(temp)
        for name, expected_verdict in [("clean", "allow"), ("findings", "deny")]:
            output = root / name
            result = call([sys.executable, str(PRODUCER), "--source",
                           str(REFERENCE / "fixtures" / f"{name}.json"),
                           "--cli", cli, "--out", str(output)], env=env)
            require(result.returncode == 0, f"{name} producer failed", result)
            statement = json.loads(result.stdout)
            require(statement["status"] == "KERNEL_EXECUTED", "producer did not use canonical CLI")
            evidence = output / "evidence"
            receipt = json.loads((evidence / "receipt.json").read_text(encoding="utf-8"))
            require(receipt["verdict"]["value"] == expected_verdict, f"unexpected {name} Pack policy verdict")

            producer_hash = hashlib.sha256((evidence / "receipt.json").read_bytes()).hexdigest()
            require(statement["receipt_sha256"] == producer_hash, "reported producer receipt digest differs")
            require(len(list(evidence.iterdir())) == 5, "non-Kernel payload inside canonical evidence directory")

            result_path = root / f"{name}-verified.json"
            verified = call([sys.executable, str(VERIFIER), str(evidence),
                             "--expect-receipt-sha256", producer_hash,
                             "--result", str(result_path)])
            require(verified.returncode == 0, f"{name} independent integrity failure", verified)
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            require(payload["status"] == "valid" and
                    payload["verification"]["integrity"] == "verified",
                    "independent verifier did not report scoped integrity")
            require(payload["verification"]["replay"] == "not_performed",
                    "unexpected replay assertion")

        for name in ["failed-zero", "missing"]:
            output = root / f"{name}-withheld"
            rejected = call([sys.executable, str(PRODUCER), "--source",
                             str(REFERENCE / "fixtures" / f"{name}.json"),
                             "--cli", cli, "--out", str(output)], env=env)
            require(rejected.returncode == 2, f"{name} not withheld", rejected)
            payload = json.loads(rejected.stdout)
            require(payload["status"] == "WITHHELD_NOT_RUN" and
                    payload["kernel_invoked"] is False, f"{name} invoked Kernel")
            require(not output.exists(), f"{name} created an output path")

        # No source file must not create an allow receipt.
        absent = root / "no-report"
        rejected = call([sys.executable, str(PRODUCER), "--source",
                         str(root / "absent.json"), "--cli", cli, "--out", str(absent)], env=env)
        require(rejected.returncode == 2 and not absent.exists(), "absent source admitted")

        clean = root / "clean" / "evidence"
        # An external pin must reject a different otherwise valid receipt.
        wrong = call([sys.executable, str(VERIFIER), str(clean),
                      "--expect-receipt-sha256", "0" * 64])
        require(wrong.returncode != 0, "incorrect independent receipt pin was accepted", wrong)

        # Artifact modification invalidates the existing manifest/receipt.
        altered = root / "altered"
        shutil.copytree(clean, altered)
        target = altered / "findings.json"
        target.write_bytes(target.read_bytes() + b" ")
        mutated = call([sys.executable, str(VERIFIER), str(altered)])
        require(mutated.returncode != 0, "one-byte change was accepted", mutated)

    print("PASS: synthetic source -> explicit admission -> canonical CLI -> scoped receiver verification; failed/absent and mutation negatives")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
