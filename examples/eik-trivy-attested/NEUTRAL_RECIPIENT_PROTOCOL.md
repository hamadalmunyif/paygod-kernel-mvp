# Neutral relying-party comparison — E-004 / B2-REAL candidate, NOT RUN

**Status: PROPOSED / NO EXTERNAL RECIPIENT / NO BUYER MEASUREMENT.** This public protocol describes how a *separate, consenting* developer, security auditor or recipient could test the current research chain fairly. It **does not** authorize a release, ask for credentials, represent an appointment or claim that anyone outside the project has agreed.

## What question would falsify PayGod's incremental value?

When a relying party receives a signed Trivy scan of a pinned artifact, does the **additional** PayGod canonical policy/decision/receipt chain allow them to reconstruct a *specific policy's disposition* more accurately, with fewer steps or ambiguities, than native Trivy + GitHub Artifact Attestations alone?

Answer `NATIVE_SUFFICIENT` if native controls give the recipient everything needed. **Do not** treat an additional checksum, signed artifact or already-native denial as PayGod innovation.

## Pre-registration and eligibility

Before running, record without identifying/sensitive details:
- An independent reviewer has consented; publisher and reviewer are different people/organizations, with no use of publisher's workspace, secrets or privileged GitHub token.
- The agreed task is only reviewing a **public synthetic/test image** and **non-permitting security example**. No actual regulated release, customer vulnerability report, scanning of third-party private assets or production action.
- The reviewer sees each solution's documented capabilities and limits, receives a **separately authenticated** expected receipt hash **if and only if one truly exists**, and can refuse to proceed. Producer-supplied CI job output is **not** an independent receipt pin.
- The full native artifact, instructions and input must be retrievable at the agreed date; short-lived GitHub artifacts may expire. Where unavailable, mark `INCONCLUSIVE / ARTIFACT_EXPIRED`, not success.
- Log the exact immutable image digest, scanner/execution statement, two native GH attestations, Kernel Pack/version/commit, verifier binary/script digest and two workflow run IDs.

## Neutral A/B comparison, same evidence source

| Arm | Inputs given to reviewer | Expected bounded capability |
| --- | --- | --- |
| **A — Native control** | Pinned public OCI image reference; full actual Trivy report; native Trivy high/critical gate result; GH attestation(s) for report and workflow execution statement | Verify authentic origin/bytes *of signed reports*, report subject, native severity block, command-record identity where attested |
| **B — Native plus PayGod** | **All Arm A evidence** plus admitted normalized source input, version-pinned research Pack, Kernel `deny` receipt/evidence, and portable verifier | Independently verify **integrity and policy-specific binding** from the same report/execution statement through input hashes to canonical `deny` receipt; identify remaining issuer/replay/time gaps |

Method: randomize A/B order if possible; present each arm's instructions without claims that one is preferable. Reviewer may inspect both systems and issue `NATIVE_SUFFICIENT` even if B is technically valid.

## Controlled questions (answers recorded verbatim)

1. Which exact immutable artifact was inspected and what was Trivy's observed severity outcome?
2. Does `Trivy Status=fixed` prove an installed package is remediated? **Expected: no**; it normally denotes vendor/advisory fix availability.
3. Which files are signed by GitHub and which provenance identity/ref/commit was verified? Does that prove scan *completeness*? **Expected: no**.
4. Which party issued the PayGod `deny` receipt? Does `valid` prove its issuer authenticity or legal release authority? **Expected: no**.
5. Can a modified report, execution statement, normalized input or canonical bundle be detected, and by which native/PayGod control? Record actual error labels and whether the reviewer could reproduce.
6. Did the additional PayGod receipt make a **specific authorized policy's** decision easier to reconstruct, or merely add processing around Trivy's existing native block?
7. Would the recipient use this output in a real approval/audit flow, and under which currently unavailable identity/authority controls? Record this separately from technical PASS.

## Required negatives and minimum record

- Change only one byte of the signed report; test GH-native attestation failure.
- Swap workflow identity or signer source revision; test native GH verify refusal.
- Change the observed scanner command, scanner binary SHA or claimed exit; test execution statement binding failure.
- Substitute another signed statement not matching the report; test `report_sha256` consistency.
- Change raw report or execution SHA in normalized input and try recipient-side binding; both must fail.
- Alter a canonical evidence member or use a wrong expected receipt digest; portable verification must fail **if independent receipt pin is in fact trusted**.
- **Coherent full bundle rewrite without an independent pin**: do not count cryptographic proof of original issuer authority merely because a new internally self-consistent bundle validates.

For each arm record **elapsed recipient minutes, number of required tools/commands, independently completed checks, false-acceptances under negatives, error explanations and reviewer trust-scope answers**. Zero observed errors is not proof of a general zero-error rate. Missing data is `UNKNOWN`, not zero.

## Predeclared outcome rubric

- `PASS_INCREMENTAL`: recipient demonstrates a policy-authorized question that Arm B answers better than A, with independently inspectable sources and measured meaningful delta, and no misleading trust claim.
- `NATIVE_SUFFICIENT`: Trivy/GitHub already answers the actual reliance question at equal or lower cost.
- `FAIL_UNSAFE`: missing/forged source or modified artifact is accepted, or any route invents an authoritative release permission.
- `INCONCLUSIVE`: reviewer/permission/independent pins/evidence expired or measurements insufficient.

A successful first-party GitHub Actions no-checkout Windows job **cannot** be recorded as an independent outside recipient. The objective remains open in [Issue #114](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/114) and the wider [Issue #116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116).

## Current public technical comparators, as of 2026-10-16

- Native Trivy-only severity gate: [run 38923531022](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38923531022) (**observed blocking without PayGod**).
- GH-native attested-report receiver: [run 38925014644](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38925014644) (**observed signature verification without PayGod**).
- Combined first-party research chain: [PR #121](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/121) and its exact-commit checks. This is **not** an outside recipient or source-completeness attestation.

No real customer identity, purchase interest, economic value or approved production workflow may be inferred from this protocol's existence.
