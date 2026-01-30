# ADR 0006: Repository Separation Strategy (Open Core)

## Status
Accepted

## Context
We are adopting an **Open Core** business model. This requires a technical architecture that allows us to develop a public, open-source "Kernel" while simultaneously building proprietary "Enterprise" extensions. We need a strategy to manage codebases, dependencies, and build pipelines without leaking commercial IP or crippling the open-source project.

## Decision
We will use a **Multi-Repository Strategy** with strict dependency direction.

### 1. Repository Structure
*   **`paygod/kernel` (Public):** The source of truth for the core engine. Contains:
    *   Core Logic (.NET/Rust)
    *   Public CLI (`paygod`)
    *   Public Schemas & Contracts
    *   Community Packs
    *   Open Documentation
*   **`paygod/enterprise` (Private):** The commercial product. Contains:
    *   Management Dashboard (UI/Frontend)
    *   SaaS Infrastructure (IaC)
    *   Enterprise Connectors (AWS/Azure Integrations)
    *   Multi-tenant API Services
    *   Proprietary License Manager

### 2. Dependency Flow
**Direction:** `Enterprise` depends on `Kernel`. **NEVER** the reverse.

*   The `Kernel` builds and publishes versioned artifacts (Nuget packages, Rust Crates, Docker Images).
*   The `Enterprise` repo consumes these artifacts as standard dependencies.
*   **Extension Points:** The Kernel exposes clean Interfaces/Traits (e.g., `ILedgerStore`, `IPolicySource`) that the Enterprise version implements to inject advanced capabilities (e.g., replacing a local file store with a centralized database).

### 3. Build & Release
*   **Kernel Release:** Triggers a public GitHub Release + Package Registry upload.
*   **Enterprise Release:** Triggers a private build that pulls the latest stable Kernel package, wraps it with proprietary modules, and deploys to the SaaS environment.

## Consequences

### Positive
*   **Security:** Impossible to accidentally commit proprietary code to the public repo.
*   **Clarity:** Clear separation of concerns. Open source contributors are not confused by "stubbed" or "locked" features.
*   **Licensing:** Clean boundary. Apache 2.0 applies to everything in `kernel`. Commercial license applies to everything in `enterprise`.

### Negative
*   **Complexity:** Requires managing two CI/CD pipelines and synchronizing versions.
*   **Refactoring Friction:** Changing a core interface in `kernel` requires a coordinated update in `enterprise`.

## Compliance
To ensure this strategy works:
1.  **No "If Enterprise" flags in Kernel:** The Kernel code must not contain logic like `if (isEnterprise)`. Instead, it should use dependency injection or plugin interfaces.
2.  **Public API First:** Any feature needed by Enterprise must be exposed via a public API/Interface in the Kernel.
