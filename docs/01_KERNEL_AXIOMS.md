# Paygod Kernel Axioms

This document defines the fundamental, non-negotiable truths (Axioms) that govern the design and operation of the Paygod Kernel. These are not merely guidelines; they are architectural constraints that must be upheld to ensure the system's integrity, security, and compliance.

Each axiom is structured to provide clarity on its definition, rationale, enforcement, and tradeoffs.

---

## Axiom 1: Schema Is Law

### 1. What
The JSON Schema definitions are the absolute and final authority on data validity. No code shall implement validation logic that contradicts or extends the schema without the schema itself being updated first.

### 2. Why
To prevent "Shadow Validation" where the actual rules of the system diverge from the documented contract. This ensures that validation is consistent across all environments (Local, CI, Production) and languages.

### 3. Counterexample
A developer adds a check `if ($obj.amount > 1000)` in a PowerShell script but leaves the schema's `maximum` value as `undefined`. A third-party integrator validates against the schema, sends `2000`, and fails mysteriously in production. The contract was lied to.

### 4. Enforcement
- **CI Gate**: All PRs must pass `paygod-cli validate --schema` which strictly enforces the schema.
- **Library**: The `Paygod.SchemaValidator` library is the only approved validation mechanism in the kernel code.
- **Policy**: `SCHEMA_SEMVER_POLICY.md` mandates strict format assertions.

### 5. Tradeoffs
- **Rigidity**: Changing a rule requires a schema change and potentially a version bump, which is slower than "hot-patching" a script.
- **Learning Curve**: Developers must learn JSON Schema vocabulary instead of writing ad-hoc `if` statements.

### 6. Non-goals
- Does not replace business logic validation that requires external state (e.g., "User has sufficient balance"). Schema validates the *shape* and *intrinsic* correctness of the message, not its *contextual* validity.

### 7. References
- [SCHEMA_SEMVER_POLICY.md](../contracts/versioning/SCHEMA_SEMVER_POLICY.md)
- [JSON Schema Validation Spec (Draft 2020-12)](https://json-schema.org/specification.html)

---

## Axiom 2: Ledger Immutability

### 1. What
Once a decision or assessment is recorded in the Ledger, it can never be modified or deleted. Corrections are made only by appending new "Correction" records that reference the original.

### 2. Why
To guarantee a tamper-evident audit trail that satisfies strict financial and regulatory compliance requirements (OSCAL, SOC2). Trust is built on the assurance that history cannot be rewritten.

### 3. Counterexample
An admin notices a typo in a risk assessment and runs a SQL `UPDATE` to fix it. The audit trail is broken; auditors can no longer verify what the state was at the time of the original decision, potentially hiding fraud or incompetence.

### 4. Enforcement
- **Cryptographic Chaining**: Each ledger entry contains a hash of the previous entry.
- **WORM Storage**: Underlying storage media (e.g., S3 Object Lock, Append-only DB) is configured to Write-Once-Read-Many.
- **API Constraints**: The Kernel API exposes no `PUT` or `DELETE` endpoints for ledger resources.

### 5. Tradeoffs
- **Storage Growth**: The database grows indefinitely.
- **Complexity**: "Reading" the current state requires replaying the history or maintaining a separate "State View" (CQRS pattern).

### 6. Non-goals
- Does not apply to ephemeral data like user session caches or draft assessments that haven't been finalized.

### 7. References
- [NIST SP 800-53 (AU-9 Protection of Audit Information)](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

---

## Axiom 3: Zero-Trust Execution

### 1. What
The Kernel assumes that no caller, internal or external, is implicitly trusted. Every request must carry verifiable cryptographic proof of identity and authorization (e.g., a signed token).

### 2. Why
Perimeter defense is insufficient for modern cloud-native architectures. If an attacker breaches the outer firewall, they should not have free reign over the internal microservices.

### 3. Counterexample
The `DecisionService` trusts any request coming from `localhost` or the internal subnet. An attacker gains shell access to a web server in the same subnet and can now issue fraudulent decisions without authentication.

### 4. Enforcement
- **mTLS**: Mutual TLS is required for all service-to-service communication.
- **Token Validation**: Every endpoint validates the JWT signature, expiration, and scopes before processing.
- **Identity Propagation**: User identity is propagated through the call chain; services do not act as "God Mode" superusers.

### 5. Tradeoffs
- **Latency**: Additional overhead for cryptographic handshakes and token validation on every hop.
- **Management**: Requires robust PKI and Key Management infrastructure.

### 6. Non-goals
- Does not imply that we don't use firewalls. Network segmentation is still a valid defense-in-depth layer, just not the *only* one.

### 7. References
- [NIST SP 800-207 (Zero Trust Architecture)](https://csrc.nist.gov/publications/detail/sp/800-207/final)

---

## Axiom 4: Evidence-Based Decisions

### 1. What
Every decision output by the DAA/Paygod system must be traceable back to specific input evidence (data points, user answers, external API responses). A decision cannot exist in a vacuum.

### 2. Why
To explain *why* a decision was made (Explainable AI / XAI) and to allow for auditing the quality of decisions. "Because the AI said so" is not an acceptable justification in financial compliance.

### 3. Counterexample
A loan application is rejected. The system logs "Rejected" but doesn't link it to the specific credit bureau report or the specific policy rule that triggered the rejection. Debugging or appealing the decision is impossible.

### 4. Enforcement
- **Data Model**: The `DecisionRecord` schema requires an `evidence` array containing references (IDs/Hashes) to all inputs used.
- **Provenance**: Input data is stored with metadata about its source and timestamp.

### 5. Tradeoffs
- **Data Volume**: Storing full evidence chains increases storage requirements.
- **Privacy**: Evidence may contain PII, requiring strict access controls and potentially redaction strategies for long-term storage.

### 6. Non-goals
- Does not require storing a full snapshot of the *entire world* state, only the specific inputs that influenced the calculation.

### 7. References
- [EU AI Act (Transparency and Record-Keeping)](https://artificialintelligenceact.eu/)
