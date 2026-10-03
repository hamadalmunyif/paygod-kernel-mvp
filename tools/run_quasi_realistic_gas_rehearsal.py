#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path

from run_gas_site_readiness_rehearsal import _produce

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", type=Path, required=True)
    parser.add_argument("--pack", default="rehearsals/gas-site-readiness")
    parser.add_argument("--cases", type=Path, default=Path("rehearsals/gas-site-readiness/quasi-realistic-cases.json"))
    parser.add_argument("--result", type=Path, default=Path("quasi-realistic-gas-rehearsal-result.json"))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    payload = json.loads((repo_root / args.cases).read_text(encoding="utf-8"))
    results = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for index, case in enumerate(payload["cases"], start=1):
            started = time.perf_counter()
            produced = _produce(args.cli.resolve(), args.pack, repo_root, case["site"], root / case["case_id"])
            elapsed_ms = int(round((time.perf_counter() - started) * 1000))
            if produced["returncode"] != 0:
                results.append({
                    "case_id": case["case_id"],
                    "scenario": case["scenario"],
                    "passed": False,
                    "error": "producer_failed",
                    "producer_returncode": produced["returncode"],
                    "stderr_tail": produced["stderr"],
                })
                continue

            actual = produced["outcome"]
            verification = produced["verification"]
            integrity_verified = (
                verification["status"] == "valid"
                and verification["verification"]["integrity"] == "verified"
            )
            relationship = "AGREE" if actual == case["simulated_operator_decision"] else "DISAGREE"
            expected_gap = case.get("expected_gap_class", "")
            gap_ok = (
                relationship == "AGREE" and expected_gap == ""
            ) or (
                relationship == "DISAGREE"
                and expected_gap in {"contract_gap", "provenance_gap", "policy_ambiguity", "missing_evidence", "human_error", "kernel_defect"}
            )

            passed = (
                actual == case["expected_paygod_decision"]
                and relationship == case["expected_relationship"]
                and integrity_verified
                and gap_ok
            )
            results.append({
                "case_id": case["case_id"],
                "scenario": case["scenario"],
                "simulated_operator_decision": case["simulated_operator_decision"],
                "actual_paygod_decision": actual,
                "relationship": relationship,
                "gap_class": expected_gap if relationship == "DISAGREE" else "",
                "integrity_verified": integrity_verified,
                "technical_produce_verify_ms": elapsed_ms,
                "receipt_sha256": produced["receipt_sha256"],
                "ledger_head": verification["ledger_head"],
                "passed": passed,
            })

    agreement = sum(1 for x in results if x.get("relationship") == "AGREE")
    disagreement = sum(1 for x in results if x.get("relationship") == "DISAGREE")
    integrity = sum(1 for x in results if x.get("integrity_verified") is True)
    passed_count = sum(1 for x in results if x.get("passed") is True)

    report = {
        "artifact_type": "paygod/gas-site-readiness-quasi-realistic-rehearsal/v0.1",
        "phase": "internal_quasi_realistic_simulation",
        "external_pilot": False,
        "counts_as_real_b2_cases": False,
        "case_count": len(results),
        "agreement_count": agreement,
        "disagreement_count": disagreement,
        "integrity_verified_count": integrity,
        "passed_count": passed_count,
        "expected_deliberate_gaps": {
            "contract_gap": sum(1 for x in results if x.get("gap_class") == "contract_gap"),
            "provenance_gap": sum(1 for x in results if x.get("gap_class") == "provenance_gap"),
        },
        "passed": (
            len(results) == 10
            and passed_count == 10
            and agreement == 8
            and disagreement == 2
            and integrity == 10
        ),
        "results": results,
        "non_claims": [
            "real historical case coverage",
            "independent human judgment",
            "market demand",
            "regulator approval",
            "external evidence truth",
            "production operational readiness"
        ]
    }

    args.result.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
