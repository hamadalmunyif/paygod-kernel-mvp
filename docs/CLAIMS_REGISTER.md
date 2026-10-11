# PayGod Kernel — Verified Claims Register

**Snapshot:** 2026-10-11 · canonical `main` at [`18b57ff0bd606d36aecd96504b433fe3c7cf84b0`](https://github.com/hamadalmunyif/paygod-kernel-mvp/tree/18b57ff0bd606d36aecd96504b433fe3c7cf84b0).  
**Status:** CURRENT EVIDENCE REVIEW FOR THIS PINNED BASELINE; not a certification, not a claim about a later HEAD.  
**Basis:** owner's 2026-10-10 Arabic draft, the pinned Kernel source, readable GitHub Check Runs, branch ruleset, and separately identified Observatory research records.

## How to interpret the evidence

- **KERNEL_ACCEPTED**: implemented in canonical source/contracts and tested within a **named, bounded witness**.
- **BOUNDARY_ACCEPTED**: documented acceptance restriction; not a new canonical Kernel runtime primitive.
- **OBSERVED_COMPATIBILITY**: external/shadow integration used an existing Kernel interface without promoting research semantics.
- **HARNESS_ONLY**: locally controlled research result; **never** a delivered Kernel capability.
- **UNRESOLVED**: hypothesis, future architecture, or independent review still missing.

A workflow **defined** is not necessarily a workflow **executed**. A Check Run marked `success` means that particular GitHub job passed on that commit, not that its claims hold against arbitrary sources or institutions. Path-filtered and `workflow_dispatch`-only workflows must not be called "passed on every push".

### GitHub evidence actually checked

- Pinned main `18b57ff`: GitHub [Check Runs API](https://github.com/hamadalmunyif/paygod-kernel-mvp/commit/18b57ff0bd606d36aecd96504b433fe3c7cf84b0/checks) showed **18 successful, two skipped** check runs at review time. Skipped `security-gate` and `Dependency Review (PR)` entries **in that check-run listing** are not failures; a separately read [security-gate workflow run on main](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/workflows/security.yml) reported `success`. Do not conflate a skipped check-run entry with a workflow-wide result.
- Active [repository ruleset #12300800](https://github.com/hamadalmunyif/paygod-kernel-mvp/rules/12300800) had `strict_required_status_checks_policy: true`, no bypass actors, and required all six contexts specified in [GATES.md](../GATES.md): `Paygod Kernel CI`, `security-gate`, `Paygod CI Enforcement`, `Pack Contract (paygod/v1)`, `Repository Boundary Gate`, `Verifier Integrity Gate`. Classic `branches/main/protection` endpoint remained inaccessible (HTTP 403) to this connector; the readable active ruleset suffices for this **six-context alignment claim only**.
- Review did not independently re-run the full .NET test suite outside CI or audit all GitHub account security settings. Future revisions need a new SHA and fresh witness results.

## A. Canonical claims accepted at the pinned baseline

| ID | Claim and status | Source / named witness | Scope and explicit refutation |
|---|---|---|---|
| K01 | Deterministic execution and test-vector reproducibility — **KERNEL_ACCEPTED** | [CLI](../src/PayGod.Cli/), [CI enforcement](../.github/workflows/ci-enforce.yml), [witness script](../tools/phase4_docker_witness.ps1) | Within pinned fixture/clock/input profile; differing canonical bytes/digests under equal conditions refute it. No source truth or policy correctness asserted. |
| K02 | Versioned schemas, manifest stability and Pack contract validation — **KERNEL_ACCEPTED** | [schemas](../contracts/schemas/), [CI](../.github/workflows/ci.yml), [Pack Contract](../.github/workflows/pack-contract.yml) | Contract files are checked, **but `run` does not automatically apply every Pack's embedded input schema before evaluating rules**. A passing schema-definition gate does not imply external-data admission. |
| K03 | Manifest/file hashes, receipt binding and locked ledger consistency — **KERNEL_ACCEPTED** | [standalone verifier](../tools/verify_portable_evidence.py), [CI](../.github/workflows/standalone-verifier.yml) | Within `paygod-c14n-v1`; detects named mismatches, not physically true measurements or independent time. |
| K04 | Cross-platform Linux producer → Windows recipient verification — **KERNEL_ACCEPTED** | [portable evidence workflow](../.github/workflows/portable-evidence.yml) | GitHub-hosted jobs only; not an independent recipient institution or all OS permutations. |
| K05 | Standalone recipient verifier without repository checkout — **KERNEL_ACCEPTED** | [standalone workflow](../.github/workflows/standalone-verifier.yml) | Recipient side has its own packaged verifier and transferred evidence; CI demonstration, not third-party operational acceptance. |
| K06 | One-byte artifact mutation rejected in the tested fixture — **KERNEL_ACCEPTED** | [portable workflow](../.github/workflows/portable-evidence.yml) and [standalone workflow](../.github/workflows/standalone-verifier.yml) | Named mutation tests only, not universal integrity of every external transport/storage layer. |
| K07 | Canonicalization rejects fractional/exponent JSON numeric forms, unsafe integers and non-NFC property names — **KERNEL_ACCEPTED** | [canonicalizer tests](../tests/PayGod.Tests/CanonicalizerTests.cs), [CLI CI](../.github/workflows/ci.yml) | Restricted `paygod-c14n-v1` profile; no general decimal measurement representation is shipped. |
| K08 | Single canonical decision/artifact authority for **registered repository adapters** — **KERNEL_ACCEPTED** | [boundary checker](../tools/check_repository_boundary.py), [boundary CI](../.github/workflows/repository-boundary.yml) | Only registered adapters; unregistered or external rails not proven. |
| K09 | Browser / Python verifier regression parity — **KERNEL_ACCEPTED** | [browser suite](../tools/test_browser_verifier.mjs), [browser parity workflow](../.github/workflows/browser-verifier-parity.yml), [dated manual witness](MANUAL_BROWSER_WITNESS_2026-10-03.md) | Path-filtered or dispatched suite plus bounded mobile/manual fixture; no independent full-browser cryptographic audit. |
| K10 | Optional Ed25519 receipt commitment authentication against recipient-supplied keys — **KERNEL_ACCEPTED** | [issuer auth](ISSUER_AUTHENTICITY.md), [issuer-auth workflow](../.github/workflows/issuer-auth.yml) | A trusted key's signature is not an issuer's legal or regulatory mandate. This workflow is path-filtered/dispatchable. |
| K11 | Coordinated replacement can remain internally consistent unless receipt identity is pinned externally — **KERNEL_ACCEPTED (bounded adversarial witness)** | [internal challenge](INTERNAL_VERIFICATION_CHALLENGE.md), [challenge workflow](../.github/workflows/internal-verification-challenge.yml) | Shows both a limitation and a defense against the tested substitution; outside commitment needs independent delivery and its own trust. |
| K12 | Missing mandatory evidence is withheld before Kernel evaluation — **BOUNDARY_ACCEPTED** | [evidence-admission ADR](../adrs/0003-evidence-admission-before-decision-execution.md), [simulated gas rehearsal](../rehearsals/gas-site-readiness/) | `WITHHELD` / `NOT RUN` are orchestration states, **not Kernel verdicts or a universal entrypoint enforcement feature**. |
| K13 | Six executable Packs have named CLI policy tests in canonical CI — **KERNEL_ACCEPTED** | [CI](../.github/workflows/ci.yml), [Packs](../packs/), [Pack contract](../tools/pack_validate.py) | Five core + one AWS provider. Pack-unit success does **not** demonstrate genuine scanner/meter input, SOC 2/ISO certification, production deployment gating, or all required input fields validated. |

## B. Observations deliberately NOT promoted to Kernel

| ID | Finding | Source / evidence quality | Strict ceiling |
|---|---|---|---|
| R01 | Historic T0 controlled-local-harness assertions; **source restricted** | **HARNESS_ONLY**; internal Observatory T0 closure is pinned in a private source. Its run totals and underlying artifacts are **not independently inspectable public evidence**. | No generic non-bypassable financial rail, external verifier mandate, Warrant/E1/E2/S0 Kernel feature, or real financial release. |
| R02 | Experimental external ACP / observation compatibility | **OBSERVED_COMPATIBILITY**; [transfer review](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md) | Compatibility/shadow observation only; not production interoperability certification or an automatic import adapter. |
| R03 | AP2 Collision Pass B; Warrant originality; downstream authority lineage | **UNRESOLVED**; [research-transfer register](OBSERVATORY_TRANSFER_ACCEPTANCE_2026-10-10.md) | Pass B prescribed but **not shown as completed in the cited handoff**. Warrant v0 does not directly commit the exact receipt in its signed body; later reviewer acceptance remains missing. |

**Privacy correction (2026-10-11):** Observatory is now **Private**. This supersedes earlier public-access descriptions. The public register does not link to inaccessible T0 records or present internal harness totals as third-party-verifiable public evidence. This local research remains HARNESS_ONLY and separate from Kernel authority. Earlier published clones or Git history cannot be recalled retrospectively.

## C. Non-claims and open gates

| Area | Current boundary |
|---|---|
| Integrity vs truth | A `VALID` transferred bundle establishes checks of integrity and bindings, **not** authenticity of the original measurement. |
| Signature vs mandate | Ed25519 verifies a signed commitment under supplied trust keys, not an organization's or regulator's authority. |
| Replay/time | Verification reports `replay: not_performed`; clocks are producer-supplied or explicitly unbound, not external trusted timestamps. |
| Input admission | Contracted pack YAML != enforced runtime input schema; the generic `run` path may evaluate incomplete domain fields. |
| Commercial readiness | No verified external financial rail, partner rollout, demand, buyer, price, paid SKU, regulatory certification, enterprise management plane, or marketplace. |
| B2-REAL | [readiness report](../rehearsals/gas-site-readiness/b2/READINESS_REPORT.md) reports **0/10** qualifying cases and **0/5** nondeveloper independent recipients; do not represent rehearsal P0 as qualifying B2 evidence. |
| Enforced authority | Only existing registered adapters are within canonical single-authority mutation tests; arbitrary custom integrations need their own boundary coverage. |
| Stop-Build | [ACTIVE](STOP_BUILD_RULE.md); document/evidence/verified defect work allowed. No new primitive from a research observation alone. |
| Research assertions | T0 and external ACP results remain HARNESS_ONLY / OBSERVED_COMPATIBILITY; the newer GHG shape-admission [PR #103](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/103) is draft and **not part of this pinned main**. |

## D. How to update the living register

1. Pin the exact new Kernel commit, and retain the prior baseline in history.
2. Identify code/contract, rule or fixture, a named negative test, and a successful applicable run **for that commit**. State whether the run was push, PR path-filtered, manual, or external.
3. Explicitly name the claim ceiling and one falsification case; never relabel a research/harness result as production because a page was published.
4. Verify the active [ruleset](https://github.com/hamadalmunyif/paygod-kernel-mvp/rules/12300800) and count actual Check Run conclusions instead of inferring success from a YAML workflow.
5. Update corresponding website [claims register](https://github.com/hamadalmunyif/paygod-cloud-starter/blob/website/paygod-production/website/CLAIMS_REGISTER_2026-10-10.md) and visible `/`, `/explore/`, `/ar/`, `/use-cases/`, `/ar/use-cases/` claims when necessary. The website is **presentation**, never a second decision authority.
6. Keep separately dated historical witness records intact. Unknown or missing supporting evidence is labeled `UNRESOLVED`, not quietly filled.

**Required review before treating a new Pack as operationally fit:** pack tests, pre-Kernel input admission, evidence/source handling, accepted relying-party scope, independent receipt verification, and explicit deployment enforcement. Community code contribution under Apache-2.0 is not equivalent to PayGod production accreditation or a promise of compensation.
