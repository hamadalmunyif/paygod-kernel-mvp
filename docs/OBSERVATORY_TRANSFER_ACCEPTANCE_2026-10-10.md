# Observatory → Canonical Kernel: Evidence Transfer Register

Status: **DOCUMENTATION / ACCEPTANCE REVIEW — 2026-10-10**  
Kernel reference: `hamadalmunyif/paygod-kernel-mvp@23ea2cca74ef8b698718c6d0c8dbda447f13bb37`  
Experimental source: `hamadalmunyif/paygod-workflow-observatory@dea10136bbb79a155237bc1252aaf41d3961ca46`

This document explains what the canonical Kernel **already accepts and verifies**, what its tests have **actually witnessed**, and what experimental Observatory results **must not** be silently promoted into the Kernel or public site.

It is an evidence and documentation record, **not** an ADR approving a new primitive, proof of an external institution's acceptance, or approval to change frozen Kernel semantics. The current [Stop-Build Rule](STOP_BUILD_RULE.md) remains ACTIVE.

## Two responsibilities

- **Canonical Kernel:** owns policy-decision and canonical artifact semantics. It emits decision, receipt, manifest and bundle identity through the one registered canonical path; adapters delegate; independent verifiers check what the transferred evidence supports.
- **Observatory:** tests outside-world observations, origin classifications, failure modes, decision-to-authority bindings and closed-harness release/conformance. A test harness is **not** a second canonical Kernel and does **not** grant downstream financial or institutional authority.

This is not an assumption that all research must eventually become a Kernel feature. A valid experiment may result in **no code change**.

## Promotion classes (not security verdicts)

| Class | Definition | May be described as delivered Kernel capability? |
|---|---|---|
| **KERNEL_ACCEPTED** | Present in canonical Kernel code/contracts and covered by Kernel-owned verification or CI evidence. | Yes, only within the named witness scope. |
| **BOUNDARY_ACCEPTED** | A documented restriction/acceptance rule that preserves Kernel semantics; includes admission outside the Kernel. | Describe the boundary accurately; do not imply a new Kernel runtime primitive. |
| **OBSERVED_COMPATIBILITY** | External observation or shadow workflow successfully consumed the existing Kernel; its authoritativeness and economics remain unproven. | No; cite only as a scoped research witness. |
| **HARNESS_ONLY** | Runtime behavior demonstrated inside Observatory's frozen local controlled harness. | No production feature or external portability claim. |
| **UNRESOLVED** | Design, proposed policy/profile, comparison, independent review or financial hypothesis awaiting proof. | No. |

The labels `SOURCE_PROVEN`, `DOC_CLAIMED`, `RUNTIME_OBSERVED`, `UNKNOWN` describe **where a claim came from**, not whether a future feature was adopted. The frozen T0 attack labels are a **different** vocabulary: `REJECTED_AS_EXPECTED`, `BYPASS_OBSERVED`, `NOT_TESTABLE_UNDER_T0`, `HARNESS_DEFECT`.

## Transfer-by-evidence matrix

