# PayGod Kernel — Documentation

**Canonical public implementation:** [paygod-kernel-mvp](https://github.com/hamadalmunyif/paygod-kernel-mvp)

PayGod is a deterministic contracts-first policy/decision Kernel producing portable evidence bundles. Its independently runnable verifier checks documented integrity dimensions; optional receipt-key authentication is separate from external source truth, organization authority, policy replay or trusted time.

## Start with what is implemented

- [README and current claims](../README.md)
- [Build and verification quickstart](../START_HERE.md)
- [Code-aligned architecture](02_ARCHITECTURE.md)
- [Standalone verifier and its non-claims](STANDALONE_VERIFIER.md)
- [Registered adapter / canonical decision boundary](REPOSITORY_BOUNDARY.md)
- [Architectural audit](ARCHITECTURE_AUDIT.md)

## Evidence and research boundaries

- [Observatory research transfer / acceptance register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md)
- [Evidence Admission ADR 0003](../adrs/0003-evidence-admission-before-decision-execution.md)
- [Internal verification challenge](INTERNAL_VERIFICATION_CHALLENGE.md)
- [Repository Stop-Build rule](STOP_BUILD_RULE.md)
- [Open Core: current software vs possible commercial paths](OPEN_CORE_POLICY.md)

Unapproved research results and historical blueprints are **not** part of the Kernel's shipped capability, even when their local tests are successful. The web project should treat this repository as the only canonical public implementation source.
