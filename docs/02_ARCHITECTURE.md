# PayGod Kernel — Implemented Architecture and Research Boundary

Status: **CURRENT CODE-ALIGNED OVERVIEW** (2026-10-10). This page supersedes earlier unimplemented diagrams that described a production microservice mesh, financial executor, hosted identity service, SLA, WORM storage, or an autonomous payment gateway. Those were design possibilities, not current shipped capabilities.

## Scope

PayGod Kernel is a deterministic, contracts-first decision core. Its canonical CLI evaluates a versioned policy pack against admitted inputs and produces inspectable artifacts. Manifest, receipt and hash-linked ledger allow a recipient to verify covered *integrity* assertions after export, without rerunning the original pack. An optional detached Ed25519 receipt signature authenticates a receipt commitment against a recipient-supplied trusted key.

Read [README](../README.md) for the complete evidence and non-claims, [Architecture Audit](ARCHITECTURE_AUDIT.md) for invariants and [Research Transfer Register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md) for the disposition of external experiments.

## Current boundaries

```text
External observation / claim  (not implicitly trusted)
    |
    v
Evidence admission outside the Kernel
    | TRUE / FALSE when justified
    | WITHHELD -> orchestration NOT RUN
    v
Contract + Policy Pack
    |
    v
Canonical CLI / deterministic Kernel
    |
    +--> decision and evidence artifacts
    +--> receipt / manifest / hash-linked ledger
              |
              v
       Portable Evidence Bundle
              |
              v
     Standalone independent verifier
       [integrity / optional issuer signature]
              |
              v
   Recipient's own reliance / execution decision
```

The Kernel owns canonical decision and artifact semantics; it does **not** own external truth, organization-level authority, downstream signing, banking settlement or autonomous transaction execution.

## Present repository components

- `src/PayGod.Cli/` — canonical CLI run/test/validate and policy evaluation path.
- `contracts/` and `spec/test-vectors/` — versioned schemas and reference vectors.
- `packs/` — contracted policy inputs and tested starter packs; domain evidence still needs independent admission.
- `tools/verify_portable_evidence.py` and issuer-auth support — independent artifact integrity and optional receipt-key verification.
- `api/server.js` — demo/liveness API; execution-like routes deliberately fail closed.
- `deploy/docker/api/app/Program.cs` — delegates to the canonical CLI rather than creating a local verdict/receipt/bundle identity.
- `.github/workflows/` — CI contracts, portable/no-checkout verifier tests, boundary mutation tests and documentation checks.

The observed witness boundary for registered adapters is [Repository Boundary Closure](REPOSITORY_BOUNDARY.md). Its tests do not certify unregistered or independent external adapters.

## Canonicalization and numeric evidence

`paygod-c14n-v1` accepts only JSON safe integers (not fractional/exponent numbers), booleans, strings, arrays, objects and null under its stated Unicode contract. An external temperature, emission factor or agent descriptor containing a decimal must not be coerced silently or used to expand this profile implicitly.

Observed external Witness 001 failed closed on a fractional ACP descriptor before succeeding on a separated, correctly admitted shadow envelope. The **transferable lesson** is an explicit admission boundary preserving raw captured evidence; a general industrial fixed-point profile has **not** been implemented. See [Research Transfer Register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md).

## Adapters, verifiers and execution

- Only the canonical Kernel originates canonical decisions and decision-related artifacts.
- An adapter may submit, transport, invoke and expose canonical output; it may not invent a verdict, receipt or bundle digest.
- A verifier verifies transferred evidence within explicit trust dimensions; it does not recreate external events.
- A downstream institution or delegated enforcer remains the owner of any payment, workflow or other consequential act.
- Closed-harness warrant/E1/E2 experiments are **not** shipped Kernel authority primitives.

## Historical ideas that remain unimplemented

Do **not** advertise the following as current software from older versions of this page: a distributed microservice architecture, `IAuthProvider` with enterprise OIDC, production `ILedgerStore` persistence/WORM storage, `IPanicSwitch`, production bank/PSP executor, secure enclave, certified OSCAL controls, automated incident fallback, guaranteed availability or latency SLOs, or Kubernetes HA deployment.

These are possible future designs only if independent need and new governed evidence justify them. The [Stop-Build Rule](STOP_BUILD_RULE.md) is active.

## Changes and review

A new source/adapter or measurement contract must preserve the existing versioned evidence meaning; an architectural change requires explicit governance, versioned tests, independent witnesses as appropriate, and an updated README. Research results do not automatically modify this architecture.
