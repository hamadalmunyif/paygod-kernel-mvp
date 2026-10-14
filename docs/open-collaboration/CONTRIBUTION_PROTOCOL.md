# CMP-01 — Contribution-to-Merge Protocol

Status: PROPOSED. Reusable process, not an upstream rule or an automatic right to merge. Follow each upstream CONTRIBUTING, LICENSE, CODEOWNERS, SECURITY, CLA/DCO, branch protections and release requirements first.

## Eight verifiable stages

0. **DISCOVER** — Confirm upstream is active and correct repo/branch. Capture issue URL, current main SHA, license, review convention and native control that may already solve the need. Do not fork based only on an attractive idea.
1. **REPRODUCE** — Pin upstream revision, run its own tests, provide minimal positive and negative witness. Report limitations including dependencies, credentials and unavailable network evidence.
2. **BOUNDARIES** — Identify who controls user consent, roles, API authorization, wallet/rail, money, data retention, object identity, timestamps and release. Build a concrete affected-surface inventory (code, API, schema, CLI output, docs, on-chain semantics, logs, CI).
3. **DESIGN** — Choose upstream-native fix with smallest viable diff. Confirm that requested behavior is not already implemented. Write non-goals. Changes to wire/state/rail/authorization require upstream issue-first consultation.
4. **FORK/BRANCH** — Fork only if write permission is absent AND code is needed. Create one short-lived branch from pinned upstream base, and keep the upstream remote. Never merge upstream main into a long-lived incompatible PayGod fork. Use read-only sample/adapters for exploratory projects.
5. **VALIDATE** — Native build/typecheck + regression that fails before fix and passes after + adversarial negative tests. Include compatibility and fail-closed behavior. For external service semantics (e.g., PUT update), mark unverified until server/test-double or authorized sandbox validates.
6. **SUBMIT/REVIEW** — One problem per PR. Include 'why', issue link, tests and exact reproduction, changed authority boundary, threat model, non-goals, expected API/UX changes, upstream commit reference, and any required changelog entry. Respond to feedback with evidence. Submit only when patch is useful independently of PayGod.
7. **VERIFY OUTCOME** — Differentiate SUBMITTED, REVIEWED, APPROVED, MERGED, RELEASED and ADOPTED. Independently check upstream main commit, release tag/package and actual behavior. Closed-unmerged is not rejected on merits unless the maintainer says so.

## Control matrix by changed surface

| Surface touched | Required negative or compatibility witness |
| --- | --- |
| CLI flags / headless execution | No TTY; missing required flag; machine-readable error; no stale prompts; old interactive mode preserved |
| Update API | Unknown ID; whitespace-only fields; omission/false/null tri-state; field preservation in true backend; retries/concurrency |
| Delete API | Wrong ID; repeated deletion; missing confirmation; explicit noninteractive consent; permissions; auditability |
| Events / retry | Unknown result, duplicate delivery, idempotency key reuse, reordering, partial failure |
| Agent evaluation | Provider-controlled prompt/data isolation; evaluator identity; signature does not prove independent judgment |
| Signed transcript | Correct DID/key; canonical bytes; venue-time metadata separate from signer time; replay and disputed ordering |
| Settlement | Native chain/rail observation; finality/reorg where applicable; reconciliation with claimed protocol status |
| PayGod evidence | File/receipt/ledger digest mutation; detached trust-key binding; no local receipt manufacture by adapter |

## Fork policy

- **No fork** for reading, watching, discussing, writing interoperability documentation, or submitting a non-code issue.
- **Temporary fork** for a confirmed upstream bug or accepted narrow improvement requiring code; track upstream base/head and keep history intact.
- **Research sandbox** if the question is about cross-protocol behavior rather than changing upstream. Prefer fixture import and read-only observers.
- **Never fork to impose PayGod**: upstream gets a self-contained benefit without a PayGod SDK, token, service, branding, account, required API, paid call, or mandatory network permission.
- **Long-lived fork** requires separately documented upstream incompatibility, security/maintenance owners and exit strategy. Default is no.

