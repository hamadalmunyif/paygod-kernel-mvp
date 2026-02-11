# START HERE — Paygod Kernel MVP

## What is this repository?
This repository is **not** an application, SDK, or feature library.

It is a **governance kernel** designed to enforce **deterministic outputs**
through:
- Fixed schemas (contracts)
- Explicit policy packs
- Non-bypassable execution gates (CI)

If something enters `main`, it has:
- Passed a contract
- Passed a gate
- Left an auditable trail

---

## Why does this exist?
Modern systems fail not because of missing features,
but because **outputs drift** and decisions become unverifiable.

Paygod Kernel exists to solve one problem only:

> **Make decisions, evidence, and outputs structurally provable.**

Everything else is intentionally secondary.

---

## Project Phases (Locked History)

### Phase 1 — Kernel Lock
**Status: Closed**

- Schemas are the single source of truth
- No interpretation after lock
- `main` represents a legal baseline

Changing a schema requires a governance decision, not a refactor.

---

### Phase 2 — Proof Run
**Status: Closed**

- Execution model:
  input → decision → evidence → ledger_entry
- Outputs are reproducible
- CI acts as an execution witness

This phase proved that the kernel is operable, not theoretical.

---

### Phase 3 — Pack Contract Gate (Current Phase)
**Status: Active**

This phase introduces **developer-proof onboarding**.

- Every `pack.yaml` must validate against:
  contracts/schemas/pack.schema.json
- Validation runs locally and in GitHub Actions
- Failure = no merge

There are no exceptions.

---

## Where should developers start?

❌ Do NOT start with BUILD.md  
❌ Do NOT start by writing code  
❌ Do NOT guess how Packs work  

✅ Start here, in this exact order:

1. Read this file completely
2. Read `GATES.md`
3. Study the reference Pack:
   packs/core/bap-output-validator-guard/pack.yaml

That Pack is the **canonical learning artifact**.

---

## What is a Pack?
A Pack is **not** code.

A Pack is:
- A policy contract
- A deterministic rule set
- A governance unit

If a Pack is ambiguous, the system is already broken.

---

## How to build a new Pack (Required Process)

1. Copy the reference Pack structure
2. Modify only:
   - metadata
   - spec.policy.rules
3. Do NOT change schemas
4. Validate locally:
   python tools/pack_validate.py
5. Open a Pull Request

If the Pack Contract Gate fails:
- The Pack is invalid
- The design is incomplete
- The PR must not merge

---

## Definition of Done (Non-negotiable)

A change is considered complete **only if**:

- All Gates pass
- No schema is altered without governance approval
- Outputs remain deterministic

If it requires explanation, it is not done.

---

## What this repository is NOT

- A feature playground
- A rapid prototype sandbox
- A framework with optional rules

This is a **kernel**.
Kernels do not bend.

---

## Short Look Ahead

Future work may include:
- Standardized governance Packs
- Compliance measurement instead of interpretation
- External systems integrating via contracts, not trust

These will only happen **after** the kernel proves immovable.

> If you feel confused, the Gate is doing its job.
> If you feel blocked, the contract is protecting the system.
