# DAA Integration Profile: Decoupled Decision Intelligence

## 1. Overview
This profile defines the integration strategy between **Paygod Kernel** (the Execution Engine) and **Decision Assessment Assistant (DAA)** (the Intelligence Engine).

**Strategic Principle**: The two systems are **strictly decoupled**. DAA acts as an untrusted external advisor ("Oracle"), while Paygod Kernel retains absolute sovereignty over execution and compliance.

## 2. Integration Pattern: The "Advisor-Judge" Model

We employ an asynchronous, message-based integration pattern where DAA provides *recommendations*, but Paygod Kernel makes *decisions*.

| Feature | DAA (The Advisor) | Paygod Kernel (The Judge) |
| :--- | :--- | :--- |
| **Role** | Analyze data, calculate scores, suggest actions. | Validate inputs, enforce policy, execute transactions. |
| **Nature** | Probabilistic (AI/ML), fast-changing. | Deterministic (Rule-based), stable. |
| **Output** | `Assessment` (Opinion) | `Decision` (Law) |
| **Failure Mode** | Hallucination, Timeout. | Rejection, Safe Fallback. |

## 3. Communication Protocol

### 3.1 Data Flow
1. **Request**: Paygod sends an anonymized `ObservationContext` to DAA.
2. **Analysis**: DAA runs the appropriate Pack (e.g., Credit Risk Pack).
3. **Response**: DAA returns a signed `AssessmentResult`.
4. **Validation**: Paygod validates the signature and schema of the result.
5. **Judgment**: Paygod compares the result against `Guardrails` (Policy).
6. **Execution**: If passed, Paygod creates a `DecisionRecord` and executes.

### 3.2 The "Air Gap" Logic
To prevent AI risks from contaminating the financial core:
- **No Direct DB Access**: DAA never touches the Paygod Ledger directly.
- **No Side Effects**: DAA cannot call external APIs (e.g., Stripe) directly. It can only return a JSON saying "I recommend paying X".
- **Strict Schema**: DAA's output must match the `Measurement` schema exactly. Any extra fields or hallucinations are stripped/rejected.

## 4. Guardrails & Safety

Paygod Kernel implements a **Defense-in-Depth** layer specifically for DAA integration:

### 4.1 Schema Sanitization
The Kernel's Ingress Gateway strips any unrecognized fields from DAA responses. If DAA hallucinates a field `"confidence_level": "very high"`, it is discarded unless defined in the strict schema.

### 4.2 Threshold Policies
Paygod defines "Hard Limits" that override DAA:
- *Example*: "If DAA recommends a loan > $50,000, force Manual Review regardless of the AI score."

### 4.3 Circuit Breakers
If DAA error rates or latency spike, Paygod automatically switches to a "Fallback Strategy" (e.g., Rule-based logic or Manual Queue) to maintain business continuity.

## 5. Deployment Lifecycle

Because the systems are decoupled, they have independent lifecycles:

- **DAA Packs**: Can be updated daily (e.g., new fraud patterns). Deployed to DAA Runtime.
- **Paygod Kernel**: Updated quarterly (e.g., regulatory changes). Deployed to Secure Enclave.

## 6. Compliance Mapping
This profile satisfies **OSCAL** controls for external system reliance:
- **SA-9 (External System Services)**: Defines trust boundaries.
- **SI-10 (Information Input Validation)**: Strict schema enforcement on DAA outputs.

## 7. References
- [Axiom 3: Zero-Trust Execution](./01_KERNEL_AXIOMS.md)
- [ADR 0004: Hybrid Tech Stack](./adr/ADR-0004-tech-stack.md)
