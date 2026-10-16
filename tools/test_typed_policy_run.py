#!/usr/bin/env python3
"""CLI witness for explicit typed-v1 Pack, no receipt on wrong/missing type.

This tests *evaluation-time* rejection, not mandatory external source
pre-admission or scanner truth. Uses an isolated synthetic Pack only.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "examples" / "policy-typed-comparisons"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", required=True)
    args = parser.parse_args()
    cli = str(Path(args.cli).resolve())
    with tempfile.TemporaryDirectory(prefix="paygod-typed-profile-") as tmp:
        tmp = Path(tmp)
        cases = [
            ("known-false", {"input": {"block": False}}, 0, "allow"),
            ("known-true", {"input": {"block": True}}, 0, "deny"),
            ("string-false", {"input": {"block": "false"}}, 2, None),
            ("zero", {"input": {"block": 0}}, 2, None),
            ("null", {"input": {"block": None}}, 2, None),
            ("missing", {"input": {}}, 2, None),
        ]
        for name, obj, expected_exit, decision in cases:
            source = tmp / f"{name}.json"
            output = tmp / f"out-{name}"
            source.write_text(json.dumps(obj, separators=(",", ":")), encoding="utf-8")
            p = subprocess.run([cli, "run", "--pack", str(PACK),
                                "--input", str(source), "--out", str(output)],
                               capture_output=True, text=True)
            assert p.returncode == expected_exit, (
                name, p.returncode, p.stdout, p.stderr)
            receipt = output / "receipt.json"
            manifest = output / "manifest.json"
            ledger = output / "ledger.jsonl"
            if decision is None:
                assert not any(x.exists() for x in (receipt, manifest, ledger)), (
                    name, "malformed typed input must not mint canonical evidence")
            else:
                assert all(x.exists() for x in (receipt, manifest, ledger)), name
                recorded = json.loads(receipt.read_text(encoding="utf-8"))
                assert recorded["verdict"]["value"] == decision, (name, recorded["verdict"])
            print(f"PASS: typed-v1 {name}, exit={p.returncode}, receipt={'yes' if decision else 'no'}")
    print("PASS: typed-v1 CLI no-artifact regression; legacy fixtures are verified separately")

if __name__ == "__main__":
    main()
