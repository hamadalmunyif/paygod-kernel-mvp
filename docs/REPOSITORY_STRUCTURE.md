# PayGod Kernel Repository Structure — Current Implementation

Status: current code-oriented map. Historical `src/Paygod.*.Service` scaffolds are not evidence of independent, deployed microservices or available proprietary implementations.

```text
README.md / START_HERE.md         canonical public claims and onboarding
contracts/                       versioned JSON schemas and schema governance
spec/test-vectors/               canonicalization and ledger reference vectors
packs/core/, packs/providers/    policy-pack samples; drafts under packs/_drafts/
src/PayGod.Cli/                  canonical .NET policy run/pack CLI
api/server.js                    fail-closed demo HTTP surface
deploy/docker/api/app/Program.cs canonical CLI delegation adapter
tools/                           Python verifier, issuer-auth and CI checks
tests/                           .NET/contract/integrity test fixtures
adrs/                            accepted design decisions
docs/                            implemented boundary, experiments and historical plans
rehearsals/                      synthetic and external-readiness checks
research/                        bounded research cases, not shipped products
.github/workflows/               runnable verification and governance gates
```

## Practical entry points

- [README](../README.md): implementation and explicit non-claims.
- [START_HERE](../START_HERE.md): developer build, example packs, evidence witness.
- [Architecture](02_ARCHITECTURE.md): canonical decision path vs external evidence/authority.
- [Repository Boundary Closure](REPOSITORY_BOUNDARY.md): which adapters may delegate and how mutations are rejected.
- [Standalone Verifier](STANDALONE_VERIFIER.md): integrity vs recipient-key issuer-authentication.
- [Research acceptance register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md): what a separate experiment established and what it did **not** promote.
- [Current stop-build rule](STOP_BUILD_RULE.md): feature work requires evidence-backed governance.

## Explicitly not shown as shipped architecture

Do not infer that `src/Paygod.Ledger.Service`, `src/Paygod.Metrics.Service` or `src/Paygod.Kernel.Api` scaffolding implements a persistent distributed backend. Similarly, interfaces and potential extensions mentioned in early plans (cloud object store, panic switch, enterprise admin UI, hosted support, RBAC, OAuth/SSO) are neither verified production features nor a guaranteed commercial SKU.

## Public project identity

The canonical public implementation is this repository. A separate observatory may run experiments against pinned Kernel commits, but does not become a second supported public execution engine merely because its local tests pass. `paygod.net` should link to this repository for public capability and contribution claims.
