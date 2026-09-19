#!/usr/bin/env python3
"""Repository Boundary Closure v0.1 enforcement.

The gate inventories real repository-hosted adapters and verifies their
authority boundary. Fixtures prove the role/capability policy. Mutation
witnesses then inject forbidden authority into copies of actual adapters and
require the same inspector to reject them.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER_ALLOWED = {"submit", "invoke", "transport", "store", "expose"}
VERIFIER_ALLOWED = {"verify"}

ADAPTERS = {
    "api/server.js": {
        "mode": "fail_closed",
        "required": [r"canonical-kernel-required"],
        "forbidden": [
            r"bundle_digest\s*[:=]",
            r"\b(?:verdict|decision)\s*[:=]\s*['\"](?:PASS|FAIL|HOLD|RELEASE|REDUCE|ALLOW|DENY)['\"]",
            r"\breceipt\s*[:=]",
            r"createHash\s*\(",
            r"pseudo[-_ ]?zip",
        ],
    },
    "deploy/docker/api/app/Program.cs": {
        "mode": "delegate",
        "required": [
            r"/runner/PayGod\.Cli\.dll",
            r'["\x27]run["\x27]',
            r"Process\.Start\s*\(",
        ],
        "forbidden": [
            r"bundle_digest\s*[:=]",
            r"\b(?:verdict|decision)\s*=\s*['\"](?:PASS|FAIL|HOLD|RELEASE|REDUCE|ALLOW|DENY)['\"]",
            r"\breceipt\s*=",
            r"SHA(?:1|256|384|512)",
            r"HashData\s*\(",
            r"pseudo[-_ ]?zip",
        ],
    },
}

MUTATIONS = {
    "verdict": {
        "api/server.js": "\nconst verdict = 'PASS';\n",
        "deploy/docker/api/app/Program.cs": '\nvar verdict = "PASS";\n',
    },
    "receipt": {
        "api/server.js": "\nconst receipt = { issuer: 'adapter' };\n",
        "deploy/docker/api/app/Program.cs": '\nvar receipt = new { issuer = "adapter" };\n',
    },
    "bundle": {
        "api/server.js": "\nconst bundle_digest = 'adapter-owned';\n",
        "deploy/docker/api/app/Program.cs": '\nvar bundle_digest = "adapter-owned";\n',
    },
}

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

def inspect_text(rel: str, text: str) -> list[str]:
    rules = ADAPTERS[rel]
    failures: list[str] = []
    for pattern in rules["required"]:
        if not re.search(pattern, text, re.I | re.S):
            failures.append(f"{rel}: missing required {rules['mode']} boundary marker: {pattern}")
    for pattern in rules["forbidden"]:
        if re.search(pattern, text, re.I | re.S):
            failures.append(f"{rel}: forbidden alternate-authority construction: {pattern}")
    return failures

def inspect_actual_adapters() -> list[str]:
    failures: list[str] = []
    for rel in ADAPTERS:
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"{rel}: registered adapter missing")
            continue
        failures.extend(inspect_text(rel, path.read_text(encoding="utf-8-sig")))
    return failures

def mutation_witness() -> list[str]:
    failures: list[str] = []
    for mutation_name, by_adapter in MUTATIONS.items():
        for rel, injection in by_adapter.items():
            path = ROOT / rel
            if not path.is_file():
                failures.append(f"{rel}: cannot mutate missing adapter")
                continue
            original = path.read_text(encoding="utf-8-sig")
            mutated = original + injection
            detected = inspect_text(rel, mutated)
            if not detected:
                failures.append(f"{rel}: {mutation_name} alternate-authority mutation was NOT rejected")
            else:
                print(f"REJECTED: {rel} mutation={mutation_name}")
    return failures

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", type=pathlib.Path)
    ap.add_argument("--expect", choices=["pass", "reject"])
    ap.add_argument("--scan-current", action="store_true")
    ap.add_argument("--mutation-witness", action="store_true")
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
        failures = inspect_actual_adapters()
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print("PASS: all registered repository-hosted adapters preserve the canonical authority boundary")
        return 0

    if args.mutation_witness:
        failures = mutation_witness()
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print("PASS: verdict, receipt, and bundle-identity mutations of actual adapters were rejected")
        return 0

    ap.error("choose --contract, --scan-current, or --mutation-witness")

if __name__ == "__main__":
    raise SystemExit(main())
