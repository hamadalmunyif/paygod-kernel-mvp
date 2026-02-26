# Start Here — Paygod Kernel MVP

This repo is a deterministic execution kernel that produces verifiable evidence bundles.

## 1) Prereqs
- .NET SDK 8
- Docker Engine/Desktop
- PowerShell 7+
- Python 3.11+ (tooling only)

## 2) Build the CLI
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out

If the output binary is `out/PayGod.Cli`, rename it to `out/paygod` (Linux/macOS) and chmod +x.

## 3) Run the deterministic witness (double-run)
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1

Expected: PASS and matching digests.

## 4) Run a pack test suite (local)
./out/paygod test --pack packs/core/secrets-in-repo-guard
./out/paygod test --pack packs/core/critical-cve-blocker
./out/paygod test --pack packs/core/cross-border-pii-guard
./out/paygod test --pack packs/core/ghg-scope-1-2-guard
./out/paygod test --pack packs/core/iso27001-policy-review
./out/paygod test --pack packs/providers/aws/admin-drift-detection

## 5) What gets enforced on main
Merges to `main` are blocked unless required CI checks pass:
- Paygod Kernel CI
- Paygod CI Enforcement (witness + proof)
- Security Gate
- Pack Contract Gate

## 6) Where to look next
- docs/02_ARCHITECTURE.md
- docs/11_OUTPUT_ARTIFACTS.md
- docs/BELLOOP_ARTIFACT_PROTOCOL.md
- contracts/schemas/
- packs/core/