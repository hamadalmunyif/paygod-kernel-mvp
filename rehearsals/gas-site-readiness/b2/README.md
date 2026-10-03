# Gas Site Readiness — Internal Rehearsal B2

**Status: NOT READY — awaiting real/de-identified cases.**

This is an Internal Rehearsal, not an external pilot and not a regulatory compliance determination.

B1 proved the engineering path on synthetic/adversarial cases. B2 asks a different question:

> Can the same bounded decision workflow represent real evidence, preserve an independent human judgment, produce a portable decision record, and let a recipient verify it without confusing integrity with truth or authority?

## Frozen workflow for B2

Decision:

**Is this site / installation ready for handover or operation under the rehearsal evidence policy?**

Outputs:

- `READY`
- `HOLD`
- `REJECT`

B2 reuses the already-tested B1 evidence fields and policy. Do **not** add or change kernel semantics merely to make a real case pass.

Current evidence fields:

- `site_id`
- `evidence_site_id`
- `pressure_test_passed`
- `isolation_valves_ready`
- `fire_protection_ready`
- `leak_detection_required`
- `leak_detection_auto_shutoff_ready`
- `preoperation_notification_evidence`
- `warning_signs_installed`

If a real human decision depends on evidence outside these fields, record it as a **contract gap** or **provenance gap**. Do not silently translate it into an existing field.

## Case order

For every real/de-identified case:

1. Capture only evidence that existed at the historical/operational decision time.
2. Remove confidential/personal identifiers where required.
3. The independent human decider records `READY | HOLD | REJECT` **before** seeing PayGod output.
4. Record what evidence the human used.
5. Run PayGod with the frozen B1 policy.
6. Record agreement/disagreement.
7. Classify every disagreement as exactly one primary class:
   - `policy_ambiguity`
   - `missing_evidence`
   - `human_error`
   - `contract_gap`
   - `provenance_gap`
   - `kernel_defect`
8. Measure timing against the simple checklist/spreadsheet baseline.
9. Produce and independently verify the evidence bundle.
10. Do not modify the kernel unless the classified cause is `kernel_defect`.

## B2 minimums

- >= 10 real/de-identified cases.
- independent human judgment for every case.
- every disagreement classified.
- >= 5 recipient verifications by a non-developer without producer assistance.
- no material confusion about integrity vs authenticity vs replay vs trusted time.
- no unexplained browser/standalone mismatch.
- integrity attacks remain fail-closed.
- at least one measurable advantage over checklist/spreadsheet baseline, or a capability the baseline cannot provide (for example tamper detection).

## Non-claims even after PASS

B2 does not prove:
- market demand;
- willingness to pay;
- regulator approval;
- external evidence truth;
- production issuer authorization;
- permission to move money or execute an operational action.

Use `tools/check_b2_readiness.py` to calculate the readiness gate from the case and recipient registers.
