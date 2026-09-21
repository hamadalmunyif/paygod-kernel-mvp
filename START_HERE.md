# Start Here — Paygod Kernel MVP

Paygod Kernel is a deterministic policy-execution kernel that produces portable, independently verifiable evidence bundles.

Read [README.md](README.md) first for current guarantees and non-claims. See [docs/ARCHITECTURE_AUDIT.md](docs/ARCHITECTURE_AUDIT.md) for architecture boundaries.

## 1. Prerequisites
- .NET SDK 8
- Docker Engine/Desktop
- PowerShell 7+
- Python 3.11+ for tooling/verifier workflows

## 2. Build the CLI
```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
```

## 3. Run the deterministic witness
```powershell
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1
```
Expected: `PASS` with matching digests.

## 4. Run pack tests
```bash
./out/paygod test --pack packs/core/secrets-in-repo-guard
./out/paygod test --pack packs/core/critical-cve-blocker
./out/paygod test --pack packs/core/cross-border-pii-guard
./out/paygod test --pack packs/core/ghg-scope-1-2-guard
./out/paygod test --pack packs/core/iso27001-policy-review
./out/paygod test --pack packs/providers/aws/admin-drift-detection
```

## 5. Evidence boundary
Current CI witnesses cover cross-environment artifact-only verification, Linux -> Windows verification, standalone/no-checkout recipient verification, and one-byte tamper rejection.

See:
- `docs/PORTABLE_EVIDENCE_WITNESS.md`
- `docs/STANDALONE_VERIFIER.md`
- `tools/verify_portable_evidence.py`

These prove integrity and portability within the stated test boundaries. They do not prove external-source truth.

## 6. Main-branch gates
See [GATES.md](GATES.md). The canonical required contexts are `Paygod Kernel CI`, `security-gate`, `Paygod CI Enforcement`, `Pack Contract (paygod/v1)`, and `Repository Boundary Gate`. The active GitHub ruleset must require all five; workflow success alone is not governance closure.

## 7. Where to look next
- `docs/ARCHITECTURE_AUDIT.md`
- `docs/02_ARCHITECTURE.md`
- `docs/11_OUTPUT_ARTIFACTS.md`
- `docs/BELLOOP_ARTIFACT_PROTOCOL.md`
- `contracts/schemas/`
- `packs/core/`
- `ROADMAP.md`

## 8. Contribution rule
Do not change canonicalization, digest construction, receipt binding, ledger-chain rules, deterministic pack semantics, or verifier fail-closed behavior merely to accommodate a domain feature.

Try contracts, packs, or adapters first. Kernel-semantic changes require explicit justification and regression evidence.
