# 90-day evidence-led contribution and integration roadmap

Status: planning proposal beginning 2026-10-12. Review at day 7, 30, 60, 90; no automatic permission for expense, external publication, product claims or Kernel mutation.

## Phase 0 — day 0–7: repository hygiene + one external merge-quality fix

1. Review internal open draft PR #107 (legal/public attribution): verify actual facts and qualified review; hold unapproved merge.
2. Review internal draft #103 as research scope: decide tests and CI, not runtime promotion.
3. Turn Virtuals ACP CLI PR #105 into native-test-supported contribution: whitespace-input rejection, no-op JSON, no-TTY delete refusal, hidden boolean tri-state, exact ID, duplicate deletion and actual backend partial PUT witness.
4. Produce one red-before/green-after test and native build/typecheck reproduction. Never assert upstream CI green without upstream check.
5. Update PR with clear authorization boundary, upstream issue #79, non-goals, no PayGod dependency; request one review.
6. Freeze target register without forking more repositories.

Output: PR #105 maintainer-ready with exact test commands; no new production work. Exit: evidence reviewed, human response requested, and pre-merge risks disclosed. If no review, track as WAITING_ON_UPSTREAM without interpreting silence.

## Phase 1 — day 8–30: one native cross-protocol mismatch witness

1. In FLOP TCLK, start at issue #172 and read CONTRIBUTING + AGENTS.md + SPEC.md before any code proposal. Native challenge: signed locked/claimed vs independent read-side settlement observation.
2. In Butler Skills, map registry source commit, version, content hashes, forked duty and owner approval. Produce positive and negative synthetic duty event fixtures; accept 'no demonstrated gap' as a valid result.
3. In ACP Node v2, pin SDK/event mapping to a native job transition. No paid jobs; avoid interpreting SDK role gating as deployed contract enforcement.
4. Generate read-only comparison bundle in PayGod research sandbox; label native coordination, signer identity, rail status and unknown facts separately.

Exit: one reproducible source-specific difference that is NOT already fully solved by native checks; one upstream issue comment with non-invasive tests where appropriate; no wire change and no spend.

## Phase 2 — day 31–60: broaden interoperable evidence, not fork count

1. Select exactly one of AP2/UCP/x402 after first-tier feedback and a demonstrated integration mismatch.
2. Compare official controls: AP2 mandate chain, UCP checkout commitment, x402 pay/facilitator states. Build tests against published SDK/samples without actual payment.
3. Define a minimal optional portable comparison envelope in a research-only repository/path; omit legal authorization, truth, finality and timestamps when not proven.
4. Ask maintainer a concrete test-vector or sample fix question. Offer standalone tests with no PayGod requirement.

Exit: an upstream-native artifact that maintainers can run independently of PayGod, documented difference from baseline, optional bridge proof.

## Phase 3 — day 61–90: reciprocal credibility and architectural decision

1. Review all PRs: submitted/reviewed/merged/released/adopted and follow-up from maintainers. A good closed-unmerged result still informs design.
2. Evaluate one partner pilot only with explicit real workflow, no prohibited economic action, bounded data rights and independent recipient.
3. Decide if PayGod needs a new admission profile, native adapter or evidence schema. Observe -> classify -> recurrence/importance -> layer -> ADR -> implementation if separately approved.
4. Write one verifiable demonstration explaining what native system proves and what optional PayGod adds. Do not announce commercial partnership without evidence.
5. Re-rank targets from actual upstream feedback; decline low-impact forks.

Exit: one trusted native contribution and one credible cross-protocol external witness, OR a documented refutation that eliminates unnecessary construction.

## Roles and weekly deliverables

| Role | Duty | Immutable evidence |
| --- | --- | --- |
| Program owner | Priority, legal/economic and publish authorization; explicit ADR choices | PR approvals, dated decision |
| Upstream contributor | Native issue reproduction, minimal patch, test execution, maintainer interaction | Repro scripts, commits, PR comments |
| Red-team reviewer | Negative tests, permissions, partial failure, prompt injection where relevant | Failure vectors, reproducible observation |
| Protocol investigator | Baseline native behavior and trust boundary, external references | Pin/commit, source link, read-side witness |
| PayGod Kernel steward | No alternate receipt/decision authority; monitor gate regression | CI check run, boundary mutation |
| Independent recipient | Independently replay transferred material within allowed scope | Signed/verifiable recipient feedback, non-claims |
| Commercial liaison | Discover whether a counterparty values an output | Date-stamped explicit answer, no imputed adoption |

Roles may be performed by fewer people initially, but a self-review is NOT independent external validation.

## Risk budget and kill criteria

- No mainnet funds, no card purchases, no ACP economic purchases without a separately frozen authorization and max exposure.
- No cross-repository CI secrets, no copying confidential Observatory artifacts into public PRs.
- No third-party commercial claims just because tests pass.
- Stop a target if native alternatives already solve the specific pain, maintainer explicitly rejects and no distinct local need exists, test cannot be reproduced, or 30-day effort cost grows without new evidence. Continue research freely elsewhere without forcing it into Kernel.
- If a research observation contradicts PayGod's claim, document the discrepancy, revise the claim register through a dated follow-up after review, and preserve original evidence.

## Candidate decision scorecard

For each target retain 0–5 evidence-based values: native user pain 35%; minimal testable change 25%; relevance to proof/authority 20%; maintainer discussion clarity 10%; no-spend/safety 10%. Score does NOT override upstream contribution rules or owner approval. No fork solely due to high popularity/star count.

## Rollout separations

A successful external native PR creates a code contribution, not a PayGod partnership.
A passing PayGod shadow bundle establishes only its declared witness and does not control foreign rails.
A prospective paid customer requires a real buyer and a statement of willingness to buy under concrete terms.
A deploy or website update requires its own repository and release witness. Never infer from a merged Kernel documentation PR.
