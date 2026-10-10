# Open Core — Strategy and Present Availability

Status: **STRATEGIC OPTION, NOT A SHIPPED ENTERPRISE EDITION** (2026-10-10).

PayGod Kernel is an openly available source repository licensed under [Apache License 2.0](../LICENSE). The objective is that developers can inspect and independently run the canonical engine, packs, public schemas, and verification tooling under that license. Access to the source does not require a hosted PayGod subscription.

This document describes *possible* commercial boundaries and does not claim that enterprise offerings, registered trademarks, regulated security certifications, paid licenses, subscriptions, SSO or SLAs exist today.

## What is actually present

| Layer | Available reference | Boundary |
|---|---|---|
| Canonical engine / CLI | `src/PayGod.Cli/`, `START_HERE.md` | Deterministic evaluation with compatible inputs |
| Public contracts and packs | `contracts/`, `packs/`, `spec/test-vectors/` | Versioned contracts; packs are not regulatory endorsements |
| Portable verification | `tools/verify_portable_evidence.py`, `docs/STANDALONE_VERIFIER.md` | Integrity, bindings and optional key-based receipt authentication |
| Registered delegation adapters | `api/server.js`, `deploy/docker/api/app/Program.cs` | Enforced single canonical authority within registered adapter scope |
| Hosted enterprise management plane | **Not demonstrated in this repository** | No delivered dashboard, login, RBAC, customer management, subscriptions or billing |

## Potential value-creation arrangements (uncommitted)

- Self-hosted Kernel and local/offline verifier as open tools.
- Optional managed hosted execution or verification subject to future security/operational validation.
- Enterprise integration engineering, support, key governance, observability, or historical evidence services.
- Community/vendor-written packs, acceptance profiles and independent interoperability suites.
- Contractual or standards-based adoption independent of PayGod-hosted usage.

Open licensing permits independent use and hosting. It does not guarantee that the originating project captures the economics of all downstream uses. Neither an enterprise SKU nor a metered Kernel API is a current verified offering.

Earlier drafts used `paygod login`, `paygod sync`, `audit-upload`, HIPAA/FedRAMP packs, AWS/Azure/Okta/Splunk connectors, dashboard, RBAC and proprietary enterprise licensing as if these were product columns. **Treat all of those as unimplemented options.** No guarantee of their existence, planned delivery or price is made.

## Governance and contribution

Changes to Kernel semantics require the [Stop-Build Rule](STOP_BUILD_RULE.md), suitable negative tests and explicit ADR/architecture approval. Avoid proprietary dependencies in canonical open semantics. Developers should consult [Contributing](../CONTRIBUTING.md) and [Research Transfer Register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md).

Brand/trademark assertions require a separate legal review; Apache-2.0 and any eventual mark rights must not be conflated.
