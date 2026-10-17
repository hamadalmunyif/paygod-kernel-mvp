#!/usr/bin/env python3
"""Research-only composition witness: typed-v1 plus non-permitting Trivy policy.

No scanner invocation, signed report admission, independent issuer or release
authorization is provided. Historical v1 packs are never touched.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "examples" / "eik-trivy-severity-typed-research"

def check(cli, source_text, expected_exit, verdict, name, root):
    source = root / (name + ".json")
    target = root / ("out-" + name)
    source.write_text(source_text, encoding="utf-8")
    p = subprocess.run([cli, "run", "--pack", str(PACK),
                        "--input", str(source), "--out", str(target)],
                       capture_output=True, text=True)
    assert p.returncode == expected_exit, (name, p.returncode, p.stdout, p.stderr)
    receipt = target / "receipt.json"
    if verdict is None:
        assert not target.exists(), (name, "malformed typed source minted artifacts")
    else:
        assert receipt.exists(), (name, "expected canonical receipt missing")
        observed = json.loads(receipt.read_text(encoding="utf-8"))["verdict"]["value"]
        assert observed == verdict, (name, observed, verdict)
        assert observed != "allow", (name, "non-permitting prototype allowed")
    print(f"PASS {name}: exit {expected_exit}, expected verdict {verdict}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cli", required=True)
    args = ap.parse_args()
    cli = str(Path(args.cli).resolve())
    pack = yaml.safe_load((PACK / "pack.yaml").read_text(encoding="utf-8"))
    assert pack["spec"]["policy"]["evaluation_profile"] == "typed-v1"
    assert pack["metadata"]["version"] == "2.1.0"
    assert all(rule["decision"] != "allow" for rule in pack["spec"]["policy"]["rules"])
    digest = "registry.example/test@sha256:" + "a" * 64
    def observation(severity):
        return {"scan_report": {"artifact_name": digest, "vulnerabilities": [
            {"cve_id": "CVE-2099-0001", "severity": severity,
             "installed_version": "3.3.7-r1", "trivy_status": "fixed"}
        ]}}
    with tempfile.TemporaryDirectory(prefix="paygod-trivy-typed-research-") as td:
        temp = Path(td)
        for name, severity, expected in [
            ("high-fixed-available", "HIGH", "deny"),
            ("critical-fixed-available", "CRITICAL", "deny"),
            ("medium-fixed-available", "MEDIUM", "flag"),
            ("low-only", "LOW", "error"),
        ]:
            check(cli, json.dumps(observation(severity), separators=(",", ":")),
                  0, expected, name, temp)
        for name, raw in [
            ("missing-array", json.dumps({"scan_report": {"artifact_name": digest}})),
            ("wrong-severity-type", json.dumps(observation(True))),
            ("duplicate-severity", '{"scan_report":{"artifact_name":"' + digest +
             '","vulnerabilities":[{"cve_id":"CVE-2099-0001","severity":"HIGH",'
             '"severity":"LOW","installed_version":"3.3.7-r1","trivy_status":"fixed"}]}}'),
        ]:
            check(cli, raw, 2, None, name, temp)
    print("PASS: typed-v1 research Trivy policy is non-permitting; missing/ambiguous inputs cannot mint artifacts")

if __name__ == "__main__":
    main()
