# Core Pack Production Readiness — Evidence Register

Status: **2026-10-10 baseline; NONE marked PRODUCTION READY.**  
Purpose: separate an executable community pack, its declared policy-unit cases, an independently admissible input, and a fully operated production workflow. This file is **not** a release certificate or a standards-accreditation finding.

| Core Pack | Existing code/test basis | Observed gap at current public entrypoints | Next falsifiable gate | Current label |
|---|---|---|---|---|
| [GHG Scope 1 & 2](../../packs/core/ghg-scope-1-2-guard/) | Real `pack.yaml`, 3 policy cases (deny/flag/allow) | `run` does not enforce the embedded input schema; no physical-data source/factor authentication; fractional readings unsupported without admitted representation | Opt-in candidate negative admission tests + synthetic delegated canonical CLI bundle verifier, then real/deidentified source and independent recipient | **IMPLEMENTED PACK; ADMISSION RESEARCH ONLY** |
| [Critical CVE](../../packs/core/critical-cve-blocker/) | Real `pack.yaml`, 3 policy cases (deny/flag/allow) | Missing/non-array `vulnerabilities` can produce an apparently clean result via `not any`; real scanner success/completeness not authenticated | Freeze negative test for absent/malformed scan result; enforce scanner completeness and provenance at admission before permitting a release | **IMPLEMENTED PACK; NOT PRODUCTION READY** |
| [ISO 27001 Policy Review](../../packs/core/iso27001-policy-review/) | Real `pack.yaml`, 4 policy cases (deny overdue/no evidence, flag near due, allow) | Approval role is an assertion, time since review is computed externally, and schema is not enforced by generic `run`; policy check is not ISO certification | Freeze missing/malformed/empty-policy and invalid approval semantics; independent signoff on evidence format and reference meaning | **IMPLEMENTED PACK; NOT PRODUCTION READY** |

## Shared finding: validation is not implementation

The Pack Contract CI gate checks **the `pack.yaml` definition** against the versioned contract. The `test --pack` command checks declared examples using the policy evaluator. Neither gate establishes that `run` validates every live input against `spec.inputs.schema`; inspect [`RunCommand`](../../src/PayGod.Cli/Commands/RunCommand.cs) and [`TestCommand`](../../src/PayGod.Cli/Commands/TestCommand.cs).

The operational problem is **input admission**, with domain-specific evidence completeness. Do not silently redefine boolean Kernel semantics or versioned receipts to make new domains appear production-ready. The kernel can evaluate *admitted* facts; the party collecting them must prove admissibility separately under [ADR 0003](../../adrs/0003-evidence-admission-before-decision-execution.md).

## No silent promotion

- `Pack exists` does not mean `all inputs accepted safely`.
- `test cases pass` does not mean `the actual data source is trustworthy`.
- `ALLOW` is a pack result, not an environmental, security or ISO certificate.
- `portable bundle VALID` means scoped integrity only, not independent physical measurement or execution authorization.
- `WITHHELD` / `NOT RUN` remain pre-kernel orchestration states.

## Next evidence order

1. Freeze and test the first **GHG** candidate admission path in [ghg-scope12-v0](ghg-scope12-v0/README.md) without modifying the Kernel.
2. Verify exact synthetic delegated CLI output and independent verifier in CI.
3. Capture one real/de-identified measurement and independently pinned evidence references with declared units and factor source; no arbitrary schema relaxations.
4. Show a recipient can interpret the same profile with an independently run verifier.
5. Only then consider enforcing the pattern at each actual entrypoint after explicit Stop-Build review and a versioned decision.
6. Apply the same falsification method to **CVE** and **ISO** separately; don't treat GHG passing as universal production assurance.

## Website publication boundary

Site Use Cases may reference these **three real existing packs** as examples of reusable Kernel decision policy. They must not advertise production-ready measurement, enterprise enforcement, ISO accreditation, a verified security scanner integration, or direct source authenticity. The canonical public technical repo is **only** [paygod-kernel-mvp](https://github.com/hamadalmunyif/paygod-kernel-mvp).
