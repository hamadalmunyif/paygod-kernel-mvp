# Contributing to Paygod Kernel

Thank you for your interest in contributing to Paygod! We welcome contributions from the community to help build the most robust policy-as-code kernel.

## 🤝 Code of Conduct
This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code. Please follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for the repository's published reporting procedure; this page does not assert that an unverified contact mailbox is operated.

## Current feature boundary

The repository-wide [Stop-Build Rule](docs/STOP_BUILD_RULE.md) is ACTIVE. A proposal arising from external research does not authorize a Kernel primitive. First read the [research acceptance register](docs/OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md), reproduce the behavior, classify the gap, and determine whether an existing contract/pack/admission adapter is sufficient. Any proposal to alter versioned canonicalization, receipt, ledger, authority or verifier semantics needs an explicit, reviewed and evidenced architecture decision.

The public website should point to **this** repository as the canonical implemented software. A bounded research-harness test is not a shipped Kernel product or third-party security validation.

## Core Rules
- **Contracts-first:** if you change anything under `contracts/`, you must add/update fixtures and contract tests.
- **Evidence-first:** new behaviors should emit verifiable records (Decision/Measurement/Evidence) and be anchorable in the ledger.
- **No silent breaking changes:** follow `contracts/versioning/SCHEMA_SEMVER_POLICY.md`.

## 📜 Open Core Guidelines
Paygod operates under an **Open Core** model. This means:

*   **We accept** contributions to the Kernel, CLI, Public Schemas, and Community Packs.
*   **We do NOT accept** features that are strictly "Enterprise-only" (e.g., closed-source backend dependencies) into this repository.
*   All contributions must be compatible with the **Apache 2.0 License**.

See [OPEN_CORE_POLICY.md](docs/OPEN_CORE_POLICY.md) for more details on the boundary between Community and Enterprise editions.

## Sign your commits (DCO)
We use the **Developer Certificate of Origin (DCO)**. Every commit must include a `Signed-off-by` line.

- Read `DCO`.
- Use:
  - `git commit -s -m "Your message"`

If you forgot, you can amend:
- `git commit --amend -s`
- `git push --force-with-lease` (if needed)

## Architectural decisions
- Use the existing [ADRs](adrs/) and versioned governance records for decisions affecting kernel contracts, ledger, metrics, or authority; avoid silently creating a conflicting ADR tree.
- Prefer small ADRs that clearly state: context, decision, alternatives, consequences.

## Pull requests
- Keep PRs small and focused.
- CI must be green (contracts, tests, security checks).
- Ensure new features are covered by tests (`dotnet run --project src/PayGod.Cli -- test --pack ...`).
