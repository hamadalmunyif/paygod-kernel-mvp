#!/usr/bin/env python3
"""Synthetic Gas Site Readiness Internal Rehearsal v0.1.

Engineering readiness only. This does not establish regulatory compliance,
market demand, willingness to pay, or independent human-decision agreement.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import tempfile

from verify_portable_evidence import SAFE_INTEGER_MAX, canonical_json, sha256_bytes, verify


RUN_TS = "2026-10-03T00:00:00+00:00"
OUTCOME_BY_VERDICT = {
    "allow": "READY",
    "flag": "HOLD",
    "deny": "REJECT",
    "error": "ERROR",
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _site(case_id: str, **overrides) -> dict:
    base = {
        "site_id": case_id,
        "evidence_site_id": case_id,
        "site_name": f"موقع تجريبي {case_id}",
        "pressure_test_passed": True,
        "isolation_valves_ready": True,
        "fire_protection_ready": True,
        "leak_detection_required": True,
        "leak_detection_auto_shutoff_ready": True,
        "preoperation_notification_evidence": True,
        "warning_signs_installed": True,
    }
    base.update(overrides)
    return base


def checklist_outcome(site: dict) -> str:
    """Independent mechanical baseline; it does not parse the Paygod pack."""
    if site.get("site_id") != site.get("evidence_site_id"):
        return "REJECT"
    if not bool(site.get("pressure_test_passed")):
        return "REJECT"
    if not bool(site.get("isolation_valves_ready")):
        return "REJECT"
    if not bool(site.get("fire_protection_ready")):
        return "REJECT"
    if bool(site.get("leak_detection_required")) and not bool(
        site.get("leak_detection_auto_shutoff_ready")
    ):
        return "REJECT"
    if not bool(site.get("preoperation_notification_evidence")):
        return "HOLD"
    if not bool(site.get("warning_signs_installed")):
        return "HOLD"
    return "READY"


def curated_cases() -> list[dict]:
    return [
        _site("CUR-01"),
        _site("CUR-02", pressure_test_passed=False),
        _site("CUR-03", isolation_valves_ready=False),
        _site("CUR-04", fire_protection_ready=False),
        _site("CUR-05", leak_detection_required=True, leak_detection_auto_shutoff_ready=False),
        _site("CUR-06", preoperation_notification_evidence=False),
        _site("CUR-07", warning_signs_installed=False),
        _site("CUR-08", leak_detection_required=False, leak_detection_auto_shutoff_ready=False),
        _site("CUR-09", preoperation_notification_evidence=False, warning_signs_installed=False),
        _site("CUR-10", evidence_site_id="OTHER-SITE"),
    ]


def generated_cases() -> list[dict]:
    """Deterministic blind-style combinations with outcome quotas.

    Naive independent booleans heavily bias this policy toward REJECT because
    several safety gates are conjunctive. Rejection sampling preserves a fixed
    seed while ensuring the generated set exercises READY, HOLD, and REJECT.
    """
    rng = random.Random(20261003)
    targets = {"READY": 3, "HOLD": 3, "REJECT": 4}
    counts = {key: 0 for key in targets}
    result: list[dict] = []
    attempts = 0

    while len(result) < 10:
        attempts += 1
        if attempts > 10000:
            raise RuntimeError("unable to satisfy generated outcome quotas")

        candidate = _site(
            "PENDING",
            pressure_test_passed=bool(rng.getrandbits(1)),
            isolation_valves_ready=bool(rng.getrandbits(1)),
            fire_protection_ready=bool(rng.getrandbits(1)),
            leak_detection_required=bool(rng.getrandbits(1)),
            leak_detection_auto_shutoff_ready=bool(rng.getrandbits(1)),
            preoperation_notification_evidence=bool(rng.getrandbits(1)),
            warning_signs_installed=bool(rng.getrandbits(1)),
        )
        outcome = checklist_outcome(candidate)
        if counts[outcome] >= targets[outcome]:
            continue

        index = len(result) + 1
        candidate["site_id"] = f"GEN-{index:02d}"
        candidate["evidence_site_id"] = candidate["site_id"]
        candidate["site_name"] = f"موقع تجريبي {candidate['site_id']}"
        counts[outcome] += 1
        result.append(candidate)

    if counts != targets:
        raise RuntimeError(f"generated outcome quota mismatch: {counts}")
    return result


def _write_input(path: Path, site: dict) -> None:
    path.write_text(
        json.dumps({"site": site}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _produce(cli: Path, pack: str, repo_root: Path, site: dict, root: Path) -> dict:
    input_path = root / "input.json"
    out_dir = root / "evidence"
    root.mkdir(parents=True, exist_ok=True)
    _write_input(input_path, site)

    env = os.environ.copy()
    env["PAYGOD_CLOCK"] = RUN_TS
    env["PAYGOD_STRICT"] = "1"

    proc = subprocess.run(
        [
            str(cli),
            "run",
            "--pack",
            pack,
            "--input",
            str(input_path),
            "--out",
            str(out_dir),
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    result = {
        "returncode": proc.returncode,
        "stdout": proc.stdout[-1000:],
        "stderr": proc.stderr[-1000:],
        "input_path": str(input_path),
        "evidence_dir": str(out_dir),
    }
    if proc.returncode != 0:
        return result

    receipt_path = out_dir / "receipt.json"
    receipt_sha = _sha(receipt_path)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    verification = verify(out_dir, expected_receipt_sha256=receipt_sha)

    result.update(
        {
            "receipt_sha256": receipt_sha,
            "verdict": receipt["verdict"]["value"],
            "outcome": OUTCOME_BY_VERDICT.get(receipt["verdict"]["value"], "UNKNOWN"),
            "verification": verification,
        }
    )
    return result


def _recompute_coherent_rewrite(root: Path, new_verdict: str) -> str:
    ledger_path = root / "ledger.jsonl"
    manifest_path = root / "manifest.json"
    receipt_path = root / "receipt.json"

    lines = [line for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError("rehearsal expects a single-entry ledger")

    ledger = json.loads(lines[0])
    ledger["data"]["verdict"] = new_verdict
    ledger["data"]["reason"] = "coordinated rehearsal rewrite"
    payload = {
        "previous_hash": ledger["previous_hash"],
        "timestamp": ledger["timestamp"],
        "data": ledger["data"],
    }
    ledger["record_hash"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    ledger_path.write_text(json.dumps(ledger, separators=(",", ":")) + "\n", encoding="utf-8")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        artifact = root / entry["name"]
        entry["sha256"] = _sha(artifact)
        entry["bytes"] = artifact.stat().st_size
    digest_lines = [
        f"{entry['name']}={entry['sha256']}\n"
        for entry in sorted(manifest["files"], key=lambda item: item["name"])
    ]
    manifest["bundle"]["bundle_digest"] = hashlib.sha256(
        "".join(digest_lines).encode("utf-8")
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["bundle"]["files"] = manifest["files"]
    receipt["bundle"]["bundle_digest"] = manifest["bundle"]["bundle_digest"]
    receipt["bundle"]["manifest_sha256"] = _sha(manifest_path)
    receipt["verdict"]["value"] = new_verdict
    receipt["verdict"]["reason"] = "coordinated rehearsal rewrite"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return _sha(receipt_path)


def _decision_case(cli: Path, pack: str, repo_root: Path, root: Path, site: dict, index: int) -> dict:
    expected = checklist_outcome(site)
    produced = _produce(cli, pack, repo_root, site, root / f"decision-{index:02d}")
    if produced["returncode"] != 0:
        return {
            "id": site["site_id"],
            "expected": expected,
            "actual": "PRODUCER_REJECTED",
            "agreement": False,
            "integrity_verified": False,
            "producer_returncode": produced["returncode"],
            "producer_stderr": produced["stderr"],
        }

    verification = produced["verification"]
    actual = produced["outcome"]
    return {
        "id": site["site_id"],
        "expected": expected,
        "actual": actual,
        "agreement": actual == expected,
        "integrity_verified": (
            verification["status"] == "valid"
            and verification["verification"]["integrity"] == "verified"
        ),
        "verdict": produced["verdict"],
        "receipt_sha256": produced["receipt_sha256"],
        "ledger_head": verification["ledger_head"],
    }


def _input_rejection_case(
    name: str,
    cli: Path,
    pack: str,
    repo_root: Path,
    root: Path,
    site: dict,
) -> dict:
    produced = _produce(cli, pack, repo_root, site, root / name)
    return {
        "name": name,
        "passed": produced["returncode"] != 0,
        "observation": {
            "producer_returncode": produced["returncode"],
            "stderr_tail": produced["stderr"],
        },
    }


def adversarial_cases(cli: Path, pack: str, repo_root: Path, root: Path) -> list[dict]:
    cases: list[dict] = []

    float_site = _site("ADV-FLOAT")
    float_site["rehearsal_probe"] = 0.1
    cases.append(_input_rejection_case("float_input_rejected", cli, pack, repo_root, root, float_site))

    unsafe_site = _site("ADV-UNSAFE")
    unsafe_site["rehearsal_probe"] = SAFE_INTEGER_MAX + 1
    cases.append(_input_rejection_case("unsafe_integer_rejected", cli, pack, repo_root, root, unsafe_site))

    non_nfc_site = _site("ADV-NFC")
    non_nfc_site["e\u0301"] = "value"
    cases.append(_input_rejection_case("non_nfc_key_rejected", cli, pack, repo_root, root, non_nfc_site))

    missing_site = _site("ADV-MISSING")
    missing_site.pop("pressure_test_passed")
    produced_missing = _produce(cli, pack, repo_root, missing_site, root / "missing-critical-evidence")
    missing_pass = (
        produced_missing["returncode"] == 0
        and produced_missing.get("outcome") == "REJECT"
        and produced_missing.get("verification", {}).get("status") == "valid"
    )
    cases.append(
        {
            "name": "missing_critical_evidence_fails_closed",
            "passed": missing_pass,
            "observation": {
                "producer_returncode": produced_missing["returncode"],
                "outcome": produced_missing.get("outcome"),
                "verification_status": produced_missing.get("verification", {}).get("status"),
            },
        }
    )

    base = _produce(cli, pack, repo_root, _site("ADV-BASE"), root / "attack-base")
    if base["returncode"] != 0:
        raise RuntimeError(f"failed to produce attack base: {base['stderr']}")
    base_dir = Path(base["evidence_dir"])
    original_pin = base["receipt_sha256"]

    def fresh(name: str) -> Path:
        target = root / name
        shutil.copytree(base_dir, target)
        return target

    target = fresh("byte-tamper")
    findings = target / "findings.json"
    data = bytearray(findings.read_bytes())
    data[-1] ^= 1
    findings.write_bytes(data)
    vr = verify(target)
    cases.append({
        "name": "manifested_byte_tamper_rejected",
        "passed": vr["status"] == "invalid" and any("sha256 mismatch" in e for e in vr["errors"]),
        "observation": {"status": vr["status"], "errors": vr["errors"]},
    })

    target = fresh("unexpected-member")
    (target / ".DS_Store").write_bytes(b"noise")
    vr = verify(target)
    cases.append({
        "name": "unexpected_member_rejected",
        "passed": vr["status"] == "invalid" and any("unexpected bundle file" in e for e in vr["errors"]),
        "observation": {"status": vr["status"], "errors": vr["errors"]},
    })

    target = fresh("receipt-tamper")
    receipt_path = target / "receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["verdict"]["value"] = "deny"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    vr = verify(target)
    cases.append({
        "name": "receipt_verdict_tamper_rejected",
        "passed": vr["status"] == "invalid" and any("locked ledger verdict" in e for e in vr["errors"]),
        "observation": {"status": vr["status"], "errors": vr["errors"]},
    })

    target = fresh("missing-ledger")
    (target / "ledger.jsonl").unlink()
    vr = verify(target)
    cases.append({
        "name": "missing_ledger_rejected",
        "passed": vr["status"] == "invalid",
        "observation": {"status": vr["status"], "errors": vr["errors"]},
    })

    target = fresh("wrong-receipt-pin")
    wrong_pin = "f" * 64 if original_pin != "f" * 64 else "e" * 64
    vr = verify(target, expected_receipt_sha256=wrong_pin)
    cases.append({
        "name": "wrong_external_receipt_pin_rejected",
        "passed": vr["status"] == "invalid" and any("expected external commitment" in e for e in vr["errors"]),
        "observation": {"status": vr["status"], "errors": vr["errors"]},
    })

    target = fresh("coordinated-rewrite")
    rewritten_pin = _recompute_coherent_rewrite(target, "deny")
    unpinned = verify(target)
    pinned = verify(target, expected_receipt_sha256=original_pin)
    cases.append({
        "name": "coordinated_rewrite_detected_by_original_pin",
        "passed": (
            rewritten_pin != original_pin
            and unpinned["status"] == "valid"
            and unpinned["verification"]["integrity"] == "verified"
            and pinned["status"] == "invalid"
            and any("expected external commitment" in e for e in pinned["errors"])
        ),
        "observation": {
            "original_receipt_sha256": original_pin,
            "rewritten_receipt_sha256": rewritten_pin,
            "unpinned_integrity": unpinned["verification"]["integrity"],
            "pinned_status": pinned["status"],
        },
    })

    if len(cases) != 10:
        raise RuntimeError(f"expected 10 adversarial cases, got {len(cases)}")
    return cases


def run(cli: Path, pack: str, result_path: Path) -> dict:
    repo_root = Path(__file__).resolve().parents[1]
    cli = cli.resolve()
    decision_inputs = curated_cases() + generated_cases()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        decisions = [
            _decision_case(cli, pack, repo_root, root, site, index)
            for index, site in enumerate(decision_inputs, 1)
        ]
        attacks = adversarial_cases(cli, pack, repo_root, root)

    agreement_count = sum(1 for item in decisions if item["agreement"])
    integrity_count = sum(1 for item in decisions if item["integrity_verified"])
    adversarial_passed = sum(1 for item in attacks if item["passed"])
    decision_total = len(decisions)
    generated_outcome_counts = {
        outcome: sum(1 for item in decisions[10:] if item["actual"] == outcome)
        for outcome in ("READY", "HOLD", "REJECT")
    }

    passed = (
        decision_total == 20
        and agreement_count == decision_total
        and integrity_count == decision_total
        and len(attacks) == 10
        and adversarial_passed == 10
    )

    report = {
        "artifact_type": "paygod/gas-site-readiness-internal-rehearsal/v0.1",
        "phase": "internal_rehearsal_b1_synthetic",
        "external_pilot": False,
        "regulatory_compliance_claim": False,
        "passed": passed,
        "readiness": "engineering_ready_for_real_cases" if passed else "iterate",
        "coverage": {
            "decision_cases": decision_total,
            "curated_synthetic_cases": 10,
            "generated_synthetic_cases": 10,
            "adversarial_cases": len(attacks),
            "real_historical_cases": 0,
            "independent_human_decisions": 0,
        },
        "metrics": {
            "checklist_paygod_agreement_count": agreement_count,
            "checklist_paygod_agreement_basis_points": (
                agreement_count * 10000 // decision_total if decision_total else 0
            ),
            "clean_integrity_verified_count": integrity_count,
            "false_invalid_count": decision_total - integrity_count,
            "adversarial_passed_count": adversarial_passed,
            "generated_outcome_counts": generated_outcome_counts,
        },
        "decision_results": decisions,
        "adversarial_results": attacks,
        "full_internal_rehearsal_complete": False,
        "external_pilot_ready": False,
        "remaining_before_full_rehearsal": [
            "add real/de-identified historical cases",
            "record independent human decisions before Paygod output is revealed",
            "run recipient-comprehension test with a non-developer",
            "measure evidence-preparation time versus the current process",
            "close browser-verifier parity before counting browser cross-runtime results",
        ],
    }
    result_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", type=Path, required=True)
    parser.add_argument("--pack", default="rehearsals/gas-site-readiness")
    parser.add_argument(
        "--result",
        type=Path,
        default=Path("gas-site-readiness-rehearsal-result.json"),
    )
    args = parser.parse_args()

    report = run(args.cli, args.pack, args.result)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
