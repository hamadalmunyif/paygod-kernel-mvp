# Independent receiver protocol — Trivy native-only vs PayGod bound receipt

**Status: PROPOSED / NOT RUN WITH EXTERNAL PERSON OR ORGANIZATION.**  
Scope: **public test image, deny-only research**, not approval to deploy, pay, release, certify or process private customer information. This is an **experimental handoff protocol**, not an invitation to transfer real credentials or sensitive scanner reports.

## Research question and possible answer

Does an independently reviewing party gain a measurable improvement in understanding, validating or defending a policy-specific **deny** decision from PayGod, compared with the *native baseline alone*: Trivy severity-gate exit status plus GitHub-native signed Trivy report and signed workflow execution record?

**NATIVE_SUFFICIENT is an acceptable result.** PayGod must not be credited for native Trivy finding/blocking, native GitHub signing, or standard SHA256 verification.

## Strict artifacts and evidence boundary

A consenting outsider receives TWO parallel independently checkable presentations:

1. **Native-only**: immutable image digest, raw Trivy JSON report and its SHA256, GH Artifact Attestation/verification instructions with trusted repository/workflow/commit/run references, signed execution-observation JSON and native HIGH/CRITICAL blocking result (exact command/exit), plus limitations of scanner completeness and advisory truth.
2. **PayGod extension**: the *same* native artifacts, **plus** the standalone PayGod CLI-produced read-only denial receipt, its bundled integrity manifest/ledger/plan/findings, bound normalized input and receipt digest, and a **clearly marked, separately pinned** relying-party expected receipt SHA. Recipient verifies native GH provenance, scoped PayGod integrity and raw report + signed execution record → normalized input → receipt canonical hash.

**Important:** the current internal Windows comparison receives `EXPECTED_RECEIPT_SHA` directly from our *producer job*. This is NOT an independently authenticated pin. A real outside test must obtain an expected receipt digest from an **independently vetted signer/out-of-band channel** and document who actually vouches for that pin. A sender-controlled copied hash cannot establish an issuer's institutional authority.

GH attestation verification is only accepted with exact trust inputs: repository, signer workflow path, source branch/ref, exact code commit and trusted `run ID/attempt` references. Current `gh attestation verify` pins repo/workflow/ref/digest; the extra observed `workflow_run_id/attempt` comparison is done by our bridge/receiver to an **explicit expected value**. This additionally limits same-commit cross-run substitution **within the internal study**; an external relying party needs an independently established expected run identity.

## Experimental procedure (blind where practical)

- Reviewer A receives native-only package first; Reviewer B receives PayGod extension first; switch in a second round with different blinded, permitted test material. Record order effects, confidence and starting familiarity. Do not expose the previously frozen AP2 blind Pass A materials or silently redefine AP2 Pass B.
- Ask reviewer to check: (i) whether HIGH/CRITICAL findings exist under stated policy; (ii) report subject/scan context; (iii) policy owner/source; (iv) whether the record really forbids release; (v) whether the hash/signature/receipt is portable without project-owner assistance; (vi) what is **not** proven.
- Provide three adversarial packages: tampered raw report, GH-signed execution statement mismatched to expected run/attempt, and intact native report with a modified PayGod receipt/normalized source SHA. Observe whether reviewers correctly refuse or mark `INCONCLUSIVE`, not just whether CLI exits nonzero.
- Record time-to-first-correct-independent-verification, commands/interventions needed, false-confidence errors, omitted limitations, required support minutes and downstream maintenance cost.
- Reviewer is *outside our repository/workflow environment*, has not developed this Pack, uses their own machine/credential boundary, and has consent. A second GitHub-hosted job on our account remains **INTERNAL_TECHNICAL_RECEIVER**, not a qualified independent recipient.
- Do not require reviewers to reveal company proprietary artifacts, real vulnerabilities, full credentials, personal data or customer source files. Use public synthetic/redistributable fixtures unless a separate authorized agreement says otherwise.

## Required submission / scoring

Record for each arm:

| Field | Accepted values / evidence |
| --- | --- |
| reviewer_id | pseudonym under reviewer control; no name/email in public repo |
| arm | `native_only` or `native_plus_paygod` |
| first_time_minutes | nonnegative measurement or `NOT_MEASURED` |
| correct_signature_and_sha | `PASS / FAIL / NOT_RUN` |
| decision_scope_understood | `PASS / FAIL / NOT_RUN` |
| issuer_and_time_limit_understood | `PASS / FAIL / NOT_RUN` |
| observed_false_confidence | `YES / NO / NOT_MEASURED` |
| negative_mutation_result | `REJECTED / ACCEPTED / NOT_RUN` |
| reviewer_support_minutes | nonnegative measurement or `NOT_MEASURED` |
| value_over_native | `DEMONSTRATED / NATIVE_SUFFICIENT / INCONCLUSIVE` |
| provenance_link | exact public URL to commands/outputs **after consent and redaction** |

No reviewer result or metric currently exists. Never replace `NOT_MEASURED` with 0, `NOT_RUN` with PASS, or a success in our own Windows CI with an external human outcome.

## Promotion criteria (not automatic)

1. **Source:** independently authenticated producer identity and command/subject/completeness scope; different vendor advisory / Trivy database updates may alter findings. Preserve original raw bytes.
2. **Policy:** authorized owner, versioned policy semantics, exact source schema and scope; optional typed-v1 changes only after separate #115/ADR decision. No release permit granted by a deny-only demonstration.
3. **Receipt:** canonical Kernel alone mints identity, no adapter-generated verdict; independent receiver authenticates expected receipt pin and correct signer authority beyond integrity alone.
4. **Recipient:** unaffiliated reviewer independently verifies the package, explains nonclaims, and compares native baseline.
5. **Value:** measured native + PayGod improvement (or honest native sufficiency). Do not infer commercial adoption from verified artifacts.

A completed internal source/receipt demonstration may satisfy a **technical prerequisite**, but it does **not** close [issue #116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116), [EIK #114](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/114), or update B2-REAL counts without a separately qualified human/recipient witness.
