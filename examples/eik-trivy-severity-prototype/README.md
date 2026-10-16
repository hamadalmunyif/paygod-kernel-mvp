# Trivy severity non-permit Pack — research prototype, v2

**Status: RESEARCH / SYNTHETIC FIXTURES ONLY / NO ALLOW / NOT A TRIVY RELEASE GATE.**

Purpose: demonstrate an explicit *separate* policy surface on canonical Kernel `main@d347213848f03a6d25554631d0183a682879b11b` which **does not confuse Trivy advisory `Status=fixed` with installed remediation**. Unlike current `critical-cve-blocker` v1, it uses **native Trivy severity**, *not* CVSS ×10. It is therefore **not a drop-in upgrade** for the original numeric CVSS policy and it does not claim production-scanner completeness, package remediated state, trusted time, or deployment authorization.

## What the prototype demonstrates

- `HIGH`/`CRITICAL` observed findings → canonical policy `deny` in fixtures, even if raw `trivy_status=fixed`.
- `MEDIUM` observed findings → `flag`, if no severe finding.
- `LOW`, an empty array, missing report, or unknown severity → **`unknown`, never `allow`**. An `unknown` produced by the legacy Kernel is not automatically `WITHHELD_NOT_RUN`; an external caller must refuse unauthorized or incomplete input **before** invoking Kernel.
- No rule emits `allow`. This reduces false permissions in this *specific* synthetic Pack, but does not establish that arbitrary malformed input is safe or admitted.
- The Pack's declared `required` JSON Schema applies only to an **opt-in** external structural admission command, not universally to direct `paygod run`. Missing fields must return external `WITHHELD_NOT_RUN` and **no Kernel call** in any actual EIK workflow. Unit policy fixture tests intentionally exercise unadmitted missing inputs to make the non-permit ceiling observable.

## Hermetic tests

```bash
./out/paygod test --pack examples/eik-trivy-severity-prototype
python3 tools/test_trivy_severity_nonpermit.py
```

The first runs synthetic `deny`/`flag`/`unknown` evaluations; the second checks that the Pack has **no `allow` rule** and the source input admission is actually required before use. It does not transform a real Trivy report or authenticate a scanner.

## Native counterfactual

Trivy itself already blocks a scanned image if `--severity HIGH,CRITICAL --exit-code 1` is configured. A [genuine public-image comparator run](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923531022) observed exactly this behavior with 2 HIGH findings; native blocking succeeded *without PayGod*. So this prototype **does not create incremental security blocking**. The research hypothesis is a **portable, independently understood decision/evidence handoff**, which requires a separate authorized real-source ingestion, signed provenance, external receiver and neutral native control.

## Required next gates

1. Keep [original v1 Pack](../../packs/core/critical-cve-blocker/pack.yaml) unchanged to preserve historic receipts. Preserve the [RED defect witness #117](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/117).
2. Separately review [Trivy shadow PR #118](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/118) and trusted source requirements in [Issue #116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116).
3. If non-permit behavior and admission are accepted, connect an **explicitly admitted real source**, then run canonical Kernel CLI/standalone verifier with negative mutation, no fake receipt, and external-recipient comparison. This prototype alone does **not** close #116.
4. [Typed evaluation PR #115](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/115) addresses a separate DSL type-coercion issue. This prototype intentionally does **not** depend on that unmerged change; no blanket typed security claim is made.
