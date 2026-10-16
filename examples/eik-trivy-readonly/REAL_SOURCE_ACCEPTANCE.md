# Trivy EIK real-source acceptance protocol — OPEN / NOT EXECUTED

Status: **PROPOSED, RESEARCH / SOURCE ADMISSION ONLY** (2026-10-16)  
Issue: [Kernel #116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116)  
RED witness: [PR #117](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/117), [CI run 38919551876](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38919551876)  
Synthetic shadow: [PR #118](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/118)

**This protocol is not a completed Trivy integration and does not authorize any actual deployment or release.** It does not declare any current branch merge-ready. Never change or rewrite the original RED witness.

## Why the issue cannot be closed by a green shadow test

Upstream Trivy issue [discussion #11021, maintainer response July 30, 2026](https://github.com/aquasecurity/trivy/discussions/11021) confirms `Status=fixed` means that a fix is available from the advisory/vendor, not that the installed version contains a fix. See [native filtering semantics](https://trivy.dev/docs/latest/configuration/filtering/), [JSON reporting](https://trivy.dev/docs/latest/configuration/reporting/), and [vendor advisory/backport selection](https://trivy.dev/docs/latest/scanner/vulnerability/).

Current canonical `critical-cve-blocker` v1 uses `v.status != 'fixed'`. The synthetic high-critical `Status=fixed` case in PR #117 reproduces **Expected deny / Got allow**. The EIK shadow in PR #118 deliberately cannot call Kernel or emit an allow. Hence the repair still needs a permissioned actual source, an independently inspectable producer witness, and a new *versioned* policy admission and decision path. Approval requires a separate ADR if Kernel semantics or canonical schema change.

## Threat model and trust ceilings

Treat the following as four **separate** proofs:

1. **Record syntax and domain admission:** JSON SchemaVersion/field/subject shape, fail-closed handling of missing, duplicate, invalid, unknown status and mandatory source fields. A parser can test this on saved reports and synthetic data.
2. **Genuine scan and subject provenance:** hash of raw report, exact scanner executable/version + invocation flags/config/policy, immutable container subject digest, OS/package scanning scope and immutable CI job identity, authenticated producer context, exit status and logs. A JSON field or caller-supplied `--scanner-exit-code` is **not proof** of any of these.
3. **A versioned PayGod decision:** separately accepted Pack, schema/admission, canonical Kernel invocation and artifact identity. No adapter, PostHog event, browser site, tracer or scanner claims to have minted this.
4. **Independent recipient and value:** someone not working in producer's workspace verifies the transferred canonical bundle and expected receipt commitment, and compares the result with native Trivy + GitHub Attestations without PayGod. `NATIVE_SUFFICIENT` is valid.

No later claim may be inferred from an earlier one. **In particular, `fixed` never equals `installed_remediated` by default.**

## Evidence acquisition — first independently checkable test

Use a non-confidential, publicly redistributable or otherwise properly permissioned test image. No credentials, customer/third-party repositories, scan history or proprietary CVE report enter GitHub. Producer and recipient should be distinct people/accounts when possible.

Producer captures a bounded **data room index**, preferably with publicly auditable links:

| Record | Capture | Trust limit |
|---|---|---|
| Image | fully qualified OCI repo@sha256 digest pinned before scan | tag alone is not immutable |
| Scanner | binary/container digest, exact `trivy --version`, command, argument vector, config and policy/ignore hash | `--ignore-unfixed`, `--ignore-status`, `--severity`, ignorefile filters must not silently omit relevant findings |
| Scanner completion | actual CI process exit and logs, job identity and completion, report output path, scan start/end | `--exit-code 0` can mean findings exist, cannot prove zero vulnerabilities |
| Raw source | immutable raw Trivy JSON bytes, SHA256, report SchemaVersion, ArtifactName, RepoDigests, Results target list, expected scanner version | report hash proves equality of bytes only |
| Authentic producer provenance | GitHub Artifact Attestation/Sigstore/in-toto or independently authenticated CI assertion binding image + report + command digest + workflow SHA | an attestation can prove *who/which workflow*, not that scan coverage was complete |
| External recipient | independently transferred report/bundle, receiver-pinned expected digest and run log | verification is scoped to actual capabilities; no inferred source truth |

**Source collection requires permission and independent review; the shadow diagnostic itself does not authenticate logs or arguments.**

## First controlled challenge matrix

All cases must be classified as `ADMITTED_TO_PROPOSED_POLICY`, `WITHHELD_NOT_RUN`, or `NATIVE_ONLY_BASELINE` by *external* admission logic. None is a Kernel decision until actual canonical invocation.

| Case | Source fact | Expected admission / action |
|---|---|---|
| T01 | real Trivy finding, `Status=fixed`, installed version still affected | preserve raw status; never infer safe remediation; security gate must not silently allow |
| T02 | real severe finding with `Status=affected` | block candidate under explicit source-admitted severity/score policy |
| T03 | `FixedVersion` not provided | do not infer installed safe or require invented patch version |
| T04 | distro backport / vendor-specific advisory | native vendor precedence; **no lexicographic compare** |
| T05 | scanner reported no relevant findings | only after trusted completion, digest, scope and filter proof may clean report be considered |
| T06 | truncated or filtered scan, nonzero scanner exit | `WITHHELD_NOT_RUN` before Kernel, no invented receipt |
| T07 | swapped image digest, different report, wrong report `RepoDigests` | `WITHHELD_NOT_RUN` |
| T08 | missing/invalid severity/CVSS, duplicate keys, NaN, report encoding/schema mismatch | `WITHHELD_NOT_RUN`; preserve originals |
| T09 | high or critical finding mixed with medium/low and several advisory statuses | evaluate full report; no dropping unknown records or mis-ordering rules |
| T10 | complete clean-source report vs native Trivy-only release gate | measure false decisions, recipient comprehension and implementation cost |
| T11 | external recipient validates a PayGod bundle with independently pinned receipt | only if versioned Pack, admitted source, exact Kernel code and verifier available |
| T12 | policy uses CVSS score while native Trivy selects vendor severity | explicitly pin score source and tie-breaking; no automatic `Severity == CVSS*10` assumption |

## Prospective Pack v2 contract (design only, not code)

- Separate exact **raw** `trivy_status` and `source_severity` from explicitly derived `remediation_evidence_state` (which can be **unknown**).
- If a new Pack wants numeric thresholds, define a trusted **specific** CVSS source, an exact typed integer `cvss_score_x10`, its presence rules and vendor context. The shadow script currently uses **source severity only**, so its `SHADOW_BLOCK_CANDIDATE` is **not equivalent** to the existing numeric Pack's deny/flag thresholds.
- The external admission layer blocks execution if required source provenance/success/scope/fields are missing; absent remains `WITHHELD/NOT RUN`, not `false`.
- Any new source-integrated Pack must be versioned, with paired negative fixtures and a native-only comparator. Preserve the original Pack v1 receipts and original replay interpreter; do not rename the current `Status` as `fixed_verified`.
- If typed-v1 DSL semantics from draft [#115](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/115) are approved, explicitly opt into them in the *new* Pack; never make assumptions about #115 being merged. A source/admission fix is needed independently from typed comparison hardening.

## Go/no-go for Issue #116

**P0 RED:** evidence of the false allow is already obtained, bounded and source-pinned.  
**P1 SHADOW:** no-authority parser and adversarial CI green in PR #118, synthetic only.  
**P2 REAL SOURCE:** **NOT OBTAINED**; no authenticated scan + subject + completion fixture yet.  
**P3 NATIVE COMPARISON:** **NOT RUN**; Trivy-only plus genuine CI attestation baseline pending.  
**P4 VERSIONED PACK / ADR:** **NOT ACCEPTED / NOT MERGED**.  
**P5 INDEPENDENT RECIPIENT:** **NOT OBTAINED**.

Issue #116 must remain **OPEN** until actual P2–P4 acceptance tests pass and the owner reviews any material Pack/Kernel change. P5 is additionally mandatory for an **external adoption / B2-REAL** claim but must not globally block other technical research tracks. No external production release, payment or industrial action is authorized here.

## Ownership boundaries

- Trivy owns native findings/status, GitHub/Sigstore owns attestation issuer mechanics.
- **EIK** checks source admission, never rewrites facts into approved decisions.
- Only the **canonical Kernel** creates PayGod decision and receipt identity under an approved Pack.
- The **independent Verifier** checks declared integrity/authenticity dimensions only; it does not claim vendor package vulnerability truth or authorized execution.
- Website/Observatory are explanation and research surfaces; neither is a regulatory certification registry.
