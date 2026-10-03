#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

DECISIONS = {"READY", "HOLD", "REJECT"}
DISAGREEMENTS = {
    "policy_ambiguity",
    "missing_evidence",
    "human_error",
    "contract_gap",
    "provenance_gap",
    "kernel_defect",
}
SOURCE_TYPES = {"real_deidentified", "operational_deidentified"}
BOOL_TRUE = {"true", "1", "yes"}
BOOL_FALSE = {"false", "0", "no"}


def _bool(value: str, field: str) -> bool:
    normalized = (value or "").strip().lower()
    if normalized in BOOL_TRUE:
        return True
    if normalized in BOOL_FALSE:
        return False
    raise ValueError(f"{field} must be true/false")


def _seconds(value: str, field: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric seconds") from exc
    if parsed < 0:
        raise ValueError(f"{field} must be >= 0")
    return parsed


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def evaluate(root: Path) -> dict:
    case_path = root / "rehearsals/gas-site-readiness/b2/case-register.csv"
    recipient_path = root / "rehearsals/gas-site-readiness/b2/recipient-comprehension.csv"
    engineering_path = root / "rehearsals/gas-site-readiness/b2/engineering-evidence.json"

    cases = [row for row in _read_csv(case_path) if (row.get("case_id") or "").strip()]
    recipients = [
        row for row in _read_csv(recipient_path)
        if (row.get("recipient_id") or "").strip()
    ]
    engineering = json.loads(engineering_path.read_text(encoding="utf-8"))

    errors: list[str] = []
    qualifying_cases = []
    agreement_count = 0
    disagreement_count = 0
    timing_advantage_count = 0

    seen_ids: set[str] = set()
    for index, row in enumerate(cases, start=2):
        prefix = f"case-register.csv row {index}"
        case_id = (row.get("case_id") or "").strip()
        if case_id in seen_ids:
            errors.append(f"{prefix}: duplicate case_id {case_id}")
            continue
        seen_ids.add(case_id)

        source_type = (row.get("source_type") or "").strip()
        if source_type not in SOURCE_TYPES:
            errors.append(f"{prefix}: source_type must be one of {sorted(SOURCE_TYPES)}")
            continue

        try:
            deidentified = _bool(row.get("deidentified", ""), f"{prefix} deidentified")
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not deidentified:
            errors.append(f"{prefix}: public-repository B2 register requires deidentified=true")
            continue

        human = (row.get("human_decision") or "").strip().upper()
        paygod = (row.get("paygod_decision") or "").strip().upper()
        if human not in DECISIONS:
            errors.append(f"{prefix}: human_decision must be READY/HOLD/REJECT")
        if paygod not in DECISIONS:
            errors.append(f"{prefix}: paygod_decision must be READY/HOLD/REJECT")
        if not (row.get("decision_owner_role") or "").strip():
            errors.append(f"{prefix}: decision_owner_role is required")
        if not (row.get("human_evidence_refs") or "").strip():
            errors.append(f"{prefix}: human_evidence_refs is required")

        try:
            agreement = _bool(row.get("agreement", ""), f"{prefix} agreement")
        except ValueError as exc:
            errors.append(str(exc))
            agreement = None

        disagreement = (row.get("disagreement_class") or "").strip()
        if agreement is True:
            agreement_count += 1
            if disagreement:
                errors.append(f"{prefix}: disagreement_class must be blank when agreement=true")
        elif agreement is False:
            disagreement_count += 1
            if disagreement not in DISAGREEMENTS:
                errors.append(
                    f"{prefix}: disagreement_class must be one of {sorted(DISAGREEMENTS)}"
                )

        try:
            integrity = _bool(
                row.get("integrity_verified", ""),
                f"{prefix} integrity_verified",
            )
            if not integrity:
                errors.append(f"{prefix}: clean real-case bundle integrity must verify")
        except ValueError as exc:
            errors.append(str(exc))

        issuer = (row.get("issuer_authenticity") or "").strip().lower()
        if issuer not in {"verified", "not_verified", "failed"}:
            errors.append(
                f"{prefix}: issuer_authenticity must be verified/not_verified/failed"
            )

        timing = {}
        for field in (
            "evidence_prep_seconds",
            "human_decision_seconds",
            "paygod_produce_verify_seconds",
            "baseline_reconstruction_seconds",
            "paygod_reconstruction_seconds",
        ):
            try:
                timing[field] = _seconds(row.get(field, ""), f"{prefix} {field}")
            except ValueError as exc:
                errors.append(str(exc))

        if (
            "paygod_reconstruction_seconds" in timing
            and "baseline_reconstruction_seconds" in timing
            and timing["paygod_reconstruction_seconds"]
            < timing["baseline_reconstruction_seconds"]
        ):
            timing_advantage_count += 1

        qualifying_cases.append(case_id)

    comprehension_pass = False
    qualifying_recipients = 0
    for index, row in enumerate(recipients, start=2):
        prefix = f"recipient-comprehension.csv row {index}"
        try:
            non_dev = _bool(row.get("non_developer", ""), f"{prefix} non_developer")
            independent = _bool(
                row.get("independent_from_producer", ""),
                f"{prefix} independent_from_producer",
            )
            material_confusion = _bool(
                row.get("material_confusion", ""),
                f"{prefix} material_confusion",
            )
            explains = [
                _bool(row.get(field, ""), f"{prefix} {field}")
                for field in (
                    "explains_integrity_correctly",
                    "explains_not_verified_truth_correctly",
                    "explains_issuer_authenticity_correctly",
                    "explains_replay_correctly",
                    "explains_time_authority_correctly",
                )
            ]
            bundles = int((row.get("bundles_verified") or "").strip())
            if bundles < 0:
                raise ValueError(f"{prefix} bundles_verified must be >= 0")
        except (ValueError, TypeError) as exc:
            errors.append(str(exc))
            continue

        if non_dev and independent:
            qualifying_recipients += 1
            if bundles >= 5 and all(explains) and not material_confusion:
                comprehension_pass = True

    tamper_advantage = bool(
        engineering.get("baseline_capability_advantage", {}).get("tamper_detection")
    )
    measurable_advantage = timing_advantage_count > 0 or tamper_advantage

    criteria = {
        "real_deidentified_case_count_at_least_10": len(qualifying_cases) >= 10,
        "independent_human_judgment_for_all_cases": (
            len(qualifying_cases) >= 10
            and all(
                (row.get("human_decision") or "").strip().upper() in DECISIONS
                for row in cases
            )
        ),
        "every_disagreement_classified": all(
            (
                _safe_bool(row.get("agreement", "")) is not False
                or (row.get("disagreement_class") or "").strip() in DISAGREEMENTS
            )
            for row in cases
        ),
        "recipient_comprehension_pass": comprehension_pass,
        "timing_captured_for_all_cases": (
            len(qualifying_cases) >= 10
            and all(
                _has_numeric_timings(row)
                for row in cases
            )
        ),
        "baseline_advantage_demonstrated": measurable_advantage,
        "browser_manual_witness_recorded": (
            engineering.get("browser_witness", {}).get("external_receipt_pin_correct")
            == "matched"
            and engineering.get("browser_witness", {}).get("external_receipt_pin_altered")
            == "fail_closed"
        ),
        "issuer_authentication_engineering_witness": (
            engineering.get("issuer_authentication", {}).get(
                "signed_bundle_with_recipient_demo_trust"
            )
            == "verified"
        ),
        "engineering_evidence_does_not_substitute_for_real_cases": (
            engineering.get("real_case_evidence_substitute") is False
        ),
    }

    ready = not errors and all(criteria.values())
    return {
        "artifact_type": "paygod/internal-rehearsal-b2-readiness/v0.1",
        "workflow": "gas-site-readiness",
        "ready": ready,
        "recommendation": (
            "READY_FOR_DESIGN_PARTNER_DISCOVERY" if ready else "ITERATE"
        ),
        "counts": {
            "real_deidentified_cases": len(qualifying_cases),
            "agreements": agreement_count,
            "disagreements": disagreement_count,
            "recipient_rows": len(recipients),
            "qualifying_independent_non_developer_recipients": qualifying_recipients,
            "cases_with_reconstruction_time_advantage": timing_advantage_count,
        },
        "criteria": criteria,
        "validation_errors": errors,
        "non_claims": [
            "market demand",
            "willingness to pay",
            "regulator approval",
            "production issuer authorization",
            "external evidence truth",
            "autonomous execution authority",
        ],
    }


def _safe_bool(value: str):
    normalized = (value or "").strip().lower()
    if normalized in BOOL_TRUE:
        return True
    if normalized in BOOL_FALSE:
        return False
    return None


def _has_numeric_timings(row: dict[str, str]) -> bool:
    try:
        for field in (
            "evidence_prep_seconds",
            "human_decision_seconds",
            "paygod_produce_verify_seconds",
            "baseline_reconstruction_seconds",
            "paygod_reconstruction_seconds",
        ):
            _seconds(row.get(field, ""), field)
        return True
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON output path.",
    )
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Exit nonzero unless all B2 exit criteria are satisfied.",
    )
    args = parser.parse_args()

    result = evaluate(args.root)
    rendered = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    if result["validation_errors"]:
        return 2
    if args.require_ready and not result["ready"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
