# Paygod Kernel MVP

Paygod Kernel is a deterministic policy-execution core built on **contracts-first + evidence-first** principles.

It produces schema-governed decision evidence that can be transferred and independently verified without replaying the original decision.

## What is proven

The repository currently has CI witnesses for:
- bit-for-bit deterministic execution;
- schema-governed evidence artifacts;
- receipt-to-manifest and bundle-digest binding;
- CI-enforced contract, determinism, and security gates;
- artifact-only evidence handoff across environments;
- Linux-producer to Windows-verifier portability;
- standalone/no-checkout verification inside CI;
- fail-closed rejection after a one-byte evidence mutation;
- single-authority enforcement for registered repository-hosted adapters, including rejection of injected verdict, receipt, and bundle-identity authority;
- production mobile-browser manual witness for receipt-pin match and fail-closed mismatch;
- detached Ed25519 receipt-signature verification against an externally supplied recipient trust store.

The standalone verifier checks bundle **integrity**: manifest/file digests and byte counts, strict transferred-file membership, bundle binding, exactly one manifest-locked `ledger.jsonl`, receipt-to-manifest binding, decision-critical receipt claims against that ledger, and ledger hash-chain integrity. Verifier v0.4 uses the restricted `paygod-c14n-v1` profile, exposes `receipt_sha256` and `ledger_head`, and can fail closed against an externally supplied `--expect-receipt-sha256`. It can also verify an optional detached Ed25519 `receipt.sig.json` against a recipient-supplied external trust store. Its machine-readable result separates `integrity`, `issuer_authenticity`, `replay`, and `time_authority`; a top-level `status: valid` still means integrity verified within this documented boundary only. `issuer_authenticity: verified` means a trusted key signed this receipt commitment; it does not prove external evidence truth, regulator authorization, replay, or trusted time.

The single-authority witness is deliberately scoped: it covers adapters registered in `tools/check_repository_boundary.py`. New execution-facing surfaces must be registered and covered by the same boundary witness.

## What was accepted from external research?

Experimental research and the canonical public implementation have different evidentiary status. The [Observatory → Kernel evidence-transfer register](docs/OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md) identifies what the Kernel **already accepted**, what was only proven in a bounded research harness, and what remains unresolved.

- **Witnessed compatibility, not a new primitive:** a live external ACP descriptor with fractional JSON numbers failed closed at `paygod-c14n-v1`; a later shadow workflow preserved the captured external observation separately and supplied a compatible canonical input. This is an evidence-admission boundary, **not** a canonicalization defect or live ACP integration.
- **Already accepted:** [ADR 0003](adrs/0003-evidence-admission-before-decision-execution.md) requires pre-kernel evidence admission; missing, temporally unproven or unrepresentable mandatory facts remain `WITHHELD` and cause orchestration `NOT RUN`. Neither is a Kernel verdict.
- **Not promoted:** local experimental Warrant/E1/E2/S0 controlled-release results, external-provider acceptance, cross-enforcer portability and financial authority are not current Kernel capabilities. A bounded local test does not grant any of these claims.
- **Numeric interoperability:** fractional temperatures, emission factors and other external decimals need a separately versioned and tested admission/representation contract. None is shipped as a generic industrial profile.
- **One public software reference:** this repository is the canonical implementation source; research may inform it without automatically changing code or becoming a website feature.

## What is not yet proven

The repository does **not** yet prove:
- that an external real-world fact or claimed evidence issuer is truthful;
- a published production organization-level trust root with rotation/revocation;
- external institutional adoption beyond the recorded manual browser witness;
- a live bank/PSP release integration;
- autonomous authority over money movement;
- institutional adoption or willingness to pay.

**Integrity is not provenance.**

## Canonical trust path

```text
External fact/source
        |
        v
Evidence / provenance
        |
        v
Contract + Policy Pack
        |
        v
Deterministic Kernel
        |
        v
Decision Artifact
        |
        v
Manifest + Receipt + Ledger
        |
        v
Portable Evidence Bundle
        |
        v
Independent Verifier
```

Execution rails such as a bank, PSP, agent, or API are downstream consumers; they are not part of the kernel trust primitive.

## Architecture

```text
CLI -> Canonicalization -> Pack Evaluation -> Artifact Envelope -> Receipt/Ledger -> Witness -> CI Gate
```

Domain logic should enter through contracts, packs, or adapters before changing kernel semantics.

See [Architecture Audit](docs/ARCHITECTURE_AUDIT.md).

## Quickstart

Canonical developer onboarding: [START_HERE.md](START_HERE.md).

```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
```

```powershell
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1
```

Expected: `PASS` (strict) with matching digests.

## Portable verification

- `.github/workflows/portable-evidence.yml` — artifact handoff and cross-OS independent verification.
- `.github/workflows/standalone-verifier.yml` — versioned standalone verifier artifact, no repository checkout in recipient jobs, clean evidence -> integrity `verified`, one-byte tamper -> integrity `failed`.

See [Standalone Verifier](docs/STANDALONE_VERIFIER.md) and [Issuer Authenticity](docs/ISSUER_AUTHENTICITY.md).

## Main-branch enforcement

See [GATES.md](GATES.md). The governance contract defines stable required check contexts for kernel CI, security, deterministic enforcement, pack contracts, repository-boundary enforcement, and verifier integrity. The GitHub ruleset must remain aligned with those contexts.

## Next boundary

P0 — Gas Maintenance Workflow & Evidence-Admission Pilot is closed as `CLOSED — PASS WITH BOUNDARY`. It is a simulated workflow witness and contributes zero cases to B2-REAL.

The repository-wide **stop-build is ACTIVE**. Feature and security-capability expansion is frozen except for confirmed defect/security remediation and evidence-backed architecture changes. See [Stop-Build Rule](docs/STOP_BUILD_RULE.md).

Current validation work is:

1. **B2-REAL** — collect qualifying real/de-identified Gas Site Readiness cases under the frozen evidence-admission protocol. Current qualifying count remains 0 / 10.
2. **Virtuals X1** — Level 0 research freeze is **CLOSED** after the block-bound Base deployment witness in PR #99. The next step is one bounded **X1-R0 instrumentation case** under the frozen method. R0 remains shadow-only, the Kernel remains unchanged, and paid execution is not authorized until a separate explicit economic cap is approved.
3. Promote predecessor-state binding, post-flight conformance, next-transition eligibility, conditional-release authority, or other new primitives only after external witnesses demonstrate recurrence and operational value.

Do not treat P0, B2, or Virtuals X1 research as evidence of market demand, regulator approval, external evidence truth, or autonomous execution authority.

See [ROADMAP.md](ROADMAP.md) and [Virtuals X1](research/virtuals-x1/README.md).

## README contract

`README.md` is the public contract. Any merged architectural change that materially changes what Paygod is, a proven guarantee, the canonical trust path, required gates, or the supported developer workflow must update this file in the same change and distinguish **proven guarantees** from **roadmap claims**.
