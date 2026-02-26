Paygod Kernel MVP

![badges]

Paygod Kernel is a deterministic execution core built on contracts-first + evidence-first principles.

It enforces deterministic execution and independently verifiable evidence at CI level.

Why this matters

Deterministic runs eliminate ambiguity.

Evidence bundles remove trust assumptions.

CI-level enforcement prevents configuration drift.

Guarantees (MVP)

Bit-for-bit deterministic execution

Evidence-first artifact outputs (schema-governed)

CI-enforced safety gates (nothing lands on main if checks fail)

Architecture (at a glance)

CLI → Canonicalization → Pack Evaluation → Artifact Envelope → Witness → CI Gate

Example Artifact
{
  "artifact_type": "decision",
  "input_digest": "sha256:...",
  "pack_digest": "sha256:...",
  "bundle_digest": "sha256:..."
}
Quickstart (Local)

Start here: START_HERE.md

Build the CLI
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
Run deterministic witness
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1

Expected: PASS (strict) and matching digests.

What is enforced on main

Required checks must pass before merging to main:

Paygod Kernel CI

Paygod CI Enforcement

Security Gate

Pack Contract Gate
