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

## Native public-image witness achieved, without independent producer validation

On 2026-10-16 our branch executed genuine `Trivy v0.75.0` against public Alpine image SHA `ce64758a...6e5d3507` at [successful run #38923270994](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923270994), and repeated the same target with a separate native HIGH/CRITICAL exit gate at [successful run #38923531022](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923531022). See the exact [source and native-only comparison record](REAL_NATIVE_PUBLIC_IMAGE_WITNESS_2026-10-16.md).

This moves one **narrow** item to `P2A OBSERVED_NAMED_PUBLIC_NATIVE_SCAN`: 21 vulnerability findings, 2 HIGH, all advisory `Status=fixed`, and Trivy-native exit **1** on HIGH/CRITICAL. The shadow diagnostic agreed on 2 HIGH but issued **no PayGod verdict**. A GitHub Actions report and local hash are not proof of independent external producer authenticity, user/partner permission, complete anti-filter attestation, fixed binary state, or independent receiver. `P2B AUTHENTICATED_EXTERNAL_SOURCE` remains **NOT OBTAINED**. `P3 NATIVE_ONLY_BLOCK_COMPARISON` is **OBSERVED**, but a broader native signed-attestation-vs-PayGod evidence comparison remains **NOT RUN**.

## P2A signed GitHub report provenance — native tool capability confirmed

[Third native source run #38924288024](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38924288024) produced [GitHub Artifact Attestation #56711445](https://github.com/hamadalmunyif/paygod-kernel-mvp/attestations/56711445) for raw Trivy report SHA `e5ed929984636ad1387a0de39646748e496082d622be9c84ad8aae6b0986455d`, signed through Sigstore/Rekor and successfully verified by `gh attestation verify` in the same workflow. Exact evidence, issuer and source limitations: [real source witness](REAL_NATIVE_PUBLIC_IMAGE_WITNESS_2026-10-16.md).

This independently verifies the **native GitHub signature** using GitHub CLI but remains a scan by **our own** CI, not an outside human/tenant or consented partner. It is **not proof of a fully unfiltered scan**, and the current EIK parser does not verify this attestation, so its output retains `source_attested=false`. GitHub's native attestation is now an explicit **existing competing control**: PayGod must prove a differential need before attempting to reproduce such provenance machinery.

## Go/no-go for Issue #116

**P0 RED:** evidence of the false allow is already obtained, bounded and source-pinned.  
**P1 SHADOW:** no-authority parser and adversarial CI green in PR #118, synthetic only.  
**P2 REAL SOURCE:** public native scan in our CI **OBSERVED**, report provenance **NATIVELY ATTESTED AND SIGNATURE VERIFIED** by GitHub/Sigstore at dated exact run; independent outside producer/receiver and scan-completeness proof **NOT OBTAINED**.  
**P3 NATIVE COMPARISON:** native Trivy severity-only blocking **OBSERVED** and sufficient for this gate; genuine cross-organization signed attestation and independent-receiver baseline **NOT RUN**.  
**P4 VERSIONED PACK / ADR:** **NOT ACCEPTED / NOT MERGED**.  
**P5 INDEPENDENT RECIPIENT:** **NOT OBTAINED**.

Issue #116 must remain **OPEN** until actual P2–P4 acceptance tests pass and the owner reviews any material Pack/Kernel change. P5 is additionally mandatory for an **external adoption / B2-REAL** claim but must not globally block other technical research tracks. No external production release, payment or industrial action is authorized here.

## Ownership boundaries

- Trivy owns native findings/status, GitHub/Sigstore owns attestation issuer mechanics.
- **EIK** checks source admission, never rewrites facts into approved decisions.
- Only the **canonical Kernel** creates PayGod decision and receipt identity under an approved Pack.
- The **independent Verifier** checks declared integrity/authenticity dimensions only; it does not claim vendor package vulnerability truth or authorized execution.
- Website/Observatory are explanation and research surfaces; neither is a regulatory certification registry.
