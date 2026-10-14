# Contributing to Paygod Kernel

Thank you for your interest in contributing to Paygod! We welcome contributions from the community to help build the most robust policy-as-code kernel.

## 🤝 Code of Conduct
This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code. Please follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for the repository's published reporting procedure; this page does not assert that an unverified contact mailbox is operated.

## Current feature boundary

The former repository-wide stop-build was superseded on 2026-10-14 by the [scoped evidence-governed development rule](docs/STOP_BUILD_RULE.md), accepted in [PR #108](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/108). Developers may explore, author private Packs, run permitted local fixtures, write independent optional adapters, and contribute upstream-native fixes without waiting for unrelated research lanes. This permission does **not** waive consent, security, privacy, external execution authority, or protected Kernel gates. Consult the [research acceptance register](docs/OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md) for claim boundaries; canonicalization, receipt, ledger, authority, and verifier semantic changes require a reproducible witness, reviewed ADR, compatibility/negative tests, and the protected merge process.

The public website should point to **this** repository as the canonical implemented software. A bounded research-harness test is not a shipped Kernel product or third-party security validation.

## Core Rules
- **Contracts-first:** if you change anything under `contracts/`, you must add/update fixtures and contract tests.
- **Evidence-first:** new behaviors should emit verifiable records (Decision/Measurement/Evidence) and be anchorable in the ledger.
- **No silent breaking changes:** follow `contracts/versioning/SCHEMA_SEMVER_POLICY.md`.

## 📜 Open Core Guidelines
PayGod's source is distributed under Apache-2.0. **Open Core is an optional future commercial strategy, not a delivered enterprise edition.** For ordinary upstream code review:

*   **We can review** proposed contributions to the Kernel, CLI, Public Schemas, and Community Packs under the repository's current scoped contribution and architectural-review rules; proposing a Pack does not guarantee acceptance.
*   **We do NOT accept** features that are strictly "Enterprise-only" (e.g., closed-source backend dependencies) into this repository.
*   All contributions must be compatible with the **Apache 2.0 License**.

A merged Community Pack is **not** a production certification or a guaranteed place in a curated Pack catalog. A future creator-benefit/revenue-sharing/accreditation process has **not** been approved. Any rights or compensation beyond the existing code license require separate explicit terms. See [OPEN_CORE_POLICY.md](docs/OPEN_CORE_POLICY.md) and the [claims register](docs/CLAIMS_REGISTER.md).

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

## Build privately; contribute optionally

You may write and test Packs in your own workspace and keep them private. A PayGod hosted account, public fork, upstream PR, or maintainer approval is **not** required for a local development experiment within your authorized environment. No guarantee of production fitness is implied.

Start with [EIK developer/agent onboarding](docs/eik/README.md), [Pack examples](docs/STARTER_PACKS.md), and [ADR 0003](adrs/0003-evidence-admission-before-decision-execution.md). Missing mandatory source evidence is `WITHHELD / NOT RUN` in **pre-Kernel orchestration**, never a forged Kernel verdict. Pack schema validation and Pack unit tests do not establish source truth, complete admission, authorization, or institutional acceptance. If you choose to send a Pack upstream, include cases for missing/invalid data and an honest scope statement.

## Pull requests
- Keep PRs small and focused.
- CI must be green (contracts, tests, security checks).
- Ensure new features are covered by tests (`dotnet run --project src/PayGod.Cli -- test --pack ...`).
