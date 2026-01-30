# Design Specification: Paygod.SchemaValidator

## 1. Overview
`Paygod.SchemaValidator` is a standalone .NET 8 CLI tool (and library) designed to serve as the **Unified Validation Engine** for the Paygod ecosystem. It enforces "Schema is Law" by strictly validating JSON data against JSON Schemas with strict format assertions.

## 2. Core Objectives
- **Strictness**: Enforce `format` keywords as assertions (e.g., email, date-time, uuid).
- **Performance**: Native AOT compilation for sub-second startup and execution.
- **Portability**: Single-file binary distribution for Linux (CI/Container) and Windows (Dev).
- **Integration**: Designed to be called by PowerShell scripts, GitHub Actions, and Docker containers.

## 3. Architecture

### 3.1 Technology Stack
- **Language**: C# (.NET 8.0)
- **Core Library**: `JsonSchema.Net` (by Greg Dennis) - chosen for compliance with Draft 2020-12.
- **CLI Framework**: `System.CommandLine` or simple `args` parsing.

### 3.2 CLI Interface

```bash
paygod-validator validate --schema <path_to_schema> --instance <path_to_data> [--output-format <text|json>]
```

#### Arguments:
- `--schema, -s`: Path to the JSON Schema file (required).
- `--instance, -i`: Path to the JSON data file to validate (required).
- `--output-format, -o`: Output format. Defaults to `text` (human readable), `json` for machine parsing.

#### Exit Codes:
- `0`: Validation Passed.
- `1`: Validation Failed (Schema violations found).
- `2`: Application Error (File not found, Invalid JSON syntax, etc.).

### 4. Functional Requirements

#### 4.1 Strict Format Validation
The tool MUST configure the underlying validation engine to treat formats as errors.

```csharp
// Configuration Concept
var options = new ValidationOptions
{
    OutputFormat = OutputFormat.Detailed,
    RequireFormatValidation = true // CRITICAL: This enables strict format checking
};
```

#### 4.2 Error Reporting
Output must be clear and actionable.

**Text Output Example:**
```text
[FAIL] Validation failed for 'user_profile.json'
Errors:
  - /contact/email: 'not-an-email' is not a valid email address.
  - /meta/uuid: Value must match format 'uuid'.
```

**JSON Output Example:**
```json
{
  "valid": false,
  "errors": [
    {
      "path": "/contact/email",
      "message": "'not-an-email' is not a valid email address",
      "keyword": "format"
    }
  ]
}
```

## 5. Implementation Plan

1. **Scaffold Project**: Create `src/Paygod.SchemaValidator` console app.
2. **Install Dependencies**: Add `JsonSchema.Net`.
3. **Implement Logic**:
   - Load Schema & Instance from file paths.
   - Configure `ValidationOptions`.
   - Execute `schema.Evaluate(instance, options)`.
   - Parse results and render output.
4. **Build & Publish**: Configure `csproj` for `PublishAot=true`.

## 6. Future Extensions
- **Remote Schemas**: Support fetching schemas from HTTP/S URLs.
- **Batch Mode**: Validate multiple files in one run for performance.
- **Watch Mode**: Re-run validation when files change (for dev experience).
