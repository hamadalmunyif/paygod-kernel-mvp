# Paygod Kernel Architecture

## 1. Context & Problem Statement

Paygod Kernel is the high-assurance execution engine designed to bridge the gap between **Decision Intelligence** (provided by DAA) and **Financial Compliance/Execution**.

In modern fintech and regulatory environments, "deciding" what to do and "executing" that decision compliantly are distinct challenges. Existing systems often couple these tightly, leading to "Spaghetti Code" where business logic, compliance checks, and execution scripts are inextricably mixed. This makes audits difficult and changes risky.

**Paygod Kernel solves this by:**
1. Decoupling the **Decision** (Policy/Logic) from the **Execution** (Mechanism).
2. Enforcing a strict, immutable **Ledger** of all actions.
3. Treating **Compliance** as code (OSCAL) rather than manual checklists.

## 2. Goals & Non-Goals

### Goals
- **Auditability**: Every state change is cryptographically verifiable.
- **Modularity**: New Decision Packs (DAA) can be plugged in without recompiling the Kernel.
- **Resilience**: The system fails safely and recovers automatically.
- **Strictness**: Invalid data is rejected at the boundary; no "garbage in, garbage out".
- **Extensibility**: Support both Community (local) and Enterprise (SaaS) deployments via the same core.

### Non-Goals
- **General Purpose CMS**: This is not a generic content management system.
- **Real-time Trading**: While fast, the Kernel prioritizes consistency and correctness over microsecond-level latency required for HFT.

## 3. System Decomposition

The architecture follows a **Microservices** pattern centered around a shared immutable Ledger, designed for the **Open Core** model.

### 3.1 Core Services (Open Kernel)
1. **Ingress Gateway (API)**:
   - Authenticates requests (mTLS/JWT).
   - Validates input schemas (Strict Mode).
   - Routes to appropriate internal services.
   
2. **Decision Runtime (DAA Host)**:
   - Loads and executes Decision Packs.
   - Stateless execution engine.
   - Inputs: `Context` + `Pack`. Outputs: `Decision` + `Evidence`.

3. **Ledger Service**:
   - The "Write-Only" heart of the system.
   - Appends cryptographically chained records.
   - Provides "Time Travel" queries (State at Time T).

4. **Executor Service**:
   - Listens to Ledger events (e.g., `DecisionFinalized`).
   - Performs side effects (e.g., Send Money, Update KYC Status).
   - Idempotent design.

### 3.2 Extension Points (Interfaces)
To support the Open Core model (ADR-0006), the Kernel exposes interfaces that can be swapped at runtime:

| Interface | Community Implementation (Default) | Enterprise Implementation (Proprietary) |
| :--- | :--- | :--- |
| `ILedgerStore` | **LocalFileSystem**: Appends to `ledger.jsonl` on disk. | **S3/BlobStore**: Appends to immutable object storage with WORM locking. |
| `IPolicySource` | **LocalDirectory**: Loads YAML packs from `/packs` folder. | **GitOps/DB**: Loads packs from managed Git repo or Policy Registry. |
| `IAuthProvider` | **StaticToken**: Simple API Key or Local User. | **OIDC/SAML**: Integration with Okta, Azure AD, Keycloak. |
| `IAuditSink` | **Console/File**: Logs to STDOUT or file. | **Splunk/Datadog**: Forwards structured logs to SIEM. |
| `IPanicSwitch` | **LocalFileFlag**: Checks a local lock file. | **GlobalRedisKey**: Checks a distributed Redis key for instant cluster-wide freeze. |

### 3.3 Boundaries
- **Public Boundary**: The Ingress Gateway is the only component exposed to the internet/public network.
- **Trust Boundary**: Services inside the mesh trust each other's identity (via mTLS) but strictly validate each other's data payloads.

## 4. Deployment Modes

### Mode A: Standalone (Community Default)
Optimized for developer experience and local testing.
- **Single Process**: All services run within one binary or a minimal `docker-compose`.
- **Zero Dependencies**: Uses SQLite and local files. No external DB or Cache required.
- **Goal**: `docker run paygod/kernel` just works in < 5 seconds.

### Mode B: Distributed (Enterprise Scale)
Optimized for high availability and compliance.
- **Microservices**: Services deployed as separate K8s pods.
- **External State**: Uses Postgres/RDS, Redis, and S3.
- **Goal**: 99.99% SLA, Zero-Trust security mesh.

## 5. Key Flows

### The "Observation → Measurement → Impact → Evidence → Ledger" Loop

1. **Observation**: The system ingests raw data (e.g., User Form, Credit Report).
2. **Measurement**: DAA Packs quantify this data against criteria (e.g., Risk Score = 85/100).
3. **Impact**: The system determines the consequence (e.g., "High Risk" -> "Manual Review Required").
4. **Evidence**: All inputs and intermediate scores are bundled as a verifiable evidence package.
5. **Ledger**: The final Decision Record (with Evidence hash) is sealed in the Ledger.

## 6. Trust Boundaries & Security Model

### 6.1 Zero-Trust Assumptions
- The internal network is considered hostile.
- No service trusts another based on IP address.
- All secrets (DB connection strings, API keys) are injected at runtime via Vault/Secrets Manager, never stored in code.

### 6.2 PII & Data Privacy
- **PII Zone**: User profile data is stored in a segregated `IdentityService`.
- **Anonymization**: The Ledger stores references (UUIDs) to users, not PII itself, wherever possible.
- **Secrets**: Strictly forbidden in the Ledger.

## 7. Operational Model

### 7.1 SLOs (Service Level Objectives)
- **Availability**: 99.9% (allows ~43m downtime/month).
- **Latency**: 95% of Decision requests < 500ms.
- **Durability**: 99.9999999% (11 9s) for Ledger data.

### 7.2 Failure Modes
- **Ledger Down**: System enters "Read-Only" mode. No new decisions can be finalized.
- **DAA Service Down**: Requests queue up or fail fast (depending on priority).
- **Validation Failure**: Request rejected immediately with 400 Bad Request (protects system integrity).

### 7.3 Kill-Switch (Panic Mode)
- **Function**: Instantly freezes all Executor side-effects (e.g., stop money movement) while allowing Read/Decision operations.
- **Implementation**: Defined via `IPanicSwitch` interface.
    - **Community**: Toggled via a local file or CLI command.
    - **Enterprise**: Toggled via API/UI, propagated globally via Redis/Consul.

## 8. Decision Links (ADRs)

- [ADR-001: Use JSON Schema for Contracts](../docs/adr/ADR-001-json-schema.md)
- [ADR-002: Immutable Ledger Strategy](../docs/adr/ADR-002-ledger-append-only.md)
- [ADR-003: .NET for Kernel / Python for Data Science](../docs/adr/ADR-003-tech-stack.md)
- [ADR-005: Unified CLI Validator](../docs/adrs/0005-unified-cli-validator.md)
- [ADR-006: Repository Separation Strategy](../docs/adrs/0006-repository-separation-strategy.md)
