# Internal Rehearsal B2 — Historical Case Data Collection Guide

**Workflow:** Gas Site Readiness  
**Classification:** Internal Rehearsal  
**Minimum qualifying cases:** 10 real/de-identified historical or operational cases  
**External pilot:** No  
**Regulatory determination:** No

## 1. Purpose

B2 tests whether the frozen Gas Site Readiness workflow can represent evidence that existed in real operational cases, preserve an independent human judgment, produce a portable decision record, and allow an independent recipient to understand what was and was not verified.

B2 does not test market demand, willingness to pay, regulator approval, production issuer authority, external evidence truth, or autonomous execution authority.

No kernel or policy semantics may be changed merely to improve agreement with real cases.

### External challenge corpus — non-gating

B2 may maintain external diagnostic challenges alongside the qualifying real-case sample:

- `B2-EXT-*` uses independent public historical investigations or records to test evidence boundaries and historical reasoning;
- `B2-SENSOR-*` uses public technical, sensor, telemetry, or prototype material to test software-to-physical evidence boundaries.

External challenges MUST NOT:

- count toward the minimum 10 `B2-REAL-*` cases;
- alter the sampling freeze or readiness gate;
- be rewritten as if they were internal operational cases;
- coerce an external fact into a frozen B2 field merely to make PayGod executable;
- authorize a kernel change from a single observed gap.

External challenges SHOULD bind public sources as precisely as the source permits, separate observed facts from interpretations, and distinguish contemporaneous evidence from post-incident findings. Third-party credentials or secret values must never be copied into the repository.

## 2. Sampling Rule — Freeze Before PayGod Output

The qualifying sample MUST be selected before PayGod results are observed.

Preferred methods:

- consecutive eligible historical cases from a predefined period; or
- a predefined stratified sample based on operational characteristics known before PayGod execution.

Cases MUST NOT be selected because they are expected to make PayGod look correct.

For every excluded case, record the exclusion reason.

Acceptable exclusion reasons include:

- historical evidence cannot be reconstructed sufficiently;
- de-identification cannot be performed safely;
- no independent human review can be obtained;
- evidence available today cannot be separated from evidence that existed at the decision time.

PayGod output MUST NOT be used as an inclusion or exclusion criterion.

## 3. Two-Zone Evidence Handling Model

### Zone A — Restricted Source Vault

Original source material stays outside the public repository.

This zone may contain original certificates, site/customer identifiers, equipment serial numbers, photographs, signatures, emails, source-system records, and original metadata.

Access is restricted to the case custodian.

### Zone B — B2 De-identified Dataset

Only de-identified decision material required for B2 enters the rehearsal dataset.

The public repository contains references and commitments, not raw sensitive source documents.

Recommended pseudonymous identifiers:

- `B2-REAL-001`
- `B2-SITE-001`
- `EVD-B2-001-A`

The mapping between these identifiers and real entities MUST remain outside the repository.

A cryptographic hash of a predictable real identifier (for example a name, phone number, address, project number, or commercial identifier) MUST NOT be treated as sufficient de-identification.

## 4. De-identification Requirements

Before a case enters the qualifying register, remove or replace:

| Category | Treatment |
| --- | --- |
| Person names | Remove or random pseudonym |
| Company/customer names | Random pseudonym unless public and necessary |
| Phone/email | Remove |
| Exact address / coordinates | Remove or generalize |
| National/commercial IDs | Remove |
| Contract/work-order numbers | Random case reference |
| Certificate numbers | Random evidence reference |
| Equipment serial numbers | Random evidence reference |
| Signatures/stamps | Remove from B2 copy |
| QR/barcodes | Remove |
| Image metadata / EXIF | Strip |
| File metadata / author names | Strip |
| Filenames revealing identity | Rename |
| Internal URLs | Replace with evidence reference |

De-identification MUST preserve decision-relevant meaning.

If removing an identifier destroys evidence required by the historical decision, record the limitation explicitly rather than silently rewriting the fact.

## 5. Historical Evidence Cut-off

Only evidence that existed at the historical or operational decision time may be used for the human judgment and PayGod input.

Evidence discovered or created later MUST be classified separately as `post_decision_evidence` and MUST NOT be used to improve the historical case retrospectively.

The case custodian establishes an evidence cut-off before the independent reviewer begins.

## 6. Frozen PayGod Input

Only the existing B2 fields may enter the frozen decision contract:

- `site_id`
- `evidence_site_id`
- `pressure_test_passed`
- `isolation_valves_ready`
- `fire_protection_ready`
- `leak_detection_required`
- `leak_detection_auto_shutoff_ready`
- `preoperation_notification_evidence`
- `warning_signs_installed`

A real-world fact that cannot be represented by these fields MUST NOT be forced into an approximate field.

Examples:

