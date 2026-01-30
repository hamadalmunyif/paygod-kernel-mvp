# Schema Semantic Versioning & Validation Policy

This document defines the governing rules for schema versioning, validation strictness, and compatibility guarantees for the Decision Assessment Assistant (DAA) ecosystem and Paygod Kernel integration.

## 1. Schema Versioning (SemVer)

We adhere to [Semantic Versioning 2.0.0](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible changes (e.g., removing a required field, changing a data type).
- **MINOR**: Backward-compatible additions (e.g., adding an optional field).
- **PATCH**: Backward-compatible bug fixes (e.g., correcting a description, adding an example).

### 1.1 Compatibility Guarantees
- **Forward Compatibility**: Old consumers MUST be able to read new Minor/Patch schemas (ignoring unknown fields).
- **Backward Compatibility**: New consumers MUST be able to read old Minor/Patch data.

## 2. Validation Strictness Policy

To ensure compliance and reliability in financial/regulatory contexts (Paygod Kernel), we enforce a **Strict Validation** policy that exceeds standard JSON Schema defaults.

### 2.1 Format Assertions
> **CRITICAL POLICY**: All `format` keywords defined in schemas (e.g., `email`, `uuid`, `date-time`, `uri`) are **ASSERTIONS**, not just annotations.

- **Requirement**: All validators used in CI/CD, Runtime, and Ledger MUST be configured to fail validation if a `format` check fails.
- **Rationale**: In a compliance system, an invalid email string or malformed UUID is a data integrity violation, not a stylistic preference.
- **Implementation**:
  - **.NET**: `JsonSchema.Net` must be configured with `ValidationOptions.RequireFormatValidation = true`.
  - **Node/Other**: Validators (like `ajv`) must be instantiated with `{ format: true }` or equivalent strict mode.

### 2.2 Unknown Keywords
- **Policy**: Unknown keywords in schema definitions are **FORBIDDEN**.
- **Rationale**: Prevents typos in schema authoring (e.g., writing `descripton` instead of `description`).

### 2.3 Additional Properties
- **Policy**: `additionalProperties` should generally be `false` for core data structures to prevent "Shadow Data" (data that exists but isn't validated).

## 3. Deprecation Strategy

- Fields scheduled for removal MUST be marked with `deprecated: true` in a MINOR release.
- Removal can ONLY occur in the next MAJOR release.
- A migration script or guide MUST be provided for MAJOR transitions.

## 4. Source of Truth

- The JSON Schema files in this repository are the **Single Source of Truth**.
- No validation logic should exist in code (e.g., PowerShell scripts, C# classes) that is not derived from or strictly enforcing these schemas.
