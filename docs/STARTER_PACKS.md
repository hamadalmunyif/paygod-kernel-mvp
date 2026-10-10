# PayGod Starter Packs — Executable Policy Examples

**Status: IMPLEMENTED PACKS / FIXTURE-TESTED; NOT PRODUCTION-ACCREDITED**  
**Source of claims:** [Kernel Claims Register](CLAIMS_REGISTER.md) · [Stop-Build](STOP_BUILD_RULE.md) · [Pack Contract](../contracts/schemas/pack.schema.json)

A PayGod Pack defines **input expectations, ordered policy rules and fixture cases**. The Kernel evaluates rules using admitted input and produces bounded decision evidence. Packs **do not themselves** scan Git histories, query a cloud provider, certify compliance, prove external reports are accurate, enforce deployment at a CI/CD target, or execute release authority outside the canonical Kernel.

## Included examples

| Pack | Actual input and policy behavior | Upstream responsibility | What it does **not** establish |
|---|---|---|---|
| [secrets-in-repo-guard](../packs/core/secrets-in-repo-guard/) | Uses a supplied `scan_report.secrets_found` count to `deny` when positive or `allow` when zero | External scanner must run, supply a complete report and authenticate it | Not a built-in Git scanner; does not guarantee absence of secrets |
| [critical-cve-blocker](../packs/core/critical-cve-blocker/) | Uses supplied `cvss_score_x10` / fix status; unpatched critical ≥90 `deny`, high 70–89 `flag` | A scanner such as Trivy/Grype must supply a valid complete report | Not a scanning service; `allow` does not prove code is vulnerability-free or deployment was blocked |
| [cross-border-pii-guard](../packs/core/cross-border-pii-guard/) | Evaluates declared cross-border PII conditions under its Pack policy | Data classification and cross-border attributes must be supplied appropriately | Not a legal transfer determination or regulatory approval |
| [ghg-scope-1-2-guard](../packs/core/ghg-scope-1-2-guard/) | Evaluates the presence of methodology, evidence and factor **references** for previously calculated integer-kg Scope 1/2 fields | Producer must measure, calculate, verify and attribute factors and references | Not emissions calculation, certified measurement or GHG conformity assurance |
| [iso27001-policy-review](../packs/core/iso27001-policy-review/) | Evaluates declared policy evidence and review-age rules inspired by ISO 27001 A.5.1 | Complete policy inventory, authentic approval evidence and timing must be established outside the Pack | Not ISO 27001 certification or a complete control assessment |
| [admin-drift-detection](../packs/providers/aws/admin-drift-detection/) | Uses a supplied CloudTrail-like IAM event and change-request field; `deny` absent ticket for `AdministratorAccess` | Real event ingestion, ticket validation and CI/cloud enforcement integration must be implemented separately | Does not listen to CloudTrail or prevent an IAM API call on its own; a ticket **identifier** is not approval proof |

These six Packs have policy-fixture tests executed by the [Kernel CI](../.github/workflows/ci.yml) at the documented baseline. **The Pack schema check validates Pack definitions**, not the truth or mandatory runtime completeness of all external JSON. The generic CLI `run` does not automatically enforce the embedded `spec.inputs.schema` for all inputs. Treat missing mandatory observations as a separate pre-Kernel evidence-admission condition (see [ADR 0003](../adrs/0003-evidence-admission-before-decision-execution.md)).

## Reproduce using the **actual** CLI

From the repository root with .NET 8:

```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
dotnet run --project src/PayGod.Cli -- test --pack packs/core/critical-cve-blocker
dotnet run --project src/PayGod.Cli -- test --pack packs/core/ghg-scope-1-2-guard
dotnet run --project src/PayGod.Cli -- test --pack packs/core/iso27001-policy-review
```

The separate `validate` command checks whether an input JSON is parseable/representable under the canonical profile and computes its hash. It **does not validate a policy pack or certify domain input completeness**:

```bash
dotnet run --project src/PayGod.Cli -- validate --input example.json
```

To validate **Pack definitions**, use:

```bash
python3 -m pip install -r tools/requirements.txt
python3 tools/pack_validate.py
```

To evaluate a real Pack input, use `paygod run --pack <dir> --input <file> --out <dir>` only after domain-specific evidence admission, and distinguish the returned policy verdict from an independently authorized action. See [developer onboarding](../START_HERE.md) and [verifier boundary](STANDALONE_VERIFIER.md).

## Future use and contributions

These are **source-available Community Pack examples**, not endorsed production integrations or compliance certifications. Contributors may propose changes through [CONTRIBUTING](../CONTRIBUTING.md) under Apache-2.0; inclusion in this repository is **not** a PayGod production-accreditation, guaranteed publication in a curated catalog, compensation or royalty commitment. A future program for approved third-party production Packs, quality gates and creator benefits requires separately published governance and agreements.

The prior estimates of `$5k+` incident savings or `20–30%` FinOps savings and claims such as "ensures no exploits ship" and "meets SOC 2/ISO" were removed because no supporting performance, operational enforcement or regulatory evidence was recorded. Future hypothetical FinOps Packs are not available executable products and are intentionally omitted from the actual inventory.
