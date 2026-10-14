#!/usr/bin/env python3
"""Local EIK authoring and structural input regression, using temp fixtures only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def call(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=40, check=False)


def check(result: subprocess.CompletedProcess[str], code: int, label: str) -> None:
    if result.returncode != code:
        raise AssertionError(f"{label}: expected exit {code}, got {result.returncode}: {result.stdout} {result.stderr}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", type=Path, required=True)
    args = parser.parse_args()
    cli = str(args.cli.resolve())
    admission = str(Path(__file__).resolve().with_name("eik_admit.py"))
    with tempfile.TemporaryDirectory(prefix="paygod-eik-") as directory:
        root = Path(directory)
        pack = root / "packs" / "core" / "example-safe-pack"

        for invalid in ("Bad Name", "bad/name", ".."):
            r = call([cli, "pack", "init", "--name", invalid], root)
            if r.returncode == 0:
                raise AssertionError(f"Invalid name accepted: {invalid}")

        check(call([cli, "pack", "init", "--name", "example-safe-pack"], root), 0, "pack init")
        if not (pack / "pack.yaml").is_file():
            raise AssertionError("Generated pack.yaml missing")
        check(call([cli, "test", "--pack", str(pack), "--json"], root), 0, "Pack fixture tests")

        cases = [
            ({"input": {"block": True}}, 0, "STRUCTURAL_ONLY_PASS"),
            ({"input": {"block": False}}, 0, "STRUCTURAL_ONLY_PASS"),
            ({}, 2, "WITHHELD_NOT_RUN"),
            ({"input": {}}, 2, "WITHHELD_NOT_RUN"),
            ({"input": {"block": None}}, 2, "WITHHELD_NOT_RUN"),
            ({"input": {"block": "false"}}, 2, "WITHHELD_NOT_RUN"),
        ]
        for index, (value, code, status) in enumerate(cases):
            fixture = root / f"fixture-{index}.json"
            fixture.write_text(json.dumps(value), encoding="utf-8")
            result = call([sys.executable, admission, "--pack", str(pack), "--input", str(fixture)], root)
            check(result, code, f"structural input {index}")
            report = json.loads(result.stdout)
            if report["status"] != status or report["kernel_invoked"] is not False:
                raise AssertionError(f"Incorrect structural status for case {index}: {report}")

    print("PASS: Pack creation, positive fixtures, missing/wrong-type structural rejection")
    return 0


if __name__ == "__main__":
    sys.exit(main())
