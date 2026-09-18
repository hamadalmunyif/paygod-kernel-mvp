# Paygod Kernel MVP

Paygod Kernel is a deterministic policy-execution core built on **contracts-first + evidence-first** principles.

It produces portable decision evidence that can be independently verified without replaying the original decision.

## What is proven

Repository witnesses currently prove deterministic execution, schema-governed evidence, receipt/manifest/bundle binding, tamper-evident ledger verification where present, artifact-only handoff, Linux-producer to Windows verification, standalone/no-checkout verification inside CI, clean evidence -> `VALID`, and one-byte mutation -> `INVALID`.

The standalone witness is a **CI-level portability proof**. It is not yet a claim of a published/signed external verifier trust root or of real-world evidence truth.

## Canonical trust path

```text
External fact/source
        ↓
Evidence / provenance
        ↓
Contract + Policy Pack
        ↓
Deterministic Kernel
        ↓
Decision Artifact
        ↓
Manifest + Receipt + Ledger
        ↓
Portable Evidence Bundle
        ↓
Independent Verifier
```

Execution rails such as a bank, PSP, agent, or external API are downstream consumers. They are not part of the kernel trust primitive.

## Architecture

```text
CLI -> Canonicalization -> Pack Evaluation -> Artifact Envelope
    -> Manifest / Receipt / Ledger -> Portable Evidence -> Independent Verifier
```

Domain logic should enter through contracts, packs, and adapters before any change to kernel semantics.

See [docs/ARCHITECTURE_AUDIT.md](docs/ARCHITECTURE_AUDIT.md) for the post-#53 KEEP / FREEZE / REVIEW / MISSING audit.

## Quickstart

Developer onboarding: [START_HERE.md](START_HERE.md)

```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
```

```powershell
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1
```

Expected: `PASS` with matching digests.

## Main-branch enforcement

Required CI gates protect kernel build/test, deterministic enforcement, security, and pack contracts. See [GATES.md](GATES.md). Portability workflows additionally test transferred evidence and standalone verification behavior.

## Current non-claims

Paygod does **not yet prove** external real-world fact truth, a published/signed external verifier trust root, a live bank/PSP conditional-release integration, autonomous authority over money movement, institutional adoption, or willingness to pay.

## Next boundary

```text
External verifier distribution
 -> Evidence Provenance Contract
 -> One real domain pack
 -> Shadow pilot
 -> Conditional-release pilot
```

Generic feature expansion stops until a real workflow demonstrates a need for it.

## README contract

This README is the public entry point. Any merged architectural change that materially changes what Paygod is, what has been proven, the trust path, required gates, or the supported developer workflow must update this file and distinguish **proven guarantees** from **roadmap claims**.
