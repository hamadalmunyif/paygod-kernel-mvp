# ADR 0001: Canonical Kernel Records & Schema Validation

## Status
Accepted

## Context
Paygod Kernel requires a mechanism to validate data integrity across multiple boundaries (API ingress, internal messaging, ledger storage). The system must guarantee that invalid data is rejected before it can cause side effects or pollute the immutable ledger.

Previously, validation was performed via ad-hoc logic in PowerShell scripts and C# classes. This led to:
1. **Inconsistency**: Validation rules in the API differed from those in the Ledger.
2. **Shadow Validation**: Rules existed in code but not in documentation.
3. **Maintenance Burden**: Every schema change required manual code updates in multiple places.

## Decision
We will adopt **JSON Schema (Draft 2020-12)** as the single source of truth for all data contracts.

The Canonical Record Types defined are:
- `Observation`: Raw input data.
- `MetricSpec`: Definition of how to measure data.
- `Measurement`: The quantified result.
- `Decision`: The final judgment.
- `Evidence`: The bundle of inputs used.
- `Impact`: The consequence/action to take.
- `LedgerEntry`: The sealed record.

Furthermore, we will enforce a **Strict Validation Policy**:
1. **Formats are Assertions**: All `format` keywords (e.g., `email`, `uuid`) must be validated strictly.
2. **No Unknown Keywords**: Schemas must not contain unrecognized keywords (to prevent typos).
3. **Unified Engine**: A single .NET-based CLI tool (`Paygod.SchemaValidator`) will be used across all environments (Local, CI, Production) to perform validation.

## Consequences

### Positive
- **Guaranteed Consistency**: The same validation logic runs everywhere.
- **Contract-First Development**: Developers must define the schema before writing code.
- **Automated Documentation**: API documentation can be auto-generated from the schemas.
- **Reduced Liability**: Strict format validation prevents common data integrity issues (e.g., invalid emails).

### Negative
- **Initial Friction**: Developers must learn JSON Schema syntax.
- **Rigidity**: "Quick fixes" to validation logic now require a formal schema update and release.
- **Performance Overhead**: Parsing and validating against full schemas is computationally more expensive than simple `if` checks (though mitigated by Native AOT compilation).

## Compliance
This decision supports **Axiom 1: Schema Is Law**.

## References
- [SCHEMA_SEMVER_POLICY.md](../../contracts/versioning/SCHEMA_SEMVER_POLICY.md)
- [PAYGOD_VALIDATOR_SPEC.md](../design_specs/PAYGOD_VALIDATOR_SPEC.md)
