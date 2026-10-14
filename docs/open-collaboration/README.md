# PayGod Open Collaboration — Parallel Evidence-Governed Program

**Status: ACTIVE as of the accepted 2026-10-14 [PR #108](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/108); supersedes only the prospective blanket stop-build.** The earlier rule and frozen witnesses remain in Git history. Open independently scoped exploration while protecting canonical authority and release gates.

Operating rule: **Upstream First · Evidence Native · PayGod Optional**.

**Build privately · Verify independently · Contribute optionally.** Personal/agent-authored Packs can be developed and tested without creating a PayGod PR or account. The [EIK entry guide](../eik/README.md) is documentation and a local onboarding path, not a released adapter SDK, hosted assessment, authenticated source, or deploy authorization.

## Four separate authorities

1. Upstream maintainer accepts/releases their own source; our PR is never automatic adoption.
2. External runtime/rail owns native execution, identity, and settlement.
3. Canonical PayGod Kernel alone owns its registered decision and evidence identity.
4. Independent verifier checks defined recipient-side evidence only, never inventing fact, time, or authorization.

## Parallel work lanes, with independent GO/HOLD/STOP

| Lane | Home | What can advance now | Gate specific to its claims |
| --- | --- | --- | --- |
| Canonical integrity and defect fixes | Kernel | repair, reproducibility and bounded security work | witness, protected CI, owner review; semantic ADR |
| B2-REAL / gas acceptance | gas case register + Observatory | solicit and evaluate genuinely eligible cases/recipients | frozen B2 qualification; not prerequisite for other lanes |
| External Virtuals X1 | Observatory + pinned X1 materials | read-only capture, prospective shadow design | spend approval before paid job, no Kernel promotion by inference |
| AP2 blind Pass B | isolated neutral handoff | independent review and falsifiers | blinded isolation; preserve Pass A and history |
| OSS native contributions | temporary fork/upstream PR | reproduce and improve external native bugs | upstream maintainer controls merge/release |
| Optional adapters / cross-protocol | Observatory | fixtures, read-only comparisons, negative tests | upstream authority stays external; no forged receipt |
| CEMS/GHG industrial data | Observatory | read-only/deidentified data and numeric-admission research | source quality, permission, domain-specific acceptance |
| Nondeveloper handoff | Observatory | portable evidence, independent recipient exercises | recipient's documented scoped verification result |
| Buyer discovery | private research records | needs interviews, counterfactuals, pilot design | buyer or partner statements, not inferred demand |
| Website/public claims | Cloud | describe accepted evidence accurately | claim register, deployment-specific witness |

**A HOLD on one lane never blocks another unless a documented dependency is technically necessary.** A success in one lane never waives another lane's acceptance or authorization gate.

## Minimal interaction contract

Upstream event / saved JSON / measurement → preserve raw bytes and source → provenance-labeled optional adapter → pre-Kernel admission (WITHHELD/NOT RUN outside Kernel for missing mandatory facts) → unchanged canonical Kernel when representable → portable evidence → independent scoped verifier → compare against native status.

Adaptation is optional; do not require upstream to install PayGod, change protocol, accept a fork, transfer secrets, or trust a PayGod receipt. Prefer no checkout, narrow reads, and native fixtures when available.

## Work ownership

- **Kernel** = sole canonical implemented PayGod decision/receipt/manifest/bundle source.
- **Private Observatory** = hypothesis and decision registry, experiments, independent review isolation, and shadow integrations; never public proof by mere existence.
- **Cloud starter** = non-authoritative website and presentation. Its default branch is `master`.
- **Upstream projects** = code and release authority for their own projects.

Do not create new repositories solely to reopen a lane. Use disposable branches/forks only for a proved native change.

## Routing and review

Each lane tracks: source URL + SHA/date, objective, falsifier, data permission, authority boundary, acceptance gate, owner, blocked reason if any, direct hours, upstream waiting days, current claim ceiling and next permitted action. Review lanes concurrently. Only semantic Kernel promotion requires a dated ADR and protected checks; defect/security repairs follow the documented protected path.

## Decision rules

- **GO**: scoped authorized next experiment or upstream-native bug fix with verifiable outcome.
- **HOLD**: missing permission, witness, reviewer independence, or rail-level authorization **for that lane only**.
- **STOP**: unverifiable claims, forged receipts, undisclosed spending, bypass of upstream controls, confidentiality violations or inadequate bounded risk.

Continue independently useful work while a foreign PR is awaiting response. Submitted, reviewed, merged, released, adopted and externally verified are distinct states.

References: [Scoped Stop-Build Amendment](../STOP_BUILD_RULE.md), [Claims](../CLAIMS_REGISTER.md), [CMP-01](CONTRIBUTION_PROTOCOL.md), [Targets](TARGETS.md), [Registry](PR_REGISTRY.md), [Roadmap](ROADMAP_90_DAYS.md).
