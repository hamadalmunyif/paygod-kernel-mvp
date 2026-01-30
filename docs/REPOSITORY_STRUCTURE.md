# Repository Structure & Open Core Architecture

This document explains the organization of the Paygod Kernel repository, highlighting the separation between the **Public Core** and the **Extension Points** that enable the Open Core model.

## 📂 Root Directory

```
/
├── contracts/          # 📜 Canonical JSON Schemas (The Law)
├── docs/               # 📚 Documentation & Governance
├── packs/              # 📦 Policy Bundles (Starter Packs)
├── spec/               # ⚖️ Compliance Test Vectors (Golden Fixtures)
├── src/                # 🧠 Core Kernel Source Code (.NET)
├── tools/              # 🛠️ CLI & Verification Scripts (Python)
├── LICENSE             # ⚖️ Apache 2.0 License
├── SECURITY.md         # 🛡️ Security Policy & Disclosure
├── TRADEMARK.md        # ™️ Trademark Usage Guidelines
└── CONTRIBUTING.md     # 🤝 Contribution Guidelines
```

## 🏗️ Key Components

### 1. `spec/` (The Standard)
This is the "Constitution" of the system. It defines the mathematical truth that all implementations must adhere to.
*   **`test-vectors/`**: JSON files containing "Golden Fixtures" for Canonicalization and Hashing.
*   **Role**: Ensures that a Rust CLI, a .NET Server, and a Python Script all produce the *exact same* ledger hashes.

### 2. `contracts/` (The Law)
Contains the versioned JSON Schemas that define valid data structures.
*   **`schemas/`**: `observation.schema.json`, `decision.schema.json`, etc.
*   **Role**: Enforces "Strict Mode" validation at the API boundary.

### 3. `packs/` (The Value)
Contains the "Starter Packs" that solve real business problems.
*   **`security/`**: `secrets-in-repo-guard`, `critical-cve-blocker`.
*   **`compliance/`**: `admin-drift-detection`.
*   **Role**: Drives adoption by providing immediate value ("Drop-in Security").

### 4. `src/` (The Engine)
The core execution logic, designed as a set of decoupled services.
*   **`Paygod.Contracts`**: Shared C# models generated from JSON Schemas.
*   **`Paygod.ControlEngine`**: The stateless runtime that evaluates Policy Packs.
*   **`Paygod.Ledger.Service`**: The immutable append-only log.
*   **Interfaces**: `ILedgerStore`, `IPolicySource` (The Extension Points for Enterprise).

### 5. `docs/` (The Strategy)
*   **`OPEN_CORE_POLICY.md`**: Defines the boundary between Community and Enterprise.
*   **`PUBLIC_API_POLICY.md`**: Defines the stable surface area (SemVer).
*   **`adrs/`**: Architectural Decision Records (Why we did what we did).

## 🔄 The Open Core Flow

1.  **Community User**:
    *   Downloads `paygod` CLI (built from `src/`).
    *   Uses `packs/security` to scan their repo.
    *   Stores results in a local `ledger.jsonl` file (Default `ILedgerStore`).

2.  **Enterprise User**:
    *   Uses the *same* `paygod` CLI.
    *   Configures it to use the `S3LedgerStore` (Proprietary Extension).
    *   Connects to `Paygod Cloud` for centralized dashboards.

## 🛡️ Trust & Verification
*   **`tools/verify_spec.py`**: Runs in CI to prove that the code complies with `spec/`.
*   **`tools/dev/mock/test_pack.py (NOT source of truth)`**: Runs in CI to prove that the Packs logic is correct.

This structure ensures that **Paygod Kernel** is a complete, standalone open-source product, while leaving clear, architectural "sockets" for commercial features.
