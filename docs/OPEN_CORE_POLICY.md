# Open Core Policy

This document defines the strategic boundary between the **Community Edition (Open Source)** and **Enterprise Edition (Commercial)** of Paygod.

## 🎯 Philosophy
We believe in a **"Value-Based" Open Core model**.
- **Developers** should have everything they need to run, test, and validate policies locally or in CI/CD **for free**.
- **Enterprises** pay for centralized management, advanced integrations, governance at scale, and support.

The "Kernel" is not a crippled version; it is the fully functional engine. The "Enterprise" edition is a wrapper that adds organizational capabilities.

## ⚖️ The Boundary: Open vs. Commercial

| Component Category | **Open Source (Community)** | **Commercial (Enterprise)** |
| :--- | :--- | :--- |
| **Core Engine** | **Full Kernel:** Policy evaluation logic, ledger primitives, canonicalization, and validation engine. | **Same Kernel:** The commercial product wraps the exact same binary/library. |
| **CLI Tooling** | **Full CLI:** `paygod validate`, `paygod test`, local execution. | **Enterprise CLI:** Adds commands like `paygod login`, `paygod sync`, `paygod audit-upload`. |
| **Policy Packs** | **Standard Packs:** General purpose security & compliance (e.g., CVEs, Admin Drift, Secrets). | **Premium Packs:** Industry-specific standards (PCI-DSS, HIPAA, FedRAMP) and complex vendor integrations. |
| **Connectors** | **Generic/Local:** JSON file inputs, standard input streams (STDIN), basic webhooks. | **Native Integrations:** AWS Org Sync, Azure AD, Okta, Jira, ServiceNow, Splunk forwarders. |
| **Data & Storage** | **Local/Ephemeral:** Local file system, ephemeral in-memory validation. | **Persistent/SaaS:** Long-term ledger storage, historical trending, team-based access control (RBAC). |
| **User Interface** | **None:** CLI and text-based outputs only. | **Management Dashboard:** Web UI for visualization, reporting, user management, and audit trails. |

## 🛡️ Protection Mechanisms
To ensure the commercial value is protected while maintaining a healthy open source ecosystem:

1.  **License Separation:**
    *   **Kernel:** Apache 2.0 (Permissive).
    *   **Enterprise Modules:** Proprietary Commercial License.
2.  **Repository Isolation:**
    *   Proprietary code resides in a separate, private repository.
    *   It imports the Kernel as a dependency, ensuring no "leakage" of commercial IP into the public codebase.
3.  **Trademark Enforcement:**
    *   The name "Paygod" and the Logo are trademarks.
    *   Forks cannot use the official branding to sell a competing hosted service.

## 🤝 Contribution Guidelines
*   Contributions to the **Kernel** are welcome and remain open source forever.
*   We do not accept "Enterprise-only" features into the Kernel repo (e.g., code that strictly relies on a closed-source backend).
*   All checks and balances (hashing, signatures) in the Kernel are transparent to guarantee trust.
