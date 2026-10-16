# Signed Trivy report → admitted source → canonical Kernel deny → no-checkout receiver

**Status: WITNESSED RESEARCH / STACKED ON DRAFT #118 / NOT MERGED / NO ALLOW PATH / NOT A RELEASE GATE.**  
First complete workflow: [GitHub Actions run #38928986734](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38928986734), commit `56287d015fefe626e08e77c3f693c243f78947e8`. Two jobs completed successfully after correcting workflow YAML syntax. No additional source authenticity, regulatory authority, trusted time, policy permission or external organizational adoption is inferred.

## Reproducible witnessed result

| Claim within scope | Evidence |
| --- | --- |
| Genuine Trivy v0.75.0 report for immutable **public** Alpine image | Linux job, public `alpine@sha256:ce64758a109eb420d874a118f87920e625e12d3634e03b4a5573fd9f6e5d3507` |
| Raw report bytes | SHA-256 `a50435b4505d8ad0c5f58b889bc75aa1627211fc2c164ecb7b1da8b2682bb092`, **21** findings (2 HIGH). Report/normalized input transferred separately from canonical Kernel evidence |
| Genuine GH-native report attestation | `actions/attest` signed exact raw Trivy bytes; bridge calls **`gh attestation verify`**, not a caller-supplied `source_attested=true` |
| Bounded source/structure gate | Existing read-only `eik_trivy_shadow.examine` requires digest-shaped subject, report/result consistency and severe source observation; `tools/eik_admit.py` checks opted-in Pack schema. Unqualified/clean/invalid reports are **WITHHELD_NOT_RUN**, not `allow` |
| Only canonical Kernel minted PayGod artifacts | `examples/eik-trivy-attested/bridge.py` invokes `./out/PayGod.Cli run` using a *separate research Pack v2*; actual receipt verdict **`deny`**, digest `584431b08a4be8bf8426d9ab2ea9714eeac02c444bfbc72042a2d8619e7607c9` |
| Portable recipient checks | Fresh Windows runner with **no repository checkout** separately verifies GH-signed report, independently invokes PayGod Python verifier with transferred receipt pin, and recomputes raw-source SHA → exact normalized findings → canonical input hash → Kernel Receipt input hash |
| Negative mutation | Altered signed raw report is rejected by GH prior to Kernel with **no output directory**; recipient rejects altered raw report, tampered PayGod findings.json, and changed source/receipt binding |
| Scoped verdict and trust | Receiver verifier returns `status=valid`, `integrity=verified`, **`issuer_authenticity=not_verified`**, `replay=not_performed`, `time_authority=producer_supplied`. This does not create a separate issuer signature over the PayGod receipt |

Source-transfer artifact [#12058351592](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38928986734/artifacts/12058351592) and receiver-code artifact [#12058311515](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38928986734/artifacts/12058311515) have **seven-day retention**. Exact transcript of run is linked above; availability after TTL is not guaranteed.

## Architecture and major limitations

- The actual Trivy source is signed using **GitHub's preexisting native attestation**, which already provides cryptographic file provenance verification. The PayGod adapter is NOT the signer and the raw report's own signature does not prove command/flags/scan scope, threat database source truth, full scan completeness, vendor backports, or an original customer source. Runner metadata and `scanner_exit_code=0` are scoped assertions observed from our own workflow, **not independent attestation of full tool execution**.
- The CLI-generated PayGod Receipt binds canonical **admitted input** via input hash, and the normalized input explicitly includes SHA-256(raw Trivy report). The **source raw file and GH attestation are external sidecars**, *not* manifest members in the canonical PayGod bundle. The receipt does not independently prove the raw source's origin or an organizational policy authority; an outsider must reperform GH verification and explicit binding checks.
- The Pack (`pack/pack.yaml`) is a **research-only `v2.0.0` severity rule**, not a rewrite of the old numeric CVSS ×10 `critical-cve-blocker` v1. HIGH/CRITICAL → `deny`, MEDIUM → `flag`, no `allow` rule. Even the `deny` here is a **policy observation**, **not** an enforceable deployment authorization. For clean/untrusted scans the bridge does not call the Kernel, so the research test cannot be used for permitting releases.
- Receiver's expected PayGod receipt SHA comes from **same workflow producer job output**: this is **producer-supplied**, NOT an independently authenticated out-of-band receipt pin. GitHub native report signature is independently verifiable using GitHub's trust roots; **PayGod issuer authenticity is not proven** in this example. Source and verifier code are generated/handed off by our project; a relying third party must vet this code independently.
- Two runners on different OS within our own repository are a **separated technical receiver**, not an unrelated third-party human review or a B2-REAL qualified recipient. No external buyer, regulator or upstream maintainer approved this experiment.
- Native Trivy `--severity HIGH,CRITICAL --exit-code 1` was already sufficient to block this same image, and GitHub's report attestation was already sufficient to check file provenance and tampering. Thus neither blocking nor signing is PayGod's unique value. Additional value in a *portable institutional decision* remains a hypothesis, not a result proven by the workflow.

## How to inspect

1. Open the [successful workflow](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38928986734) and view both Linux and Windows jobs.
2. Inspect `.github/workflows/trivy-attested-canonical-chain.yml`, `bridge.py`, `receiver_binding.py` and `pack/pack.yaml` at the exact source SHA.
3. Check both artifacts (if still retained); compare raw report hash to `source/input.json.scan_report.source_sha256` and receipt `input.canonical_hash` using the bundled binding script.
4. Verify `evidence/receipt.json` from the actual Kernel and separately run portable verifier. `valid` refers to scoped integrity; inspect each listed nonclaim.
5. Compare with the [native-only Trivy severity block](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923531022) and [native-only GitHub signed report handoff](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38925014644) without PayGod.

## Remaining acceptance gates before any promotion

1. **Independent source execution/command/completeness attestation:** bind signer/identity, scanner version/config, immutable image digest, exact filter scope, native exit and scanner output **without trusting current producer-supplied claims**. Handle stale advisories and distinct CVSS scoring policies.
2. **Decision authority binding:** who authorized the Pack and the signer's trust roots, independent endorsed receipt pin, policy scope and legal/operational reliance. An integrity-valid Kernel receipt is not an approved enterprise release.
3. **Trusted external recipient:** entirely separate organization/human using publicly inspectable pinned verifier binaries and native controls, no checkout and no project-owner guidance.
4. **Native-only counterfactual:** score external receiver comprehension/time/error and additional controls compared with Trivy-native + GitHub Attestations alone. Accept `NATIVE_SUFFICIENT` if equivalent.
5. **Governance:** owner reviews [Trivy Issue #116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116), optional typed-policy proposal [PR #115](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/115), original RED [#117](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/117), Trivy research [#118](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/118) and independent severity prototype [#119](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/119). Only a reviewed versioned implementation may be promoted beyond research; preserve frozen source records.

**No single successful workflow is evidence of PayGod market fit, regulator endorsement, real funds/deployment effects or completeness of security scanning.**
