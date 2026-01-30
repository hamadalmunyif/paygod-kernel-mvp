# Contributing to Paygod Kernel

Thank you for your interest in contributing to Paygod! We welcome contributions from the community to help build the most robust policy-as-code kernel.

## 🤝 Code of Conduct
This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code. Please report unacceptable behavior to `conduct@paygod.org`.

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
- Use `docs/adr/` for decisions that affect the kernel contracts, ledger, metrics model, or governance.
- Prefer small ADRs that clearly state: context, decision, alternatives, consequences.

## Pull requests
- Keep PRs small and focused.
- CI must be green (contracts, tests, security checks).
- Ensure new features are covered by tests (`dotnet run --project src/PayGod.Cli -- test --pack ...`).