- expired pressure-test certificate: do not silently convert this to `pressure_test_passed=false` if the frozen contract has no validity semantics;
- unknown detector calibration provenance: do not silently convert this to `leak_detection_auto_shutoff_ready=false` if readiness and provenance are distinct facts.

Record such facts as unrepresentable evidence.

## 7. Independent Human Judgment

The independent reviewer MUST record a judgment before seeing PayGod output.

Allowed decisions:

- `READY`
- `HOLD`
- `REJECT`

Record:

- reviewer role, not personal identity;
- decision;
- evidence references actually relied upon;
- important evidence considered;
- evidence that affected the decision but cannot be represented in the frozen PayGod contract.

The pre-PayGod judgment MUST NOT be overwritten after PayGod output is revealed. A later interpretation may be recorded separately.

## 8. PayGod Execution

After the human judgment is frozen:

1. Produce the normalized frozen B2 input.
2. Run PayGod.
3. Record `READY`, `HOLD`, or `REJECT`.
4. Produce the evidence bundle.
5. Verify bundle integrity independently.
6. Record issuer-authenticity state as `verified`, `not_verified`, or `failed`.
7. Preserve the original machine-readable result.

The operator MUST NOT modify case input to force agreement.

## 9. Agreement and Gap Classification

Every case records `agreement=true|false`.

A disagreement MUST receive exactly one primary classification from the existing B2 contract:

- `policy_ambiguity`
- `missing_evidence`
- `human_error`
- `contract_gap`
- `provenance_gap`
- `kernel_defect`

More detailed analysis may be recorded as a secondary subtype without changing the primary B2 taxonomy.

Recommended secondary subtypes include:

| Primary class | Example subtype |
| --- | --- |
| `contract_gap` | `validity_window` |
| `contract_gap` | `missing_field_semantics` |
| `provenance_gap` | `issuer_identity` |
| `provenance_gap` | `calibration_provenance` |
| `provenance_gap` | `time_authority` |
| `missing_evidence` | `document_unavailable` |
| `policy_ambiguity` | `rule_interpretation` |
| `human_error` | `overlooked_evidence` |
| `kernel_defect` | `incorrect_evaluation` |

Secondary subtypes are diagnostic only and do not alter the primary class consumed by the current readiness checker.

## 10. Timing Protocol

Use the same start/stop definition for every case.

### Evidence preparation time
Start: operator opens the historical evidence set.  
Stop: frozen normalized B2 input and evidence references are ready.

### Human decision time
Start: independent reviewer begins examining the prepared evidence.  
Stop: `READY/HOLD/REJECT` is recorded.

### PayGod produce + verify time
Start: PayGod execution starts.  
Stop: the portable evidence bundle completes independent verification.

### Baseline reconstruction time
Start: recipient receives the ordinary checklist/spreadsheet evidence set.  
Stop: recipient can reconstruct the decision and supporting evidence.

### PayGod reconstruction time
Start: recipient receives the PayGod bundle/verifier.  
Stop: recipient can identify the decision, commitments, and verification boundaries.

Do not compare unlike timing categories as if they measured the same operational activity.

## 11. Recipient Comprehension

Recipient testing occurs without producer coaching during the verification task.

Record whether the recipient can correctly explain:

- what integrity verification established;
- what integrity verification did not establish;
- issuer-authenticity status;
- whether decision replay occurred;
- whether time authority was externally trusted;
- whether underlying evidence truth was proven.

Any misunderstanding that could materially change reliance on the result is recorded as `material_confusion=true`.

The current B2 readiness contract measures qualifying independent non-developer verification events and must not be silently changed during collection.

## 12. Non-gating Gap Register

Maintain a separate diagnostic gap register with:

- `case_id`
- `primary_gap_class`
- `secondary_gap_subtype`
- `observed_fact`
- `why_current_contract_cannot_resolve_it`
- `layer_candidate`
- `requires_kernel_change`
- `notes`

Suggested `layer_candidate` values:

- `pack`
- `evidence_profile`
- `adapter`
- `trust_profile`
- `human_process`
- `unknown`

This field is diagnostic only. It does not authorize implementation.

## 13. Stop-Build Rule During B2

A discovered gap does not authorize immediate coding.

For every gap:

**Observe → classify → count recurrence → assess operational importance → then decide whether architecture work is justified.**

No kernel change may be made unless the evidence supports `kernel_defect`.

Contract, provenance, time, source-authentication, and workflow deficiencies remain recorded for post-B2 design.

## 14. B2 Exit Evidence

B2 produces:

- qualifying case register;
- independent human judgments;
- agreement/disagreement analysis;
- gap register;
- timing comparison;
- recipient-comprehension register;
- verified evidence bundles;
- one-page readiness report.

A passing B2 means only that the bounded workflow is sufficiently understood to proceed to design-partner discovery under the repository roadmap.

It does not prove product-market fit, demand, regulatory acceptance, production source truth, production issuer authorization, or authority to execute operational or financial actions.
