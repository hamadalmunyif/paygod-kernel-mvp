# Evidence-Governed Development — Scoped Stop-Build Amendment

Status: **PROPOSED on PR #108; effective only upon approved merge to main**  
Decision date: 2026-10-14  
Original stop-build baseline: `6b65d0d97ce61111b9eb77762de03f4a518c0d21` (after P0 / PR #92).

## Decision and supersession

The original repository-wide stop-build remains a historical governance event. This amendment replaces its **prospective blanket development interpretation**, not its historical evidence, conclusions, or release gates. Before this amendment is merged, the existing main-branch rule remains in force.

The operating model is **open exploration, scoped authority, evidence-gated canonical promotion**. No independent track waits for B2-REAL, Virtuals X1, Pass B, upstream PR acceptance, or commercial validation unless its own explicit acceptance claim depends on that particular evidence.

## Independently open tracks

Research, technical discovery, authorized read-only acquisition, fixtures and shadow adapters, cross-protocol comparison, upstream-native contributions, provenance experiments, UX/prototypes, B2-REAL recruitment, independent-receiver tests, industrial measurements, and buyer discovery may proceed concurrently in their appropriate research, fork, or documentation workspace. These activities do not by themselves require a new Kernel ADR. Existing licenses, privacy, consents, data-handling restrictions and external-system rules still apply.

Each track has its own hypothesis, source/commit pin, scope, owner, falsifier, budget, evidence classification, dependencies, and next decision. A blocked track is marked HOLD with a scoped reason; its status does not freeze unrelated tracks.

## Protected canonical boundary

Changes to Kernel decision semantics, policy DSL, canonicalization, input schema or admission semantics, receipt/ledger/manifest/bundle identity, trust/key model, execution authority, independent verification contracts, or a new security primitive require **before merge**:
1. Concrete defect, real observation, or compelling external witness with reproducible positive/negative controls; recurrence OR documented high operational severity.
2. Comparison to existing native and PayGod capabilities; evidence that an adapter, fixture or external orchestration cannot solve the need.
3. ADR specifying exact layer/contract, alternative designs, migration/backward compatibility, failure modes, explicit non-claims, security/authority boundaries, and rollback.
4. Canonical regression, adversarial mutation and CI/ruleset checks at the proposed head SHA; explicit owner approval according to repository protections.

Exploratory implementations of new ideas may exist on isolated non-canonical branches or in the private Observatory, with clear **EXPERIMENTAL / NOT ACCEPTED** labels and no production publication. They must not mint or impersonate canonical PayGod decisions, receipts, or bundle identity.

Confirmed defects and urgent security patches may be fixed under the existing protected review/CI process with a recorded incident or defect witness and impact; they must not be delayed by unrelated pilot quotas. A material semantic change still requires an ADR (an expedited security ADR where necessary).

## Preserved immutable evidence

P0 stays `CLOSED — PASS WITH BOUNDARY`, `simulated_shadow_pilot`, `counts_as_b2_real=false`.
B2-REAL remains at its actually observed counts and gates (currently 0/10 eligible cases and 0/5 nondeveloper recipients in the pinned register), **gating only its own readiness claims**.
Virtuals X1 Level 0, X1-R0 acquisition/spend boundaries, AP2 blind Pass B, T0 and existing witness records stay frozen at their original pins and classifications. Never rewrite historical score sheets, tamper with original artifacts, expose Pass A to blind reviewers, or promote HARNESS_ONLY to external proof. Add dated errata or independently pinned follow-up evidence.

## Authority and operating limits

Upstream maintainers own upstream merges/releases; foreign runtimes own their native transitions; the PayGod canonical Kernel owns its registered decisions and artifacts; the verifier checks the declared envelope only. Reading, signing, hashing or passing CI alone never proves external truth, organizational mandate, causal control, trusted time, settlement or commercial demand.

No live money movement, wallet funding, paid ACP job, production deployment, control-system command, secret distribution or external release without its own explicit authorization and bounded risk approval. No automatic merge or deployment follows from this document.

## Track progression

DISCOVER → REPRODUCE → BOUNDARIES → SHADOW / NATIVE TEST → INDEPENDENT REVIEW → GO / HOLD / STOP.

GO means **proceed in the named scope**; it never silently grants canonical or production authority. For canonical promotion, use the stricter witness → layer → ADR → tests → owner/review → merge chain.

Metrics: time to reproduce, first native test, engineering hours, external-wait time, adapter reuse, external recipient verification, and avoided unnecessary forks. Track unresolved causes by scope, not as global blockers.

References: [Claims register](CLAIMS_REGISTER.md), [roadmap](../ROADMAP.md), [open collaboration](open-collaboration/README.md), [CMP-01](open-collaboration/CONTRIBUTION_PROTOCOL.md).

## Historical non-retroactivity

This prospective amendment does **not** declare that historical Stop-Build was invalid, that a particular external integration passed, that a new feature was released, or that prior tests are newly independent. The superseded text remains available unchanged in Git history at the cited baseline.
