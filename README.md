# Paygod Kernel

![CI](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/ci.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub issues](https://img.shields.io/github/issues/hamadalmunyif/paygod-kernel-mvp)](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues)
[![GitHub stars](https://img.shields.io/github/stars/hamadalmunyif/paygod-kernel-mvp)](https://github.com/hamadalmunyif/paygod-kernel-mvp/stargazers)

**Paygod Kernel** is a contracts-first, evidence-first core for **continuous compliance and measurement**.

It turns any operational event into:
- **Observation** → **Measurement** → **Impact** → **Evidence** → **Ledger proof**
- governed by **versioned contracts (schemas)** and **versioned packs (policy bundles)**

## 🚀 Starter Packs (MVP-ready)

| Pack | Scope | Notes |
|------|-------|------|
| **[secrets-in-repo-guard](./packs/core/secrets-in-repo-guard)** | Core | Prevents credential leaks (API keys, passwords) before they enter the repo. |
| **[critical-cve-blocker](./packs/core/critical-cve-blocker)** | Core | Blocks artifacts with Critical CVEs (e.g., CVSS >= 9.0). |
| **[cross-border-pii-guard](./packs/core/cross-border-pii-guard)** | Core | Enforces **evidence refs only** and prevents PII/raw payload leakage by design. |
| **[iso27001-policy-review](./packs/core/iso27001-policy-review)** | Core | Base ISO 27001 control checks (starter). |
| **[ghg-scope-1-2-guard](./packs/core/ghg-scope-1-2-guard)** | Core | Sustainability guardrails (Scope 1/2). |
| **[admin-drift-detection](./packs/providers/aws/admin-drift-detection)** | AWS Provider | Provider-specific pack (must live under `packs/providers/...`). |

> Draft packs (not part of MVP core): `packs/_drafts/*`

## Quickstart (local)

Prereqs:
- .NET SDK 8 (see `global.json`)
- Docker Engine / Desktop
- Python 3.11+ (tooling only: schema/spec utilities)

### 1) Build the CLI
```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
# dotnet publish outputs ProjectName by default
if [ -f "out/PayGod.Cli" ]; then mv out/PayGod.Cli out/paygod; fi
chmod +x out/paygod
```

### 2) Run pack tests (CLI = source of truth)
```bash
./out/paygod test --pack packs/core/secrets-in-repo-guard
./out/paygod test --pack packs/core/critical-cve-blocker
./out/paygod test --pack packs/providers/aws/admin-drift-detection
```

### 3) Run local stack (services are currently stubbed)
```bash
cd deploy/docker
docker compose up --build
```

## Repo map
- `contracts/` — canonical JSON schemas (versioned)
- `packs/`
  - `packs/core/<pack-name>` — **cloud-agnostic** packs (no provider-specific logic)
  - `packs/providers/<cloud>/<pack-name>` — provider-specific packs only
  - `packs/_drafts/<pack-name>` — incomplete packs (not in MVP)
- `src/` — .NET services + CLI
- `tools/` — python utilities (schema/manifest/spec), **not** a policy runner
- `docs/` — vision, axioms, governance, ledger, metrics, profiles
- `deploy/` — docker-compose + k8s stubs
- `.github/` — CI/security/release workflows

## Build
See `BUILD.md`.

## Governance
See `GOVERNANCE.md` and `MODEL_GOVERNANCE.md`.

## License
Apache-2.0. See `LICENSE` and `NOTICE`.


## Examples

- `examples/sample.json`: sample input payload used during local experimentation.
- `examples/tmp_entry.json`: sample ledger entry shape for quick manual checks.
