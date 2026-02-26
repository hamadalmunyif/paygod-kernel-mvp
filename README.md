# Paygod Kernel MVP

![Paygod Kernel CI](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/ci.yml/badge.svg)
![Paygod CI Enforcement](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/ci-enforce.yml/badge.svg)
![Security Gate](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/security.yml/badge.svg)
![Pack Contract Gate](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/pack-contract.yml/badge.svg)

Paygod Kernel is a deterministic execution core built on contracts-first + evidence-first principles.

## Guarantees

1) Bit-for-bit deterministic execution  
2) Evidence-first artifact outputs  
3) CI-enforced safety gates  

## Local Quickstart
Start here: START_HERE.md
Build CLI:
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out

Run deterministic witness:
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1