# Open-source target map and contribution ordering

Snapshot: 2026-10-12. Repositories were checked as public and not archived via connected GitHub metadata. Targeting is an internal research priority, NOT a partner agreement, product endorsement or proof of operational integration.

## Selection rule

Rate each candidate 0–5 on: real upstream user problem (35%), narrow testable patch (25%), proximity to PayGod trust boundary (20%), maintainer access/community clarity (10%), low risk or no-spend implementation (10%). Scores are candidate hypotheses and must be recomputed from issue/CI evidence, not presented as market facts. **Tier A first**, **Tier B read/reproduce**, **Tier C only after a grounded need**.

Fork budget: 1 active external code fork at a time for the first 30 days; maximum 2 concurrently only when both have a working witness and maintainer engagement. A directory of candidate links is not a reason to fork.

## Tier A — active engineering conversations

| Repo | Upstream-first contribution | Optional PayGod research | Stage |
| --- | --- | --- | --- |
| [Virtual-Protocol/acp-cli](https://github.com/Virtual-Protocol/acp-cli) | Finish Issue #79 / PR #105: headless resource update/delete with regression, predictable CLI JSON and safe failures | Shadow resource-change evidence, never API mandatory dependency | OPEN PR — improve current fork first |
| [flop-labs/tclk](https://github.com/flop-labs/tclk) | Issue #172: rail-observed reconciliation/conformance; first agree interface and test expectation; follow CONTRIBUTING + AGENTS.md | Separately verify signed coordination vs independently observed value | ISSUE/DESIGN — no fork yet |
| [Virtual-Protocol/butler-skills](https://github.com/Virtual-Protocol/butler-skills) | Author-native validator/fixture test that demonstrates any specific owner-mandate-to-version ambiguity; avoid claiming missing built-in hash controls | Optional signed version/owner mandate continuity receipt | RESEARCH — no fork yet |
| [Virtual-Protocol/acp-node-v2](https://github.com/Virtual-Protocol/acp-node-v2) | Evaluator isolation or deterministic job event fixtures, only after confirming existing safeguards and owner interest | External evaluator-state vs native ACP chain reconciliation | RESEARCH — no fork yet |

## Tier B — protocol and ecosystem interoperability

| Repo | Existing native capability to respect | First useful contribution to upstream | PayGod-only experiment |
| --- | --- | --- | --- |
| [google-agentic-commerce/AP2](https://github.com/google-agentic-commerce/AP2) | Signed intent, payment/checkout mandate chain and receipts; standards decisions also belong to FIDO process | SDK/samples tests for double use, settlement-status evidence, archived verifier keys; don't assume the upstream sample issue is verified | Compare multi-protocol mandate and external receipts |
| [Universal-Commerce-Protocol/ucp](https://github.com/Universal-Commerce-Protocol/ucp) | Checkout model and AP2-compatible extension | Conformance vectors for failed/partial checkout and status reconciliation | Cross-provider portable witness |
| [coinbase/x402](https://github.com/coinbase/x402) | Native HTTP 402 settlement flow | Test negative facilitator outcomes, idempotency and proof surfaces using no-value fixtures | Receipt vs provider-side external proof |
| [a2aproject/A2A](https://github.com/a2aproject/A2A) | Cross-agent tasks, state and discovery; not itself financial settlement proof | Task transition evidence compatibility examples and disputed source labels | Read-only A2A task state + PayGod shadow |
| [modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | MCP tool interoperability and authorization ecosystem | Secure tool invocation/audit example, or negative tests after maintainer discussion | Tool-call lineage into proof envelope |

## Tier C — infrastructure foundations and long-run options

| Repo | Relevant strong native primitive | Default first interaction |
| --- | --- | --- |
| [sigstore/cosign](https://github.com/sigstore/cosign) | Signing, verification and supply-chain transparency | Test interoperability with detached evidence/signature and expiry; do not claim cosign attests source truth |
| [in-toto/attestation](https://github.com/in-toto/attestation) | Provenance predicate and attestation envelopes | Evidence mapping without inventing an attestation format |
| [spiffe/spire](https://github.com/spiffe/spire) | Workload identity issuance/trust domains | How authenticated workload identity differs from organizational decision authority |
| [open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification) | Trace/span interoperability | Propagate source correlation identifiers; do not call tracing a verified financial receipt |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | Mature policy execution | Compare policy decision records, without making OPA an unregistered second canonical PayGod decision authority |

## Watchlist D — agent runtimes, industrial evidence and data spaces (NO FORK at this stage)

These are open doors for future cross-sector workflows, not active joint projects. This layer matters if the same evidence/authority question recurs outside payments.

| Repo | Potential partner-native benefit | PayGod shadow question | First evidence needed |
| --- | --- | --- | --- |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | Reproducible handoff, guardrail and external-action trace tests, if a maintainer requests a concrete fix | Can an action's owner mandate be carried separately from trace semantics? | Actual failing native test, not a generic wrapper |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Durable state, checkpoint/retry test vectors where external effects are involved | Can the outcome of a replayed consequential tool action be externally evidenced? | Native replay/side-effect fixture |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | Typed workflow and executor interoperability tests, if a specific gap emerges | Can evaluator/workflow events be reconciled with external evidence? | Upstream-native event/actor baseline |
| [open62541/open62541](https://github.com/open62541/open62541) | OPC UA data-quality/time/status capture tests without altering industrial device/control paths | Source measurement quality vs portable attested CEMS evidence | Deidentified or synthetic read-only industrial stream |
| [eclipse-milo/milo](https://github.com/eclipse-milo/milo) | OPC UA client read-only evidence mapping and negative source-quality tests | Same CEMS ingestion question across Java implementation | Native OPC UA status/quality fixture |
| [eclipse-edc/Connector](https://github.com/eclipse-edc/Connector) | Contract-controlled data exchange receipt/transfer interoperability | Does the received evidence remain independently verifiable without trusting sender-side dashboard? | Realistic, non-sensitive transfer fixture |
| [ethereum/ERCs](https://github.com/ethereum/ERCs) | Standards analysis only when a concrete identity or wallet mandate interoperability issue emerges | Does protocol-standard authorization survive transfer to offchain evidence? | Existing EIP/ERC reference and working compliance vectors |

Repositories were verified as public and non-archived at snapshot. Their inclusion does NOT authorize modifications to OPC UA control systems, production sensors, token/payment contracts, or model-agent deployments. Industrial integration begins read-only; no process-control commands, no public client telemetry, no regulatory certification claim.

## Explicit out-of-scope early targets

A new cryptocurrency token, a replacement settlement chain, an ACP/TCLK fork with rewritten wire format, a mandatory PayGod SDK in upstream, a generic cross-industry DSL, or commercial bank integration without an authentic external partner witness. Reconsider only with concrete demand and ADR.

## Native integration architecture

Upstream event/receipt/observation -> independent capture with provenance -> explicit admission policy (WITHHELD on unknown mandatory fact) -> existing PayGod canonical path only if it can represent input -> portable original evidence and labeled mapping -> independent verifier -> diagnostic comparison with native state.

In shadow mode PayGod must not affect external action. An external enforcer is a SEPARATE future optional product that would require actual nonbypassability proof and owner/rail authorization.

## Diversity / anti-lock-in

Prefer protocol-neutral evidence and adapters; every integration target gets at least one deliberate comparator to avoid optimising solely for the first partner's implementation. Example comparators: ACP vs A2A job, TCLK coordination vs x402 settlement, Butler duty vs signed supply-chain artifact, AP2 native verifier vs independent observer.

## What establishes a reciprocal relationship?

1. Upstream confirms a native problem, gives feedback or merges a useful fix.
2. Our patch improves their native workflows without imposing PayGod.
3. Their maintainers or external users independently repeat and validate a witness.
4. Only then discuss optional joint adapters/test vectors and business exploration.
No collaborator or partnership is claimed from an opened PR or GitHub issue.
