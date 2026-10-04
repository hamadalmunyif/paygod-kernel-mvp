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

If a real human decision depends on evidence outside these fields, record that evidence as **unrepresentable** and do not silently translate it into an existing field. Any later `contract_gap` or `provenance_gap` classification requires the normal diagnostic/comparison process; non-executability alone does not create a formal gap.

### Pre-kernel evidence admission boundary

B2 now makes the pre-kernel boundary explicit:

Claim / source evidence
→ semantic representability
→ historical/provenance admission
→ TRUE | FALSE | WITHHELD
→ Executability Gate
→ PayGod only when the frozen input is complete.

WITHHELD is a pre-kernel mapping/admission state. It is not a third boolean value in the kernel or policy DSL.

NOT RUN is an orchestration result produced before the kernel when a faithful complete frozen input cannot be constructed. It is not READY, HOLD, REJECT, allow, flag, or deny.

## Case order

For every candidate selected by the frozen sampling rule:

1. Capture only evidence that existed at the historical/operational decision time.
2. Remove confidential/personal identifiers where required.
3. The independent human decider records READY | HOLD | REJECT before seeing PayGod output.
4. Record what evidence the human used and any normative/professional basis separately.
5. Map each source fact to the frozen B2 fields without semantic coercion.
6. Apply evidence admission. Missing, unproven, or semantically insufficient evidence may produce WITHHELD.
7. Apply the Executability Gate.
8. If any required frozen field remains WITHHELD, record NOT RUN and preserve the candidate without inventing input values.
9. Only an executable candidate becomes a qualifying B2 case and enters PayGod.
10. For an executed case, record agreement/disagreement and classify every disagreement as exactly one primary class:
   - policy_ambiguity
   - missing_evidence
   - human_error
   - contract_gap
   - provenance_gap
   - kernel_defect
11. Measure timing against the simple checklist/spreadsheet baseline.
12. Produce and independently verify the evidence bundle for executed cases.
13. Do not modify the kernel unless the classified cause is kernel_defect.

## Candidate vs qualifying cases

The frozen sampling rule creates the candidate population before PayGod output is known. Every selected candidate is retained in candidate-register.csv, including candidates that later become NOT RUN.

A candidate is qualifying only when the historical cut-off is established, the human judgment is frozen, the frozen fields can be represented and admitted without coercion, and the Executability Gate passes.

A candidate MUST NOT be silently replaced because evidence is incomplete, because it becomes NOT RUN, or because its eventual outcome is inconvenient. If the pre-frozen sampling rule needs an extension to obtain the minimum qualifying count, that extension must be recorded before observing PayGod output for the added candidates.

## B2 minimums

- >= 10 qualifying real/de-identified cases, with all candidates from the frozen sampling rule retained.
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
