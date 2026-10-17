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
                assert not output.exists(), (
                    name, "failed typed evaluation must not create output directory")
                assert not any(x.exists() for x in (receipt, manifest, ledger)), (
                    name, "malformed typed input must not mint canonical evidence")
            else:
                assert all(x.exists() for x in (receipt, manifest, ledger)), name
                recorded = json.loads(receipt.read_text(encoding="utf-8"))
                assert recorded["verdict"]["value"] == decision, (name, recorded["verdict"])
            print(f"PASS: typed-v1 {name}, exit={p.returncode}, receipt={'yes' if decision else 'no'}")
        # Duplicate source keys can be consumed differently by different
        # runtimes; typed-v1 rejects raw object keys before materialization.
        # This includes hidden nested objects that a rule did not reference.
        duplicates = [
            ("duplicate-block", '{"input":{"block":false,"block":true}}'),
            ("duplicate-nested", '{"input":{"block":false,"nested":{"x":1,"x":2}}}'),
            ("duplicate-in-array", '{"input":{"block":false,"items":[{"x":1,"x":2}]}}'),
        ]
        for name, raw in duplicates:
            source = tmp / f"{name}.json"
            output = tmp / f"out-{name}"
            source.write_text(raw, encoding="utf-8")
            p = subprocess.run([cli, "run", "--pack", str(PACK),
                                "--input", str(source), "--out", str(output)],
                               capture_output=True, text=True)
            assert p.returncode == 2, (name, p.returncode, p.stdout, p.stderr)
            assert "INPUT_JSON_DUPLICATE_KEY" in p.stderr, (name, p.stderr)
            assert not output.exists(), (name, "duplicate input minted output")
            print(f"PASS: typed-v1 {name} duplicate rejected with no artifacts")
        # Attacker-controlled or malformed policy syntax must not be silently
        # truncated into a permissive expression by the typed-v1 lexer.
        # This exercises the real CLI before any canonical output is written.
        base_pack = (PACK / "pack.yaml").read_text(encoding="utf-8")
        original_rule = 'condition: "input.input.block == false"'
        assert base_pack.count(original_rule) == 1
        lexer_cases = [
            ("unknown-ampersand", "input.input.block == false && input.input.required"),
            ("unknown-pipe", "input.input.block == false || true"),
            ("unknown-comment", "input.input.block == false # ignored"),
            ("invalid-number", "input.input.count == 1e999"),
            ("malformed-number", "input.input.count == 1-1"),
            ("unterminated-string", "input.input.word == 'open"),
        ]
        for name, expression in lexer_cases:
            pack_dir = tmp / f"pack-{name}"
            pack_dir.mkdir()
            (pack_dir / "pack.yaml").write_text(
                base_pack.replace(original_rule, f'condition: "{expression}"'),
                encoding="utf-8")
            source = tmp / f"source-{name}.json"
            source.write_text('{"input":{"block":false,"count":0,"required":false,"word":"open"}}',
                              encoding="utf-8")
            output = tmp / f"out-lexer-{name}"
            p = subprocess.run([cli, "run", "--pack", str(pack_dir),
                                "--input", str(source), "--out", str(output)],
                               capture_output=True, text=True)
            assert p.returncode == 2, (name, p.returncode, p.stdout, p.stderr)
            assert "POLICY_INPUT_REJECTED" in p.stderr, (name, p.stderr)
            assert not output.exists(), (name, "malformed policy minted output")
            print(f"PASS: typed-v1 {name} policy rejected; no artifacts")
        # Refuse reuse of a directory holding an old canonical receipt.
        # An error must never silently overwrite or pretend to replace it.
        prior = tmp / "preexisting-output"
        prior.mkdir()
        old_receipt = prior / "receipt.json"
        old_receipt.write_text('{"historic":"do-not-modify"}', encoding="utf-8")
        source = tmp / "reused-source.json"
        source.write_text('{"input":{"block":false}}', encoding="utf-8")
        reused = subprocess.run(
            [cli, "run", "--pack", str(PACK), "--input", str(source),
             "--out", str(prior)], capture_output=True, text=True)
        assert reused.returncode == 2, (reused.stdout, reused.stderr)
        assert "OUTPUT_DIRECTORY_NOT_FRESH" in reused.stderr, reused.stderr
        assert old_receipt.read_text(encoding="utf-8") == '{"historic":"do-not-modify"}'
        assert not (prior / "manifest.json").exists()
        assert not (prior / "ledger.jsonl").exists()
        print("PASS: typed-v1 refuses stale output directory; historic receipt untouched")
    print("PASS: typed-v1 CLI no-artifact regression; legacy fixtures are verified separately")

if __name__ == "__main__":
    main()
