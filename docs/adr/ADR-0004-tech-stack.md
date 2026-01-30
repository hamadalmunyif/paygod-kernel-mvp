# ADR 0004: Technology Stack Selection (.NET & Python)

## Status
Accepted

## Context
Paygod Kernel requires high performance, strict typing, and enterprise-grade tooling for its core execution engine. However, the DAA (Decision Assessment Assistant) relies on advanced AI/ML capabilities where Python is the dominant ecosystem.

We need to select a technology stack that leverages the strengths of both worlds without introducing excessive complexity.

## Decision
We will adopt a **Hybrid Polyglot Architecture**:

1. **Core Kernel (.NET 8+)**:
   - **Role**: API Gateway, Ledger Management, Validation, Execution.
   - **Why**: Strong typing, high performance (JIT/AOT), mature enterprise ecosystem, excellent support for microservices.
   
2. **DAA Engine (Python 3.11+)**:
   - **Role**: Data Science, LLM Integration, Complex Decision Logic.
   - **Why**: Unrivaled library support (Pandas, PyTorch, LangChain), standard for AI workloads.

3. **Communication**:
   - Services communicate via **gRPC** (internal high-performance) or **REST/JSON** (external/public).
   - Strict JSON Schema contracts define the interface between .NET and Python components.

## Consequences

### Positive
- **Best Tool for Job**: .NET provides safety and speed for the "plumbing"; Python provides flexibility and power for the "brains".
- **Talent Pool**: We can hire specialized .NET engineers for platform work and Data Scientists for decision logic.
- **Scalability**: Components can be scaled independently (e.g., scale DAA workers on GPU nodes, Kernel on CPU nodes).

### Negative
- **Operational Complexity**: Deployment pipeline must support two different runtimes.
- **Context Switching**: Developers working across the full stack must know two languages.
- **Serialization Overhead**: Data must be serialized/deserialized when crossing the language boundary.

## Compliance
This decision supports **Axiom 3: Zero-Trust Execution** (by enforcing strict contracts between components).

## References
- [PAYGOD_VALIDATOR_SPEC.md](../design_specs/PAYGOD_VALIDATOR_SPEC.md)
