# Governance — Lean Core, Trusted Packs

This repository is **open-source** and aims to close the gap between **verification**, **compliance**, and **proof**.
The core principle is: **every change must be explainable**, and **every decision must be reproducible**.

## Operating model

We run a hybrid model:

- **Lean Core**: keep the kernel and CLI easy to contribute to (low friction).
- **Trusted Packs**: policy packs are the “product surface”, so we apply higher assurance for packs that claim trust.

## Roles

### Maintainers
Maintainers are responsible for:
- merging PRs
- approving releases
- managing schema and ledger compatibility
- curating *Verified* packs

Maintainers are listed in `CODEOWNERS`.

### Contributors
Anyone may contribute via PRs under the rules in `CONTRIBUTING.md` and `DCO`.

## Decision-making

- **Small changes**: maintainers merge by review.
- **Breaking / high-impact changes** (schemas, ledger format, policy DSL semantics):
  - require an ADR in `adrs/`
  - optionally a discussion RFC in `rfcs/` for larger design changes

## DCO

This project uses **DCO** (Developer Certificate of Origin). All commits must be signed-off.

## Packs trust levels

### Community Pack (default)
Requirements:
- passes schema validation
- includes `tests/cases.yaml`
- passes pack tests in CI

### Verified Pack
Verified packs require:
- all of the above, plus
- **two maintainer approvals**
- **pinned dependencies** (no floating references)
- the merge commit is signed (GPG / verified)

See `MODEL_GOVERNANCE.md` for the pack lifecycle.

## Schema stability

JSON Schemas are contracts. Changes must follow:
- `contracts/versioning/SCHEMA_SEMVER_POLICY.md`
- `contracts/schema-manifest.json` is updated via tooling (see `docs/SCHEMA_STABILITY.md`)

## Security

See `SECURITY.md` for reporting vulnerabilities and secure contribution expectations.
