# Trivy severity + typed-v1 composition (RESEARCH ONLY)

**Status: DRAFT / INTERNAL REHEARSAL / NOT ACCEPTED.** No scanner is executed by this isolated Pack, no production deployment is permitted, and no `allow` rule exists.

## Hypothesis

A new versioned non-permitting Trivy severity Pack can opt into the proposed `typed-v1` evaluation profile without changing the legacy `critical-cve-blocker` v1 or any historical receipt. `Status=fixed` from Trivy means vendor fix availability; observed HIGH/CRITICAL findings still deny.

## Witness and its boundaries

- 8 valid-source synthetic fixture outcomes adapted from research PR #119; missing source and missing list deliberately **not** treated as ordinary `unknown` fixtures under strict evaluation.
- `tools/test_trivy_typed_composition.py` exercises the actual canonical CLI: HIGH/CRITICAL -> deny, MEDIUM -> flag, LOW only -> canonical `error` (not allow), missing vulnerability array / wrong severity type / duplicate raw JSON keys -> exit 2 and **no output directory**.
- All tests use a fictional pinned OCI digest. No vendor-version comparator, signed Trivy execution, complete scan, independent receipt trust root, issuer mandate, replay or time verification is established.
- Structural shape checks are not authenticity checks; evidence from an external source requires separate admission under ADR 0003 before Kernel invocation.

## Source boundaries

- Base: proposal PR #115 (typed-v1), not canonical Kernel `main`.
- Severity source: separate prototype PR #119; this is a **composition experiment**, not a replacement or merge of that draft.
- Parallel signed source/receiver experiment: PR #121, which remains research-only and independent.
- Source milestones do not imply Issue #111 or #116 closure.

## Acceptance and falsifier

An unexpected canonical `allow`, a malformed input yielding a Receipt, breaking frozen legacy CI, or any difference between documented and observed source SHA is FAIL. Native Trivy severity blocking and GitHub attestations are existing baselines. Owners must review ADR 0004 and source-admission contract before any merge to canonical main.

Reproduce in reviewed GitHub CI with `./out/paygod test --pack examples/eik-trivy-severity-typed-research` and `python3 tools/test_trivy_typed_composition.py --cli ./out/paygod`.