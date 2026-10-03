#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def run_case(cli: Path, repo_root: Path, name: str, raw_json: str, expected_codes: set[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        input_path = root / "input.json"
        out_dir = root / "out"
        input_path.write_text(raw_json, encoding="utf-8")

        proc = subprocess.run(
            [
                str(cli),
                "run",
                "--pack",
                "packs/core/secrets-in-repo-guard",
                "--input",
                str(input_path),
                "--out",
                str(out_dir),
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )

        combined = proc.stdout + "\n" + proc.stderr
        if proc.returncode != 2:
            raise AssertionError(f"{name}: expected exit 2, got {proc.returncode}\n{combined}")

        matched = [code for code in expected_codes if f"ERR[{code}]:" in combined]
        if not matched:
            raise AssertionError(
                f"{name}: expected one of {sorted(expected_codes)}, got:\n{combined}"
            )

        forbidden = ("System.CommandLine", " at System.", "Unhandled exception", "--- End of stack trace")
        for marker in forbidden:
            if marker in combined:
                raise AssertionError(f"{name}: leaked framework stack trace marker {marker!r}\n{combined}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", type=Path, required=True)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    cli = args.cli.resolve()

    cases = [
        (
            "float",
            json.dumps({"scan_report": {"secrets_found": 0}, "probe": 0.1}),
            {"CANONICAL_INPUT_REJECTED"},
        ),
        (
            "unsafe-integer",
            json.dumps({"scan_report": {"secrets_found": 0}, "probe": 9007199254740992}),
            {"CANONICAL_INPUT_REJECTED"},
        ),
        (
            "non-nfc-key",
            json.dumps(
                {"scan_report": {"secrets_found": 0}, "e\u0301": "value"},
                ensure_ascii=False,
            ),
            {"CANONICAL_INPUT_REJECTED"},
        ),
        (
            "unpaired-surrogate",
            '{"scan_report":{"secrets_found":0},"probe":"\\ud800"}',
            {"CANONICAL_INPUT_REJECTED", "INPUT_JSON_INVALID"},
        ),
        (
            "malformed-json",
            '{"scan_report":',
            {"INPUT_JSON_INVALID"},
        ),
    ]

    for name, raw_json, expected_codes in cases:
        run_case(cli, repo_root, name, raw_json, expected_codes)
        print(f"PASS: {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
