# Internal Rehearsal B2 — Readiness Report

**Workflow:** Gas Site Readiness  
**Status:** NOT READY — awaiting real/de-identified cases  
**External pilot:** No

## Case evidence

- real/de-identified cases: **0 / 10 minimum**
- independent human judgments: **0**
- human/PayGod agreements: **not measured**
- disagreements classified: **not measured**

## Evidence gaps

Not measured yet.

Required classification for each disagreement:
- policy ambiguity
- missing evidence
- human error
- contract gap
- provenance gap
- kernel defect

## Timing / baseline

Not measured yet.

Required per case:
- evidence preparation time;
- human decision time;
- PayGod production + verification time;
- checklist/spreadsheet reconstruction time;
- PayGod reconstruction/verification time.

Do not claim operational value until at least one measurable dimension beats the simple baseline or adds a capability the baseline does not provide.

## Recipient comprehension

- independent non-developer recipient verifications: **0 / 5 minimum**
- material confusion: **not measured**

Recipient must explain:
- what integrity verification established;
- what it did not establish;
- whether issuer authenticity was verified;
- whether replay occurred;
- whether time was externally trusted.

## Engineering witnesses already available

- B1 synthetic decision agreement: 20/20.
- B1 clean integrity verification: 20/20.
- B1 adversarial expectations: 10/10.
- production mobile-browser external receipt pin: correct pin MATCH / altered pin FAIL CLOSED.
- detached Ed25519 issuer authentication implemented and browser/Python tested.
- production mobile-browser signed demo:
  - without recipient trust anchor -> issuer authenticity NOT VERIFIED;
  - with recipient-supplied demo trust store -> issuer authenticity VERIFIED.

These are engineering witnesses. They do not substitute for real B2 cases.

## P0 workflow / evidence-admission witness

P0 — Gas Maintenance Workflow & Evidence-Admission Pilot is closed as a simulated shadow pilot with a bounded PASS.

- classification: simulated_shadow_pilot
- external pilot: false
- counts as B2 real: false
- simulated cases: 15
- frozen reviewer outcomes: READY 0 / HOLD 9 / REJECT 6
- executable cases after strict mapping/admission: 0 / 15
- PayGod executions for the P0 15-case sample: 0
- NOT RUN cases: 15 / 15
- kernel change: none
- frozen Gas Site Readiness pack change: none

P0 demonstrated the workflow boundary that missing, temporally unproven, or semantically insufficient evidence is not silently coerced into a boolean merely to make the kernel executable. It does not substitute for the B2 real/de-identified case minimum.

Source records and detailed mapping are referenced by the P0 manifest and registers under rehearsals/gas-site-readiness/p0-maintenance-workflow/.

## Remaining non-claims

Even a passing B2 does not prove:
- demand or willingness to pay;
- regulator approval;
- production issuer authorization;
- external evidence truth;
- autonomous execution.

## Gate result

**Current recommendation: ITERATE / COLLECT REAL CASES**

Do not set `ready_for_design_partner_discovery` until `tools/check_b2_readiness.py --require-ready` exits successfully.