## Upstream-first review message structure

Title: fix/test/docs(subsystem): observable behavior.

Body:
- Problem and user impact (link to independently reported issue).
- Reproduction on pinned upstream base; exactly what fails.
- One-paragraph smallest patch and non-goals.
- Tests: exact commands, exit results, failing-before/green-after evidence.
- Authority/compatibility/security impacts: explicit if none.
- No mandatory PayGod integration or hidden dependency.
- Ask: one specific maintainer judgment. Respect CLA/security reporting instructions.

Feedback never means automatic adoption. One courteous follow-up after a material test improvement or a reasonable review interval; no mass tagging or demand for review.

## Strict rule for disclosure

Do not publish exploitable vulnerabilities or confidential user data into public PRs; follow upstream SECURITY.md and private advisories. Do not upload API keys, wallet keys, nonpublic Observatory data, full customer logs, or personal contacts.

## CMP-01 application to Virtuals ACP CLI PR #105

Actual external PR: https://github.com/Virtual-Protocol/acp-cli/pull/105
Linked reporter issue: https://github.com/Virtual-Protocol/acp-cli/issues/79
Head SHA reviewed: 5526b606f55739aa675cd7e5a1e62ab4d45c0f59

Confirmed source-level risks to resolve or explicitly bound before asking for merge:
- Whitespace-only update name/description may be trim-converted to empty strings. Server rejection/acceptance is unverified.
- --resource-id plus --force removes CLI confirmation by design. Identify this authorization/UX change in PR.
- Resource update sends a Partial body via HTTP PUT. Backend preservation of omitted fields is NOT proven by TypeScript.
- Headless delete WITHOUT --force still attempts readline; fail promptly instead of hanging in no-TTY contexts.
- 'No changes made.' in --json mode is plain text, violating machine-readable result expectation.

Tests to add first: no-TTY update success; invalid/missing resource ID; whitespace-only name/description/url; partial field preservation at API boundary; hidden/no-hidden/absent tri-state; no-op with --json; no-TTY delete without force; with force exact-target deletion and double-delete; original interactive behavior. An upstream-native regression or approved authorized mock is required for any claimed server behavior. Avoid patching paygod-kernel-mvp as a substitute.

Existing build/typecheck noted in PR body is self-reported; no upstream CI result or maintainer review was found as of snapshot.

## Independence and claims

Native platform controls may already solve much of the problem; compare them as a baseline. A shadow PayGod witness is not a native enforcement guarantee. The verifier proves only stated checks. Demonstrated synthetic behavior does not become a production, regulatory or financial claim. See docs/CLAIMS_REGISTER.md.

## 2026-10-14 — parallel integration rule (proposed)

CMP-01 is an **upstream contribution** protocol, not a dependency gate on PayGod's observational experiments. Run two independent lanes:

- **Native upstream lane:** reproduce an upstream problem, test and propose a minimal dependency-free fix. Only the upstream maintainer may merge and release it. External review waiting time is recorded, never converted into an internal product freeze.
- **Optional local interoperability lane:** capture legally accessible original bytes or supplied fixtures; do read-only, provenance-labeled adaptation and independently test a PayGod shadow result. Never rely on unmerged upstream behavior as though available in production.

A cross-lane dependency is recorded only if a concrete interface or permission makes it technically unavoidable. B2, X1, AP2 Pass B and CEMS each have independent claim gates. Exploratory Kernel candidates remain non-canonical until witness → ADR → protected tests → approval.

Every case must record `scope`, `source_ref`, `falsifier`, `authority_boundary`, `permission`, `next_action`, `blocking_dependency` (if any), `engineering_hours`, `external_wait_days` and `evidence_ceiling`. Do not bypass privacy, secrets, payment authorization or upstream SECURITY instructions.
