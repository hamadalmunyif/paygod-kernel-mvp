# Paygod Kernel MVP

![Paygod Kernel CI](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/ci.yml/badge.svg)
![Paygod CI Enforcement](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/ci-enforce.yml/badge.svg)
![Security Gate](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/security.yml/badge.svg)
![Pack Contract Gate](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/pack-contract.yml/badge.svg)

**Paygod Kernel** is a deterministic execution core built on **contracts-first + evidence-first** principles.  
Goal: turn any run/check/decision into **verifiable artifacts** (Decision / Evidence / Ledger Entry) that can be independently validated.

## Guarantees (MVP)
1) **Bit-for-bit deterministic execution**
2) **Evidence-first artifact outputs (schema-governed)**
3) **CI-enforced safety gates** (nothing lands on `main` if checks fail)

## Quickstart (Local)
**Start here:** `START_HERE.md`

### Build the CLI
```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
```

### Run deterministic witness (double-run)
```powershell
pwsh -NoProfile -File ./tools/phase4_docker_witness.ps1
```

Expected: PASS (strict) and matching digests.

### What is enforced on main
Required checks must pass before merging to `main`:
- Paygod Kernel CI
- Paygod CI Enforcement (witness + proof)
- Security Gate
- Pack Contract Gate
