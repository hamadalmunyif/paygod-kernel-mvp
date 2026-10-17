# EIK Trivy native real-source witness, 2026-10-16 — PUBLIC TEST IMAGE, NOT A RELEASE GATE

**Status: OBSERVED_NATIVE_SCAN + NATIVE_SUFFICIENT_FOR_SEVERITY_BLOCK / INDEPENDENT RECIPIENT NOT OBTAINED / KERNEL NOT CALLED.**  
This source record is on **research PR #118**, not on Kernel `main`, and must not be conflated with a frozen B2/Pass A witness. Do not claim a bank/industrial customer, approved deployment, signature-authenticated scan, or that an end-to-end PayGod EIK production admission gate is accepted.

## Reproducible public-source observation (source-pinned)

| Field | Witness |
|---|---|
| GitHub Actions successful run | [`38923270994`](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923270994), source workflow SHA `4266ed554a2894fe0441c817261f7040fc454408` |
| Native Trivy version | `0.75.0`, installed through SHA-pinned `aquasecurity/setup-trivy@e07451d2e059ed86c2870430ea286b3a9e0bf241` |
| Public image | `alpine@sha256:ce64758a109eb420d874a118f87920e625e12d3634e03b4a5573fd9f6e5d3507`, resolved from public `docker.io/library/alpine:3.21` to a pinned immutable repository digest before scanning |
| First raw source command | `trivy image --scanners vuln --format json --exit-code 0 --output native-source/trivy.json "$subject"` |
| Raw report bytes SHA-256 | `d4ff48b0103219fd1d3b429f50fe9c0008e44111bdabddb8ffe97cae240c60c4` |
| Original artifact | [Run #38923270994 artifact #12055018039](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923270994/artifacts/12055018039), subject/command/workflow/version/raw report/shadow; short artifact retention, do not silently assume permanent access |
| Read-only shadow result | `SHADOW_BLOCK_CANDIDATE`, `REPORTED_HIGH_OR_CRITICAL`, `source_attested=false`, `kernel_called=false`, `receipt_issued=false` |

All 21 findings in this **dated public image scan** reported `Trivy Status=fixed`: **2 HIGH, 17 MEDIUM, 2 LOW**. HIGH findings included package `libcrypto3` and `libssl3` with `InstalledVersion=3.3.7-r1` and advisory `FixedVersion=3.3.7-r2`, both for the scanner-reported `CVE-2026-84782`. This is a dated scanner observation; source fixes and vulnerability databases can change. No asserted 9.0+ CVSS from the raw severity field.

### Native-only counterfactual — do not oversell PayGod

Second successful Actions run [`38923531022`](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923531022), source SHA `5955d9edb5e2b3315b3bab76b8fc441cc686dfdb`, same immutable image digest and Trivy version, ran a separate native command:
`trivy image --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --format json --output native-source/native-high-critical-gate.json "$subject"`.

This **native Trivy-only gate returned exit code 1**, as expected for **2 HIGH** findings. The separate all-severity source report in the second run has SHA-256 `77a78b81bc52ea1d779e52cc2454c9b5647055590e66228f7f7b96e7b0386299` (independent scanner runs can yield differing JSON bytes even on the same image). The read-only shadow returned `SHADOW_BLOCK_CANDIDATE` and 2 high/critical; it **did not add a unique severity-block capability**. [Run #38923531022 artifact #12055517684](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923531022/artifacts/12055517684) includes both reports, native exit and raw metadata.

**Classification:** `NATIVE_SUFFICIENT_FOR_SEVERITY_BLOCK`, not `NATIVE_SUFFICIENT_FOR_ALL_EVIDENCE_OR_INDEPENDENT_AUDIT`. A GitHub workflow success + report hash establishes a reproducible observation in our public CI run; it is **not an independent authenticated producer attestation** or external customer adoption.

## Native GitHub/Sigstore provenance test (third dated run — not an independent organization)

A third real native scan at [GitHub Actions run #38924288024](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38924288024), workflow SHA `f6327b69c30cdb2545e03fa054a17393429026e4`, used the same pinned public Alpine subject with **Trivy v0.75.0**. Scanner returned **21** reported vulnerability findings, **2 HIGH**, all advisory `Status=fixed`. Native `--severity HIGH,CRITICAL --exit-code 1` blocked, while the research shadow classified `SHADOW_BLOCK_CANDIDATE`; both native commands and shadow steps completed successfully. The new raw report SHA-256 was `e5ed929984636ad1387a0de39646748e496082d622be9c84ad8aae6b0986455d`; the differing per-run raw hash is not assumed to mean image content changed.

This time the workflow also used SHA-pinned [`actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6`](https://github.com/actions/attest/commit/1e69f48acb82d1966a394da916b4c1698aa569d6) **v4.2.2** with scoped `id-token:write`, `attestations:write`, `artifact-metadata:write` permissions. It produced [GitHub Artifact Attestation #56711445](https://github.com/hamadalmunyif/paygod-kernel-mvp/attestations/56711445) for exact `trivy.json@sha256:e5ed929984636ad1387a0de39646748e496082d622be9c84ad8aae6b0986455d`; the signed SLSA provenance was issued via public-good Sigstore and uploaded to Rekor. The workflow successfully executed `gh attestation verify native-source/trivy.json --repo "$GITHUB_REPOSITORY" --format json`, checking an actual native signature for the bytes, not merely matching a SHA in the same ZIP.

[Run artifact #12055563610](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38924288024/artifacts/12055563610) contains saved report, scanner/native gates and GitHub CLI verification result. The attestation is retrievable independently through GitHub's attestation registry even when short-retention ZIP artifacts later expire.

**Bounded trust claim:** native GitHub/Sigstore provenance signature **obtained and verified** for *a report created by our own workflow*. It binds an exact file digest to the signed issuer/workflow provenance. It **does not** mean we proved anti-filter completeness, report content truth, CVE applicability outside this specific scan, private customer origin, a nondeveloper external recipient, an actual PayGod decision/receipt, or PayGod's differential security value. The shadow script still reports `source_attested=false` because **it does not consume/verify GitHub attestations**; the native attestation and shadow diagnostic must not be silently combined into a new trust verdict.

## Fresh no-checkout Windows recipient (native GitHub baseline, not external human)

[Full passing run #38925014644](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38925014644) at exact research workflow SHA `e3572d8c002f5f4eecd0c6edab2764b49ca8cf99` now has **two separate green jobs**:

1. Linux producer: genuine pinned public Alpine image scan with Trivy v0.75.0, 21 reported vulnerabilities (2 HIGH), a Trivy-native HIGH/CRITICAL gate that exits **1**, conservative EIK shadow `SHADOW_BLOCK_CANDIDATE`, GitHub/Sigstore signed report SHA `fb79a1f5e2a17a2030b30598bad2cbc2d9f2ee965de3cec14a0b51e0548bcbb0` at [GitHub attestation #56713074](https://github.com/hamadalmunyif/paygod-kernel-mvp/attestations/56713074). [Source artifact #12055399362](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38925014644/artifacts/12055399362).
2. Separate **Windows 2022** runner: no repository checkout, downloads the transferred artifact, uses `gh attestation verify` with GitHub's own trust-root handling, asserts shadow did **not** call Kernel or mint a receipt, mutates the report content, confirms native signature verification rejects tampering. The first Windows run #38924857262 observed the two successful assertions but was marked CI failure because PowerShell retained an intentional negative probe's exit code; the reviewed workflow explicitly exits 0 **only after** assertions pass, and run #38925014644 confirms green.

**Critical limits:** this is a *technical receiver in a different runner OS, still within our same repository owner and GitHub workflow*, not an unrelated organization/human and **not** B2-REAL or an approved PayGod independent receiver. Importantly this validates **GitHub native independent report verification without PayGod**. PayGod EIK did not sign or verify the attestation; it only emitted a shadow diagnostic. Receiver's checksum/trust anchors are native GitHub/Sigstore and should not be relabeled as PayGod authority. No Pack v2 / canonical Kernel decision or proof of real-world effect was generated.

## Why #116 is still open

This observable raw Trivy report proves that at least one genuine scan can retain `Status=fixed` for a still-reported vulnerability with a strictly older **displayed** installed version. Combined with the [synthetic RED policy counterexample #117](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/117), it strongly motivates correcting source semantics. But the old `critical-cve-blocker` v1 uses a **numeric CVSS x10 policy**, whereas this shadow and native comparison use **vendor severity HIGH/CRITICAL**. Do not silently equate them or claim a real runtime PayGod `allow` result for this scan.

Still NOT demonstrated: independently authenticated scan producer/completeness/scope, external application with permissioned real report, a versioned source-admitted Pack v2 passing canonical decision/receipt tests, standalone external recipient comparison, and relative economic value. Any corrected Pack requires its own PR, exact-source fixtures, ADR if materially changing trust semantics, owner review, and appropriate release gate.

## Next falsifiable tests

1. Extract source-specific numeric scoring policy provenance (if required) and verify distribution-specific backports; never lexicographically compare versions or infer `Status=fixed` equals installed remediated.
2. Create an external admission contract that verifies original command/status/subject and complete scanned scope under an independently trusted workflow/attestation. `--exit-code 0` on the unfiltered report **cannot** prove no vulnerabilities.
3. Version a new Pack and compare its actual Kernel decision + receipt + independent verifier against Trivy-native exit/status and native provenance; no Pack upgrades automatically.
4. Obtain a second independent recipient without developer workspace access; measure whether PayGod improves transfer/understanding over the native signed report. If it does not, do not overbuild.

Evidence classification: **a public-source native scan + conservative synthetic shadow**. Do not upgrade B2-REAL eligibility, partner adoption, external release authorization, or source authenticity from this internal CI experiment.
