# PR, issue and collaboration register

Status: READ-ONLY SNAPSHOT as of 2026-10-12; always click through to GitHub before a current-state claim. This file does not automatically sync. GitHub is the authority over PR state, merge commit, review and release. Repo access and candidate scope were checked with the connected GitHub account.

## Live user-authored PR queue

| ID | Repo | Link | Snapshot | Base / state | Decision / next action |
| --- | --- | --- | --- | --- | --- |
| INT-001 | hamadalmunyif/paygod-kernel-mvp | [PR #107](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/107) | Open, DRAFT, not merged | main | P0: clarify legal entity/trademark facts; require owner's approval and competent IP counsel before merge |
| INT-002 | hamadalmunyif/paygod-kernel-mvp | [PR #103](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/103) | Open, DRAFT, not merged | main | P1: GHG admission research only; no runtime promotion without witness + ADR |
| INT-003 | hamadalmunyif/paygod-kernel-mvp | [PR #108](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/108) | Open, DRAFT, not merged | main; branch docs/upstream-first-collaboration-2026-10-12 | P1: this documentation-only program; maintain owner review and do not auto-merge |
| EXT-001 | Virtual-Protocol/acp-cli | [PR #105](https://github.com/Virtual-Protocol/acp-cli/pull/105) | Open, not merged; no recorded human reviews at snapshot | main; fork hamadalmunyif/acp-cli, branch fix/resource-headless-lifecycle, head 5526b606f55739aa675cd7e5a1e62ab4d45c0f59 | P1: fixes/negative tests in fork; ask upstream maintainer to assess after evidence, not market PayGod |
| — | hamadalmunyif/paygod-cloud-starter | [PRs](https://github.com/hamadalmunyif/paygod-cloud-starter/pulls) | No open PR in authenticated user's current PR list | default branch master | Observe active website releases; no unrelated code changes |

These statuses were read from the user's PR lists and PR metadata, not inferred from issue search. The Cloud repo's CURRENT default branch is master, not main.

## Issue/design opportunity queue (not submitted PRs)

| ID | Upstream | URL | Distinguishing work | Next gate |
| --- | --- | --- | --- | --- |
| DES-001 | Virtuals ACP CLI | [Issue #79](https://github.com/Virtual-Protocol/acp-cli/issues/79) | External reporter's non-TTY resource update/delete defect; linked to our EXT-001 | Reproduce + regression + maintainer review |
| DES-002 | FLOP TCLK | [Issue #172](https://github.com/flop-labs/tclk/issues/172) | Native rail-observed settlement vs signed coordination status | Confirm owner design scope and produce rail-status test vectors, no production money |
| DES-003 | Virtuals Butler | [Registry rules](https://github.com/Virtual-Protocol/butler-skills/blob/main/TEMPLATE_STANDARD.md) | Owner mandate vs resolved published code version, accounting for existing publish immutability and checks | Produce counterexample with synthetic fork/event or record NO GAP |
| DES-004 | ACP Node v2 | [SDK](https://github.com/Virtual-Protocol/acp-node-v2) | Evaluator data/identity at native transition and external chain | Confirm existing isolation and compare source-specific tests |
| DES-005 | AP2 | [Protocol repository](https://github.com/google-agentic-commerce/AP2) | Mandate identity, possible reuse and settlement evidence; standards scope distinct from SDK | Independently replay relevant sample test; verify upstream maintainer's response before suggesting changes |

No external PR was observed from this account in the specifically checked repositories Virtual-Protocol/acp-node-v2, Virtual-Protocol/butler-skills, flop-labs/tclk, flop-labs/technocore-chat or google-agentic-commerce/AP2. This is **not** an exhaustive search of all GitHub organizations or all historical PRs.

## Important historical anchors (not open work)

- [Kernel #57](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/57) — merged single-authority boundary for registered adapters.
- [Kernel #68](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/68) — merged verification contract repair.
- [Kernel #93](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/93) — merged stop-build and research charter; not a permanent ban on separate research.
- [Kernel #95](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/95) — closed WITHOUT merge, superseded by subsequent X1 work; do not call accepted.
- [Kernel #104](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/104), [#105](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/105), [#106](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/106) — merged public-claims/private Observatory documentation, not evidence of external adoption.
- [Cloud #12](https://github.com/hamadalmunyif/paygod-cloud-starter/pull/12) — merged bilingual V2 canonical homepage change; does not certify deployment of the exact website state.
- [Cloud #11](https://github.com/hamadalmunyif/paygod-cloud-starter/pull/11) — closed unmerged, superseded by #12.

## Live lookup routes and status procedure

- Internal PRs: https://github.com/hamadalmunyif/paygod-kernel-mvp/pulls and https://github.com/hamadalmunyif/paygod-cloud-starter/pulls
- External contribution: https://github.com/Virtual-Protocol/acp-cli/pull/105
- Fork activity: https://github.com/hamadalmunyif/acp-cli/branches
- Cross-repo GitHub PR discovery is scoped per repository via authenticated listing. Do NOT treat a GitHub issue-search response as a PR list if it returns issues under PR filters.
- Weekly refresh record: retrieved_at UTC; repo, PR number, title, author, base, head SHA, draft, state, merged_at, review_count, CI contexts, label, responsible maintainer, next step, deadline only if agreed, native upstream release witness.
- Always distinguish open, human-reviewed, approved, merged, release-published, recipient-verified and partner-accepted. An automated bot comment is not a human review.
- On superseding, cross-link previous record and append dated disposition; never rewrite the original snapshot or manipulate historic pass/fail counts.

## Baselines reviewed at creation

- Kernel main: 6cb1e7cd7d96225e7ec607fb073b89f7c7500496
- ACP CLI main: 9d2be827cc19e4ea2cecfff3896398607537ea3e
- Virtuals ACP v2 main: 392dcc6eb17a6884c214c21aff31afa1b99f45ae
- Butler Skills main: f41a1c561e1ebff8a8941c9dbb460fc9271e0fd0
- FLOP TCLK main: 5cc4ab93efbc8999a3a7e1471b639deca25998ea
These are comparison snapshots, not guaranteed permanent HEADs. Refresh before patching.

## Required status labels

DISCOVERED; REPRODUCED; PATCHED; TESTED; SUBMITTED; HUMAN_REVIEWED; MERGED; RELEASED; EXTERNALLY_VERIFIED; ADOPTED; CLOSED_UNMERGED; SUPERSEDED. A single PR can have several dated evidence lines. Avoid promoting self-reported testing to independently verified testing.
