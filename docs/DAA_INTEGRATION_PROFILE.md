# Advisor–Judge Pattern — Research Profile

Status: **DESIGN PATTERN / NOT AN IMPLEMENTED DAA RUNTIME** (2026-10-10).

This file corrects the earlier description that called the Kernel a transaction execution engine and claimed a deployed DAA gateway, circuit breakers, schema-stripping behavior, secure enclaves and OSCAL compliance. Those features are **not established by the current repository**. The canonical description is in [README](../README.md) and [Architecture](02_ARCHITECTURE.md).

## Motivation

External AI, models, heuristics, and institutional advisers may provide recommendations. Their output is evidence **to admit or reject**, not a trusted instruction. The deterministic Kernel may evaluate admitted, schema-compatible inputs against a policy pack, producing a decision and portable artifacts. Only a separately authorized downstream system can act.

```text
Untrusted adviser (AI or other)
       |
       | proposal + claimed source / context
       v
External evidence admission
       | missing/unrepresentable -> WITHHELD -> NOT RUN
       | represented/accepted -> complete canonical input
       v
Canonical Kernel (policy decision; portable artifacts)
       |
       v
Independent evidence verifier (scoped checks)
       |
       v
Relying party / independently authorized enforcer
```

## Separation rules

1. Adviser output does not carry its own authority merely because it is signed or machine readable.
2. Admission must establish field representability and relevant provenance rules; do not convert missing evidence to `false`. [ADR 0003](../adrs/0003-evidence-admission-before-decision-execution.md) governs the current pre-kernel boundary.
3. The Kernel's deterministic result is **not** a law or regulator verdict. `ALLOW` is a policy-pack result within the evaluated contract.
4. The Kernel does not sign, submit, settle or execute the downstream transaction as an intrinsic primitive.
5. The verifier is not the Kernel, and its valid integrity result does not prove external source truth or delegated execution authority.
6. Any production adviser integration would need independently tested ingress, security, reliability and operational requirements. Those are not present here by the existence of this file.

## Implementation status

| Capability | Current status |
|---|---|
| Canonical deterministic policy and portable evidence | Implemented within Kernel witness scope |
| Pre-kernel `WITHHELD` and `NOT RUN` | Accepted admission architecture; not a Kernel tri-state |
| Generic DAA service, live LLM gateway or message bus | Not implemented here |
| Automatic threshold override, fallback circuit-breaker and monitoring | Design possibilities only |
| Transaction execution, enterprise key isolation, OSCAL certification | Not implemented or certified |
| Agent-specific decision-to-Warrant portable authority | Remains experiment/research outside Kernel |

## Open questions (not decisions)

How to represent untrusted advice, whose key/capability is trusted for what purpose, which profile renders the advice admissible, and how a relying party proves its separate execution mandate require specific source evidence and threat models. See [Research Transfer Register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md) and [Stop-Build Rule](STOP_BUILD_RULE.md).
