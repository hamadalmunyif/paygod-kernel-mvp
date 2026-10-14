# Evidence Integration Kit (EIK) — developer and coding-agent entry

**Status (2026-10-14): documentation-only entry point.** The published CLI, Pack contract and independent verifier are real, bounded components. EIK is an **experimental integration concept**, not yet a packaged SDK, hosted service, autonomous Pack authoring agent, MCP server, A2A endpoint, certified deployment gate, or public marketplace.

**Principle: Build privately. Verify independently. Contribute optionally.**

This guide is designed for developers and coding agents who know their own problem better than the PayGod maintainers. You do **not** need to submit an upstream PR, disclose your Pack, connect a PayGod account or deploy a PayGod service just to test a local Pack.

## 1. Discover the truthful compatibility surface

- [Public implementation and limits](../../README.md)
- [Dated claims register](../CLAIMS_REGISTER.md)
- [Pack definition contract](../../contracts/schemas/pack.schema.json)
- [Policy examples and non-claims](../STARTER_PACKS.md)
- [Canonical recipient verifier](../STANDALONE_VERIFIER.md)
- [Agent contribution instructions](../../AGENTS.md)
- [Machine-readable discovery snapshot](capabilities.v0.json) — informational, **not** a versioned Kernel schema or endorsed agent protocol.

First ask: what does the user's **native** platform already prove? What does it lack? There is no reason to add PayGod if the native tooling already solves the need with equal assurance and less cost.

## 2. Choose the right extension surface

| Need | First suitable location | Explicit boundary |
| --- | --- | --- |
| A domain-specific policy | Private/local Pack (`pack.yaml` plus `tests/cases.yaml`) | Kernel still owns the canonical evaluation output |
| Missing, stale, impossible or unsupported observations | Pre-Kernel admission, read-only mapping or fixture | `WITHHELD / NOT RUN` external to Kernel; never invent a verdict |
| Source retrieval or provider lifecycle | Optional source-specific adapter | Do not forge authorization, provenance or receipts |
| Common policy evaluator/receipt semantics actually defective | Separate evidence-driven Kernel issue/ADR | New semantics require guarded approval and compatibility witnesses |
| Recipient needs stronger source truth / independent time | External evidence/authority and a specific verification test | The existing integrity verifier alone does not provide these |

## 3. Build your first **private** Pack

Prerequisites: .NET 8 and Python 3.11+ for the documented tools. Use a disposable working directory or branch; `pack init` writes into `packs/core/` unless a provider is selected.

```bash
dotnet run --project src/PayGod.Cli -- pack init --name local-evidence-example
python3 -m pip install -r tools/requirements.txt
python3 tools/pack_validate.py
dotnet run --project src/PayGod.Cli -- test --pack packs/core/local-evidence-example --json
```

Replace the example rules with rules matching **your** policy. Design at least these test classes: accepted true/false input, missing required field, wrong type, source error masquerading as a clean report, contradictory source, and tampered evidence. The CLI policy fixture test can compare its declared decisions, but it is **not** a universal pre-Kernel admission validator.

An **optional structural-only preflight** is available for Packs that declare an explicit object schema with nonempty `required` fields. Write a local JSON fixture such as `{"input":{"block":false}}` for the generated example, then run:

```bash
python3 tools/eik_admit.py --pack packs/core/local-evidence-example --input input.json
```

The tool returns `STRUCTURAL_ONLY_PASS` for correctly typed declared fields, or `WITHHELD_NOT_RUN` (exit code 2) for missing/malformed inputs. It never invokes Kernel or asserts scanner success, source truth, temporal validity or external execution authority. **A structural pass alone must not trigger production `run`.** Provider-specific source completion, authenticity, provenance and any explicit mandate need separate admission checks.

> **Critical current limitation:** generic `run` does not automatically enforce every embedded Pack input schema. A Pack schema valid under `pack_validate.py` is not proof of source truth, runtime mandatory-field completeness, or a safe production decision. Perform admission **before** invoking `run`; for missing required evidence the external orchestrator must report `WITHHELD / NOT RUN` and not call Kernel. See [ADR 0003](../../adrs/0003-evidence-admission-before-decision-execution.md).

Do not treat a generated Pack's illustrative `allow` result as deployment permission. The external system and its owner retain operational release authority.

## 4. Optional authorized evidence run and handoff

After independently establishing admission for a complete compatible input, the canonical CLI can be exercised with a deliberately fixed fixture. Example command shape (not a runnable proof without that admitted input and a selected Pack):

```bash
dotnet run --project src/PayGod.Cli -- run --pack packs/core/<your-pack> --input <admitted-input.json> --out <evidence-dir>
```

Use [standalone verifier documentation](../STANDALONE_VERIFIER.md) to verify a transferred directory and optionally pin the expected receipt SHA-256 using a **separately delivered** commitment. Integrity verification does not prove source authenticity, external organizational authorization, independent clock time, replay, or the truth of the represented observation.

## 5. Optional contribution to the public repository

Contribute only if useful to others, with a small isolated diff under the existing Apache-2.0/DCO process. Include:
- Problem, native alternative, and precise scope.
- Source type, consent and explicit admission rule; no secrets or private data.
- Positive and negative cases including missing/incorrect evidence.
- Commands and exact revision to reproduce tests.
- If applicable, independent verifier result and explicit non-claims.
- No required PayGod account/service, payments, permanent fork, or modification of another team's project.

Read [CONTRIBUTING.md](../../CONTRIBUTING.md) before submitting. A merged Pack is **not** production certification, a commercial listing, financial reward, or proof that the author's domain policy is substantively correct.

## 6. Proposed next experiment — **not yet executed**

The private Observatory tracks EIK as `H-007 / E-004 / W-02`: compare local user/agent setup and source-admission rejection against native GitHub Actions / direct CLI, then repeat on a second distinct source. Count human interventions, false admission, engineering hours and independent recipient comprehension. Continue source-specific research in parallel; no upstream maintainer is required to install PayGod.

A future published skill, discovery service or MCP tool may consume these public docs and bounded contracts. No chatbot is expected to auto-discover PayGod today merely because this file exists.
