# PayGod Open Collaboration — Upstream-First Program

Status: PROPOSED / documentation only; 2026-10-12 snapshot. This program does not supersede docs/STOP_BUILD_RULE.md, docs/CLAIMS_REGISTER.md, X1 freeze, any recorded Pass B or historical evidence. Adoption requires maintainer review of the draft PR. No spending, remote releases, or kernel mutation is authorized here.

## Mission

Contribute useful, independently testable improvements to other projects on their terms. Make PayGod integration optional and separate. We want reciprocal trust earned through reproducible engineering, not a requirement that an upstream project rearchitect itself for PayGod.

Core operating rule: **Upstream First · Evidence Native · PayGod Optional**.

Separate four authorities:
- Upstream maintainer: owns accepting, merging and releasing upstream code.
- Upstream runtime/rail: owns its native state, action execution and authorization semantics.
- PayGod Canonical Kernel: owns PayGod decisions, receipts, manifests and bundle identity only for its registered scope.
- Independent verifier: checks defined transferred evidence, and may not invent the source event or decision.

No signature alone proves organizational mandate, external fact truth or settlement; no passing CI alone proves demand or production control.

## Internal priorities and work inventory

| Priority | Workstream | Exit witness | Owner role | Non-claim |
| --- | --- | --- | --- | --- |
| P0 | Preserve canonical determinism, strict portable verifier and six CI checks | Current commit checks and mutation tests green | Kernel maintainer | Does not prove facts or external enforcement |
| P0 | Triage internal open PRs #107 (legal attribution), #103 (GHG research); preserve chronology | Owner-approved resolution for #107; separate research decision for #103 | Repository owner / qualified legal reviewer where applicable | No automatic merge |
| P1 | B2-REAL real cases and nondeveloper recipients | Source-true cases and independently attributable verifier receipts, measured against current gates | Domain evidence lead + external reviewer | A synthetic case never counts as real |
| P1 | Virtuals X1 and FLOP/Butler external shadow experiments | Frozen external-native witness and independently reproducible positive/negative comparisons | Research lead + external protocol reviewer | No financial action, kernel promotion or Pass B rewrite |
| P1 | Upstream contribution register, review package, partner relationships | Each external PR has a tested delta, owner, status URL, test commands and maintenance decision | Upstream liaison | Submitted != reviewed != merged != released |
| P2 | Optional, isolated integration adapters / interoperability test vectors | Native upstream acceptance and shadow-vs-native discrepancy tests | Integration engineer | No production authority claim |
| P3 | Commercial release/control productization | Actual counterparty workflow, authorization boundary, and buyer/recipient witness | Product lead | Research interest != purchase |

Reference boundaries:
- [Claims register](../CLAIMS_REGISTER.md)
- [Stop-build rule](../STOP_BUILD_RULE.md)
- [Repository single-authority closure](../REPOSITORY_BOUNDARY.md)
- [Virtuals X1 research](../../research/virtuals-x1/README.md)

## Workstreams and logical homes

1. Canonical source-of-truth, protected build and verification: paygod-kernel-mvp.
2. Website, presentation and non-authoritative API shell: paygod-cloud-starter, whose default branch is MASTER (not kernel MAIN). Confirm the active deploy repo/path before any website change.
3. External platform reproduction: isolated test folders / disposable forks; upstream-native test runners.
4. Research shadow adapters: opt-in, read-only or recorded-fixture first. Cannot mint canonical PayGod receipt/digest/decision outside the Kernel.
5. Partner exchanges: upstream Issue/PR plus follow-up, never mandatory PayGod marketing in a bugfix.

## Weekly working rhythm (operational checklist, not a scheduled automation)

- Monday: refresh the linked upstream and own PR/issue statuses directly from GitHub; pin commit SHA and exact reviewer actions.
- Tuesday/Wednesday: reproduce one upstream issue, run clean baseline and mutation/negative tests, propose minimal patch.
- Thursday: independent reviewer attempts to refute the patch and evaluates authorization, data loss, timeout, replay, idempotency, compatibility.
- Friday: send one concise maintainer-facing update only when the PR has genuinely improved; close or pause redundant forks.
- Monthly: rank targets by native usefulness, technical contact quality, reproducibility and actual maintainer response. Archive unattractive hypotheses; do not rewrite historical results.

## Decision rules

GO: reproduces a real upstream pain, minimal patch passes native regression, and risks are explicitly bounded.
HOLD: missing maintainer buy-in for a protocol change, unproven server semantics, missing CI, or no independently observable source.
STOP: makes unverifiable claims; bypasses payment, owner or production authority; fabricates a successful settlement/receipt; requires uncontrolled spending; or demands that another project adopt PayGod as a prerequisite.

See:
- [Contribution Protocol](CONTRIBUTION_PROTOCOL.md)
- [Target Repositories](TARGETS.md)
- [Live-work snapshot](PR_REGISTRY.md)
- [90-day Roadmap](ROADMAP_90_DAYS.md)

## Ownership and records

This is a living **planning** program, not a retroactive decision authority. Every status assertion needs a retrieval date and first-party GitHub source. Explicit external acceptance requires an actual upstream maintainer action. Human partner feedback requires a quoted/sourced record. Never infer collaboration from an open PR alone.
