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
- single-authority enforcement for registered repository-hosted adapters, including rejection of injected verdict, receipt, and bundle-identity authority.

The standalone verifier checks manifest integrity, artifact SHA-256 digests, bundle-digest binding, receipt binding, and ledger hash-chain integrity where present.

The single-authority witness is deliberately scoped: it covers adapters registered in `tools/check_repository_boundary.py`. New execution-facing surfaces must be registered and covered by the same boundary witness.

## What is not yet proven

The repository does **not** yet prove:
- that an external real-world fact or claimed evidence issuer is truthful;
- a published/signed external verifier trust root;
- an external-device/party verification witness outside repository CI;
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
- `.github/workflows/standalone-verifier.yml` — versioned standalone verifier artifact, no repository checkout in recipient jobs, clean evidence -> `VALID`, one-byte tamper -> `INVALID`.

See [Standalone Verifier](docs/STANDALONE_VERIFIER.md).

## Main-branch enforcement

See [GATES.md](GATES.md). The governance contract defines stable required check contexts for kernel CI, security, deterministic enforcement, pack contracts, and repository-boundary enforcement. The GitHub ruleset must remain aligned with those contexts.

## Next boundary

0. Complete main-ruleset alignment with the stable required check contexts in `GATES.md`.
1. Package and test the verifier outside repository CI.
2. Select one bounded real-domain workflow and derive the minimum evidence-provenance contract it actually requires.
3. Implement that domain authority pack without changing frozen kernel semantics.
4. Stop generic feature development.
5. Run a shadow pilot against real human decisions.

First candidate:

```text
invoice + PO + facility state + collateral/evidence + policy
                         |
                         v
              RELEASE / REDUCE / HOLD
                         |
                         v
                       receipt
```

See [ROADMAP.md](ROADMAP.md).

## README contract

`README.md` is the public contract. Any merged architectural change that materially changes what Paygod is, a proven guarantee, the canonical trust path, required gates, or the supported developer workflow must update this file in the same change and distinguish **proven guarantees** from **roadmap claims**.
