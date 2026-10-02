#!/usr/bin/env python3
"""Paygod Internal Verification Challenge v0.1.

This is an engineering rehearsal, not an external pilot.
It pressure-tests the v0.5.1 verification contract and its documented limits.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile

from verify_portable_evidence import (
    SAFE_INTEGER_MAX,
    canonical_json,
    sha256_bytes,
    verify,
)


RUN_TS = "2026-10-03T00:00:00+00:00"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_bundle(root: Path, verdict: str = "allow") -> str:
    root.mkdir(parents=True, exist_ok=True)
    pack = {
        "name": "internal-challenge",
        "version": "0.1.0",
        "path": "packs/internal-challenge",
        "digest_sha256": "1" * 64,
    }
    input_hash = "2" * 64
    ledger_data = {
        "verdict": verdict,
        "rule_name": "challenge-rule",
        "reason": f"challenge verdict: {verdict}",
        "pack": pack,
        "input_hash": input_hash,
        "evidence_refs": [],
    }
    ledger_payload = {
        "previous_hash": "0" * 64,
        "timestamp": RUN_TS,
        "data": ledger_data,
    }
    ledger_head = sha256_bytes(canonical_json(ledger_payload).encode("utf-8"))
    ledger = {
        "entry_index": 0,
        "timestamp": RUN_TS,
        "previous_hash": "0" * 64,
        "data": ledger_data,
        "record_hash": ledger_head,
    }
    ledger_path = root / "ledger.jsonl"
    ledger_path.write_text(json.dumps(ledger, separators=(",", ":")) + "\n", encoding="utf-8")

    findings_path = root / "findings.json"
    findings_path.write_text(
        json.dumps({"api_version": "paygod/v1", "kind": "FindingsReport", "findings": []}) + "\n",
        encoding="utf-8",
    )

    entries = []
    for path in sorted((findings_path, ledger_path), key=lambda p: p.name):
        entries.append({
            "name": path.name,
            "sha256": _sha(path),
            "bytes": path.stat().st_size,
        })

    bundle_digest = hashlib.sha256(
        "".join(f"{x['name']}={x['sha256']}\n" for x in entries).encode("utf-8")
    ).hexdigest()

    manifest = {
        "api_version": "paygod/v1",
        "kind": "Manifest",
        "generated_at": RUN_TS,
        "pack": pack,
        "input": {"canonical_hash": input_hash},
        "bundle": {
            "algorithm": "sha256",
            "digest_method": "sha256(join_lines(name='name=sha256' sorted by name))",
            "file_count": len(entries),
            "bundle_digest": bundle_digest,
        },
        "files": entries,
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest_sha = _sha(manifest_path)

    receipt = {
        "api_version": "paygod/v1",
        "kind": "Receipt",
        "spec_version": "0.2.0",
        "generated_at": RUN_TS,
        "clock": {"value": RUN_TS, "source": "env:PAYGOD_CLOCK"},
        "canonicalization": {"json": "paygod-c14n-v1"},
        "runner": {"image": "paygod/internal-challenge", "image_digest": "unknown"},
        "pack": pack,
        "input": {"canonical_hash": input_hash},
        "bundle": {
            "bundle_digest": bundle_digest,
            "manifest_sha256": manifest_sha,
            "files": entries,
        },
        "verdict": {
            "value": verdict,
            "rule_name": "challenge-rule",
            "reason": f"challenge verdict: {verdict}",
        },
        "replay": {"command": "not performed by integrity verifier"},
    }
    receipt_path = root / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return _sha(receipt_path)


def _coordinated_rewrite(root: Path, verdict: str) -> str:
    """Rewrite all internal commitments coherently.

    This deliberately models the documented trust-boundary limit: without an
    external commitment, a full rewrite can remain internally self-consistent.
    """
    ledger_path = root / "ledger.jsonl"
    manifest_path = root / "manifest.json"
    receipt_path = root / "receipt.json"

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["data"]["verdict"] = verdict
    ledger["data"]["reason"] = f"challenge verdict: {verdict}"
    payload = {
        "previous_hash": ledger["previous_hash"],
        "timestamp": ledger["timestamp"],
        "data": ledger["data"],
    }
    ledger["record_hash"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    ledger_path.write_text(json.dumps(ledger, separators=(",", ":")) + "\n", encoding="utf-8")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        path = root / entry["name"]
        entry["sha256"] = _sha(path)
        entry["bytes"] = path.stat().st_size
    manifest["bundle"]["bundle_digest"] = hashlib.sha256(
        "".join(
            f"{x['name']}={x['sha256']}\n"
            for x in sorted(manifest["files"], key=lambda item: item["name"])
        ).encode("utf-8")
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["bundle"]["files"] = manifest["files"]
    receipt["bundle"]["bundle_digest"] = manifest["bundle"]["bundle_digest"]
    receipt["bundle"]["manifest_sha256"] = _sha(manifest_path)
    receipt["verdict"]["value"] = verdict
    receipt["verdict"]["reason"] = f"challenge verdict: {verdict}"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return _sha(receipt_path)


def _case(name: str, passed: bool, observation: dict) -> dict:
    return {"name": name, "passed": bool(passed), "observation": observation}


def run_challenge() -> dict:
    cases: list[dict] = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "clean"
        receipt_sha = _write_bundle(root)
        result = verify(root, expected_receipt_sha256=receipt_sha)
        cases.append(_case(
            "clean_bundle_scoped_claims",
            result["status"] == "valid"
            and result["verification"]["integrity"] == "verified"
            and result["verification"]["issuer_authenticity"] == "not_verified"
            and result["verification"]["replay"] == "not_performed"
            and result["verification"]["time_authority"] == "producer_supplied"
            and result["receipt_sha256"] == receipt_sha
            and isinstance(result["ledger_head"], str),
            {
                "status": result["status"],
                "verification": result["verification"],
                "receipt_pinned": result["receipt_sha256"] == receipt_sha,
                "ledger_head_present": isinstance(result["ledger_head"], str),
            },
        ))

    rejection_checks = {}
    probes = {
        "float": {"amount": 0.1},
        "unsafe_integer": {"amount": SAFE_INTEGER_MAX + 1},
        "non_nfc_key": {"e" + "\u0301": "value"},
        "unpaired_surrogate": chr(0xD800),
    }
    for label, value in probes.items():
        try:
            canonical_json(value)
            rejection_checks[label] = False
        except Exception:
            rejection_checks[label] = True
    cases.append(_case(
        "restricted_profile_fails_closed",
        all(rejection_checks.values()),
        rejection_checks,
    ))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "byte-tamper"
        _write_bundle(root)
        target = root / "findings.json"
        data = bytearray(target.read_bytes())
        data[-1] ^= 1
        target.write_bytes(data)
        result = verify(root)
        cases.append(_case(
            "manifested_byte_tamper_rejected",
            result["status"] == "invalid"
            and any("sha256 mismatch: findings.json" in err for err in result["errors"]),
            {"status": result["status"], "errors": result["errors"]},
        ))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "unexpected-member"
        _write_bundle(root)
        (root / ".DS_Store").write_bytes(b"noise")
        result = verify(root)
        cases.append(_case(
            "unexpected_member_rejected",
            result["status"] == "invalid"
            and any("unexpected bundle file: .DS_Store" in err for err in result["errors"]),
            {"status": result["status"], "errors": result["errors"]},
        ))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "coordinated-rewrite"
        original_receipt_sha = _write_bundle(root, verdict="allow")
        rewritten_receipt_sha = _coordinated_rewrite(root, verdict="deny")
        unpinned = verify(root)
        pinned = verify(root, expected_receipt_sha256=original_receipt_sha)
        cases.append(_case(
            "coordinated_rewrite_requires_external_pin",
            rewritten_receipt_sha != original_receipt_sha
            and unpinned["status"] == "valid"
            and unpinned["verification"]["integrity"] == "verified"
            and pinned["status"] == "invalid"
            and any("expected external commitment" in err for err in pinned["errors"]),
            {
                "original_receipt_sha256": original_receipt_sha,
                "rewritten_receipt_sha256": rewritten_receipt_sha,
                "unpinned_integrity": unpinned["verification"]["integrity"],
                "pinned_status": pinned["status"],
                "meaning": (
                    "Internal consistency alone cannot distinguish a coherent full rewrite; "
                    "the external receipt commitment detects replacement."
                ),
            },
        ))

    passed = all(case["passed"] for case in cases)
    return {
        "artifact_type": "paygod/internal-verification-challenge/v0.1",
        "phase": "internal_rehearsal",
        "external_pilot": False,
        "passed": passed,
        "case_count": len(cases),
        "cases": cases,
        "non_claims": [
            "does not prove market demand",
            "does not prove willingness to pay",
            "does not authenticate an issuer",
            "does not prove external evidence truth",
            "does not perform decision replay",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--result",
        type=Path,
        default=Path("internal-verification-challenge-result.json"),
    )
    args = parser.parse_args()

    report = run_challenge()
    args.result.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
