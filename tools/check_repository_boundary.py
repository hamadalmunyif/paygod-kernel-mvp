#!/usr/bin/env python3
"""Repository Boundary Closure v0.1 enforcement.

This is intentionally a capability/ownership gate first, with source-pattern
checks only as defense in depth. It does not define kernel semantics.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
KERNEL_ONLY = {
    "originate_decision",
    "originate_verdict",
    "originate_artifacts",
    "originate_manifest",
    "originate_receipt",
    "originate_bundle_identity",
    "evaluate_policy",
}
ADAPTER_ALLOWED = {"submit", "invoke", "transport", "store", "expose"}
VERIFIER_ALLOWED = {"verify"}

def validate_contract(path: pathlib.Path) -> tuple[bool, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    role = data.get("role")
    caps = set(data.get("capabilities", []))
    if role == "kernel":
        return True, "kernel authority contract"
    if role == "adapter":
        bad = caps - ADAPTER_ALLOWED
        return (not bad, "adapter delegates only" if not bad else f"adapter claims forbidden capabilities: {sorted(bad)}")
    if role == "verifier":
        bad = caps - VERIFIER_ALLOWED
        return (not bad, "verifier verifies only" if not bad else f"verifier claims forbidden capabilities: {sorted(bad)}")
    return False, f"unknown role: {role!r}"

# Defense in depth for repository-hosted adapters. These are indicators, not
# the authority proof; the capability contract above is the primary rule.
FORBIDDEN_SOURCE = [
    (re.compile(r"bundle_digest\s*[:=]\s*['\"]demo-bundle"), "fabricated demo bundle identity"),
    (re.compile(r"createHash\s*\([^)]*\).*bundle", re.S), "adapter-created bundle hash"),
    (re.compile(r"pseudo[-_ ]?zip", re.I), "pseudo evidence archive"),
]

def scan_adapter_source(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [reason for pattern, reason in FORBIDDEN_SOURCE if pattern.search(text)]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", type=pathlib.Path)
    ap.add_argument("--expect", choices=["pass", "reject"])
    ap.add_argument("--scan-current", action="store_true")
    args = ap.parse_args()

    if args.contract:
        ok, reason = validate_contract(args.contract)
        print(json.dumps({"contract": str(args.contract), "valid": ok, "reason": reason}, sort_keys=True))
        if args.expect == "pass":
            return 0 if ok else 1
        if args.expect == "reject":
            return 0 if not ok else 1
        return 0 if ok else 1

    if args.scan_current:
        failures = []
        for rel in ("api/server.js",):
            path = ROOT / rel
            if path.exists():
                for reason in scan_adapter_source(path):
                    failures.append(f"{rel}: {reason}")
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print("PASS: repository-hosted adapter surfaces do not originate known alternate authority")
        return 0

    ap.error("choose --contract or --scan-current")

if __name__ == "__main__":
    raise SystemExit(main())
