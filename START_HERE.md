# Start Here — Paygod Kernel MVP

Paygod is a deterministic policy-execution kernel that produces portable, independently verifiable evidence bundles.

Read [README.md](README.md) first for current guarantees/non-claims and [docs/ARCHITECTURE_AUDIT.md](docs/ARCHITECTURE_AUDIT.md) before changing kernel semantics.

## Prerequisites
- .NET SDK 8
- Docker Engine/Desktop
- PowerShell 7+
- Python 3.11+ for tooling/verifier work

## Build
```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
```

## Deterministic witness
```powershell
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1
```
Expected: `PASS` and matching digests.

## Pack tests
```bash
./out/paygod test --pack packs/core/secrets-in-repo-guard
./out/paygod test --pack packs/core/critical-cve-blocker
./out/paygod test --pack packs/core/cross-border-pii-guard
./out/paygod test --pack packs/core/ghg-scope-1-2-guard
./out/paygod test --pack packs/core/iso27001-policy-review
./out/paygod test --pack packs/providers/aws/admin-drift-detection
```

## Verification boundaries
Portable-evidence and standalone-verifier witnesses test transferred evidence, no-checkout verification, and tamper rejection. See `docs/PORTABLE_EVIDENCE_WITNESS.md` and `docs/STANDALONE_VERIFIER.md`.

These prove integrity/binding inside the documented trust boundary, not external fact truth.

## Before changing the kernel
Preserve canonicalization/digest semantics, deterministic pack evaluation, evidence-bundle construction, receipt binding, ledger-chain rules, verifier fail-closed behavior, and the no-checkout boundary unless a failing real domain pilot proves a change is required.

Domain behavior belongs in a pack or adapter first.

## Main enforcement
See [GATES.md](GATES.md).

## Repository map
- `src/PayGod.Cli/`
- `src/Paygod.Contracts/`
- `src/Paygod.ControlEngine/`
- `contracts/schemas/`
- `packs/`
- `tools/verify_portable_evidence.py`
- `docs/ARCHITECTURE_AUDIT.md`
