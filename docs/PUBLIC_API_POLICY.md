# Public API Policy

This document defines the **Public Surface Area** of the Paygod Kernel. These are the contracts we guarantee to be stable according to Semantic Versioning (SemVer).

## 🎯 Scope of Stability
The "Public API" consists of:

### 1. Canonical Formats (Strict)
To ensure identical behavior across languages (Rust/Go/.NET), we mandate:

*   **Canonical JSON:** MUST adhere to **[RFC 8785 (JCS)](https://tools.ietf.org/html/rfc8785)**.
    *   Keys MUST be sorted lexicographically.
    *   Whitespace MUST be removed (compact).
    *   Numbers MUST be formatted as per IEEE 754 (e.g., `1e+2` becomes `100`).
*   **Encoding:** UTF-8 **without BOM**.
*   **Hashing:**
    *   Algorithm: **SHA-256**.
    *   Input: The UTF-8 bytes of the Canonical JSON string.
    *   Output Format: **Hexadecimal (lowercase)**, e.g., `sha256:e3b0c442...` (prefix optional in internal storage, mandatory in public references).

### 2. CLI Contract
The `paygod` binary guarantees the following interface:

*   **Exit Codes:**
    *   `0`: Success (Valid/Pass).
    *   `1`: Validation Failure (Deny/Error).
    *   `2`: System/Internal Error.
*   **Output Format:**
    *   When `--json` is passed, the output MUST be a valid JSON object adhering to the `CliResponse` schema:
        ```json
        {
          "status": "success|failure|error",
          "code": 0,
          "data": { ... },
          "errors": [ { "message": "..." } ]
        }
        ```

### 3. Interfaces (`src/Core/Interfaces/`)
*   `ILedgerStore`: Contract for appending and reading ledger records.
*   `IPolicySource`: Contract for loading and resolving policy packs.
*   `IAuthProvider`: Contract for identity resolution.
*   `IAuditSink`: Contract for emitting audit events.

### 4. Schemas (`contracts/schemas/`)
*   All JSON Schemas in this directory are versioned.
*   Breaking changes to schemas require a Major version bump.

## 🚫 Excluded (Internal API)
Everything else is considered internal and may change at any time without a major version bump:
*   Internal helper classes and utility functions.
*   Database schema of the local SQLite store (implementation detail).
*   In-memory data structures not exposed via interfaces.

## 🔄 Versioning Rules (SemVer)
We follow [Semantic Versioning 2.0.0](https://semver.org/):

*   **Major (X.y.z)**: Breaking changes to any Public API listed above.
*   **Minor (x.Y.z)**: New features (e.g., new interface method with default implementation, new CLI flag) that are backward compatible.
*   **Patch (x.y.Z)**: Bug fixes that do not change the Public API signature.

## ⚠️ Breaking Change Policy
If we must break a Public API:
1.  **Deprecation Notice**: We will mark the feature as `@deprecated` in a Minor release.
2.  **Migration Guide**: We will provide a document explaining how to upgrade.
3.  **Grace Period**: We will support the deprecated feature for at least one minor release cycle before removal.