| Topic | Experimental observation / reference | What the canonical Kernel already establishes | Class / decision |
|---|---|---|---|
| Deterministic decision authority | Observatory's shadow path invokes the pinned canonical CLI rather than inventing a verdict. | [README](../README.md), [Repository Boundary Closure](REPOSITORY_BOUNDARY.md), CI mutation witness on registered adapters. | **KERNEL_ACCEPTED**; no second decision path. |
| Versioned canonicalization and decimal rejection | [Witness 001 result](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/dea10136bbb79a155237bc1252aaf41d3961ca46/docs/WITNESS_001_RESULT.md): full live ACP descriptor containing a fractional number was rejected before policy evaluation. | [Canonical tests](../tests/PayGod.Tests/CanonicalizerTests.cs), [standalone verifier](STANDALONE_VERIFIER.md), `paygod-c14n-v1`: no fractional/exponent JSON numbers or unsafe integers. | **KERNEL_ACCEPTED** rejection. **BOUNDARY_ACCEPTED** need for external representation. Not a Kernel defect. |
| External read → byte-preserving normalization → manifest | [Observation Pack v0](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/dea10136bbb79a155237bc1252aaf41d3961ca46/docs/OBSERVATION_PACK.md): local captured bytes, derived normalized data and SHA-256 manifest. | Kernel can receive an admitted compatible decision input and produce its *own* canonical artifacts; it does not claim the source observation itself was authentic. | **OBSERVED_COMPATIBILITY**; do not call generic raw-observation ingestion a shipped Kernel service. |
| No silent evidence coercion | Observatory's `WITHHELD_NO_PAYLOAD` shadow case and simulated gas P0. | [ADR 0003](../adrs/0003-evidence-admission-before-decision-execution.md): `TRUE | FALSE | WITHHELD` **before** the Kernel; mandatory `WITHHELD` yields orchestration `NOT RUN`, not Kernel verdict `FALSE`. | **BOUNDARY_ACCEPTED** and already in the reference repo; no tri-state Kernel extension. |
| Trust dimensions and independently pinned bytes | Experimental challenges include cross-object substitution and issuer trust-root attack probes. | [Standalone Verifier](STANDALONE_VERIFIER.md), [Issuer Authenticity](ISSUER_AUTHENTICITY.md), [Internal Verification Challenge](INTERNAL_VERIFICATION_CHALLENGE.md): hash, binding, ledger and optional Ed25519 signature; externally pinned receipt can detect coherent rewrite. | **KERNEL_ACCEPTED** for covered verification dimensions, **not** external fact truth or issuer mandate. |
| Controlled conditional release and state progression | [T0 Closure](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/dea10136bbb79a155237bc1252aaf41d3961ca46/docs/CONTROLLED_HARNESS_T0_CLOSURE_V0.md): 98/98 tests, 13/13 declared E1 Gate Zero attempts rejected, 23 postflight checks, two-surface local-EVM sequence. | Kernel supplies pinned canonical decision and authenticated artifacts to the harness. Kernel README **does not** claim E1, E2, S0 or Warrant as a public Kernel execution rail. | **HARNESS_ONLY**; no import into Kernel and no live enforcement claim. |
| No silent upgrade across decisions / trust domains | Observatory labels `RAW_REMOTE / SDK_DERIVED / LOCAL_DERIVED / UNKNOWN`; T0 blocks signer/trust-set substitution. | Kernel limits producer/adapters/verifier authority, and `WITHHELD` admission guards semantic coercion. | **BOUNDARY ACCEPTED AS DOCUMENTED PRINCIPLE**, **not** a generic executable invariant tested for every system. |
| AP2 collision and Warrant originality | [Pass B handoff](https://github.com/hamadalmunyif/paygod-workflow-observatory/blob/dea10136bbb79a155237bc1252aaf41d3961ca46/docs/AP2_COLLISION_PASS_B_HANDOFF_V0.md): blind comparison prescribed, result not established in this record. | No canonical Kernel claim of independent Warrant originality. | **UNRESOLVED**. |
| Real institutional acceptance, demand, price | B2-REAL and external enforcement not closed. | [B2 readiness](../rehearsals/gas-site-readiness/b2/READINESS_REPORT.md): `0/10` real/deidentified qualifying cases and `0/5` independent non-developer recipient witnesses. | **UNRESOLVED**. |

## An engineering lesson admitted now: canonical input vs. external evidence

Witness 001 is evidence for **an admission-layer separation**, not a request to relax `paygod-c14n-v1`.

```text
External observation (possibly fractional, untrusted)
    | keep exactly captured bytes + source class + digest
    v
Raw evidence record (outside canonical Kernel decision input)
    | explicit metric/meaning representability and provenance review
    v
Admitted, bounded canonical input (safe integers, strings, schema)
    | only after mandatory facts are admitted
    v
Canonical Kernel decision (or orchestration NOT RUN before Kernel)
    |
    v
Kernel-owned receipt / manifest / ledger / portable bundle
```

The recorded acquisition boundary in Witness 001 preserves the **captured CLI output bytes**. It does *not* establish byte identity with raw HTTP wire data. SHA-256 of the captured output is not source authentication.

For future decimal-heavy sources (temperature, mass, emissions factors, etc.), a proposed **domain admission profile** could represent a value as a versioned safe integer plus declared unit/scale/precision, retain original source bytes, define rounding or reject it, and bind the transformation. **No such general profile is implemented or approved by this transfer register.** Until a contract exists and its tests pass, required unrepresentable measurements remain `WITHHELD`.

## Trust claims that must remain separate

| Established in a scope | Not established merely by it |
|---|---|
| Numeric calculation / policy decision | Truth of the external measurement |
| Matching file digest and ledger chain | Unchanged historical issuance without an external anchor |
| Valid Ed25519 receipt signature under recipient's supplied key | Organization/regulator authorization of the signer |
| Canonical Kernel `ALLOW` | Permission to execute on an external financial or agent rail |
| T0 local enforcement observation | Universal bypass resistance or independent production enforcement |
| Verifier A accepting an artifact | Verifier B being obligated to accept it |

These separations are recurring design controls, not claims that PayGod invented PKI or portable attestations.

## Research-promotion procedure

1. **Observe:** name frozen source version, actual runtime event, exact bytes/inputs and witness.
2. **Classify:** confirm whether result is a Kernel defect, contract/admission mismatch, provenance limitation, harness defect, or integration question.
3. **Reproduce in the correct owner:** Kernel CI for canonical Kernel semantics; Observatory tests for experimental external behavior. Do not forge a passing Kernel test for an unimplemented enforcer.
4. **Check compatibility:** try existing contracts, packs, admission and delegated adapters without broadening Kernel authority or changing `paygod-c14n-v1`.
5. **Decide whether adoption is justified:** retain the active stop-build until relevant external evidence, recurrence/importance, an explicit ADR and agreed review permit changes.
6. **Document:** if implemented, identify exact Kernel code, negative tests, CI runs and versions; if not implemented, mark `HARNESS_ONLY` or `UNRESOLVED`.
7. **Publish:** `paygod.net` should link only to canonical Kernel documentation and reflect the same class, never silently turning a research result into a shipped product.

### Rejected automatic promotions

- Copy `warrant-v0`, `e1-transaction-gate`, `e2-provider-release`, `authority-state` into the Kernel merely because T0 closed.
- Claim a general-purpose ACP, AP2, x402, bank or PSP adapter because the Observatory performed a signerless read or local EVM transaction.
- Convert `WITHHELD` into `FALSE` to force a verdict; treat `NOT RUN` as a Kernel verdict.
- Treat `SOURCE_PROVEN` or `RUNTIME_OBSERVED` as a guarantee of real-world validity or regulatory approval.
- Use public website copy or legacy architecture documents as stronger authority than current Kernel README, tests and explicit witness limits.

## Public-communication boundary

The **only current canonical implementation repository to present as the PayGod public technical asset** is `hamadalmunyif/paygod-kernel-mvp`. Research source references above exist for internal provenance, documentation audit and possible independent review; they do not change the public website's repository-navigation rule.

This page and the public website must be reviewed again if the Kernel's README, frozen versioned contracts, supported verification checks or test results materially change.
