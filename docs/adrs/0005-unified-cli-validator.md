# ADR 0005: Unified CLI Validator

## Status
Accepted

## Context
Currently, Paygod Kernel relies on a mix of PowerShell scripts (`pwsh/`) and Python tools (`tools/`) for validation, testing, and automation. This fragmentation leads to:
1. **Inconsistent Logic:** Validation rules might differ slightly between languages.
2. **Deployment Friction:** Users need multiple runtimes (PowerShell Core, Python 3.x) installed.
3. **Performance:** Interpreted scripts are slower for high-volume validation in CI pipelines.
4. **Developer Experience:** Contributors have to learn multiple toolchains.

## Decision
We will consolidate all client-side validation, testing, and interaction logic into a **single, unified CLI binary**.

### Technology Choice
- **Language:** Rust or .NET (AOT compiled).
- **Target:** Single static binary (`paygod`) with no external dependencies.
- **Scope:**
  - `paygod validate`: Schema and policy validation.
  - `paygod test`: Run pack tests (replacing `test_pack.py`).
  - `paygod build`: Package policies into distribution artifacts.

## Consequences

### Positive
- **Zero Dependency:** Users just download one binary. No `pip install` or `Install-Module`.
- **Speed:** Native performance for JSON parsing and policy evaluation.
- **Consistency:** One codebase ensures validation logic is identical everywhere.

### Negative
- **Migration Effort:** Existing scripts need to be rewritten.
- **Learning Curve:** Contributors may need to learn Rust/.NET if they are only familiar with Python/PowerShell.

## Implementation Plan
1. Define CLI specs in `docs/PAYGOD_VALIDATOR_SPEC.md` (Done).
2. Build MVP validator replacing `test_pack.py`.
3. Deprecate `pwsh/` and `tools/` in favor of the new CLI.
