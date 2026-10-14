# AGENTS.md — PayGod Kernel contributor/agent instructions

Scope: this repository. These instructions are advisory developer guidance, **not** authorization to modify external systems, run payments, merge pull requests, publish site claims, or bypass CI/review. Follow user consent, repository policies, and tool permissions.

## First read
1. [README.md](README.md) — the public capability and non-claim boundary.
2. [GATES.md](GATES.md) and [docs/STOP_BUILD_RULE.md](docs/STOP_BUILD_RULE.md) — mandatory gates and scoped freedom to explore after [PR #108](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/108).
3. [adrs/0003-evidence-admission-before-decision-execution.md](adrs/0003-evidence-admission-before-decision-execution.md) — external evidence admission.
4. [docs/CLAIMS_REGISTER.md](docs/CLAIMS_REGISTER.md) — **dated** claims at a pinned source revision; do not extrapolate a later release.
5. [docs/eik/README.md](docs/eik/README.md) — optional self-service Pack/integration onboarding.

## What an agent can help a user do
- Explain the public Pack YAML contract and test fixtures.
- Create a Pack privately using `dotnet run --project src/PayGod.Cli -- pack init --name <safe-name>`, edit its rules, and run `test --pack`.
- Compare an existing source/native control against an optional PayGod policy evaluation, only with authorized data and permitted dependencies.
- Prepare a small optional PR with specific positive and **negative** tests. Private use requires no PR.
- Independently verify an existing canonical bundle using documented verifier tools.

These are **instructions to use current code**, not claims that an EIK SDK, MCP service, A2A endpoint, online Pack marketplace, automated feasibility oracle, or live financial release system has shipped.

## Non-negotiable boundaries
- The registered canonical Kernel path alone creates PayGod decision, artifact, ledger, manifest, receipt, and bundle identity. An adapter or AI agent must not create substitute values.
- `spec.inputs.schema` in a Pack is **not** universally enforced by generic `run`. A parsed JSON file, `pack_validate.py` pass, or `pack test` pass is not proof that a real external report was complete or authentic.
- Missing, contradictory, temporally unproven, or semantically unrepresentable **mandatory** evidence: `WITHHELD / NOT RUN` in **pre-Kernel orchestration**; do not invoke canonical evaluation as though admitted. Neither state is a Kernel verdict.
- Integrity ≠ source truth ≠ issuer authenticity ≠ organizational mandate ≠ trusted time ≠ replay correctness.
- Never assume an approved code review equals authorization to deploy, or a scanner count of zero equals a successfully completed scan.
- A new Pack or adapter does not silently change `paygod-c14n-v1`, receipt/manifest semantics, trust dimensions, or schema behavior. Propose a separate ADR, positive/negative witness, compatibility plan, and guarded Kernel PR for such changes.
- Preserve frozen research/witness classifications, avoid copying private Observatory findings or secrets into this public repo, and do not manufacture evidence or partner endorsement.

## Smallest reproducible development loop
1. State the user's problem, the native solution already available, required facts, source authority, and the least privileged test.
2. Check whether an existing Pack plus an external admission profile is sufficient.
3. Pin versions and use synthetic or authorized read-only inputs. Design positive, missing, malformed, tampered, and incorrect-source tests.
4. Run the Pack definition validation (`python tools/pack_validate.py`) and policy fixture tests (`dotnet run --project src/PayGod.Cli -- test --pack <path>`).
5. Only after explicit evidence admission, use canonical `run` on authorized inputs and inspect a transferred bundle using [standalone verifier guidance](docs/STANDALONE_VERIFIER.md).
6. Record failures, manual intervention, baseline/native alternative, version pins, non-claims, and whether the result justifies submission.
7. Contribute upstream **only if the user chooses**. Follow [CONTRIBUTING.md](CONTRIBUTING.md) and required status checks.

This file is not a substitute for executable validation or repository branch protections.
