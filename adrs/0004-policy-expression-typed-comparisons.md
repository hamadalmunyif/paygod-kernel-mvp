# ADR 0004 — Strict typed comparisons and fail-closed evaluation (PROPOSED)

Status: **PROPOSED / EXPERIMENTAL DRAFT, NOT ACCEPTED**  
Date: 2026-10-16  
Issue: [#111](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/111)  
Review draft: [#115](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/115)

## Problem and precise witness

The canonical `main@d347213848f03a6d25554631d0183a682879b11b` evaluator attempts numeric parsing, ordinal string comparison, then truthiness fallback. A missing or null path and string `"false"` can satisfy `input.input.block == false`. A numeric string `"0"` can satisfy numeric `== 0`. A wrong typed value can therefore produce an unsound permission outcome if the Pack author intended a real typed observation.

At exact [RED SHA `d2228a6`](https://github.com/hamadalmunyif/paygod-kernel-mvp/commit/d2228a6ea54baa55a0129dc27a99a531f9018d2e), [CI run 38914437974](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38914437974) compiled and ran: 7 failed, 40 passed, 47 total. The failures were source-derived mismatched comparisons, **not** an external exploit or source authenticity finding.

A naïve strict comparison that returns `false` on absent operands is **not safely compositional**: the existing `critical-cve-blocker` Pack uses `not vulnerabilities.any(v => v.cvss_score_x10 >= 70 and v.status != 'fixed')` to allow. If `v.status` is missing, returning false from `!=` causes `not any(...)` to allow. The source may also omit the entire array.

## Decision proposal (conditional)

1. Compare **numbers to numbers**, **strings to strings** and **booleans to booleans** only. Retain the existing numeric epsilon comparison and ordinal string ordering for now to avoid an unrelated numeric contract rewrite.
2. A comparison involving an absent/null operand or mismatched/unsupported JSON types raises a deterministic `InvalidOperationException` before a verdict can be produced. This applies to `==`, `!=` and ordering comparisons. A Boolean `true` vs `false` comparison is well-typed even though `JsonValueKind` differs.
3. `.any(...)` requires a **present JSON array**; missing/null/wrong-kind source is an evaluation error, **not** an empty array. A present empty array is permitted within the DSL *but is not proof of a completed external scan*.
4. This does **not** add a tri-state Kernel decision, pre-Kernel `WITHHELD`, trust-key proof, receipt format, authorization rail, or external source truth. ADR 0003 remains in force: mandatory source missing/unsupported => **external `WITHHELD / NOT RUN` without calling Kernel**. If generic direct `run` sees malformed type during evaluation, it must fail closed; no fake receipt/verdict can be minted.
5. The legacy truthiness of a standalone string/array/object path and `not path` is **not** changed in this proposal. This remains a separate source admission / Pack semantics risk and **must not** be marketed as fixed by typed comparison alone.
6. This ADR **does not approve** the repair or a production upgrade. The experiments are isolated to PR #115 until tests, risk review and explicit owner approval.

## Competing alternatives and rejected shortcuts

- **Only opt-in external preflight**: best way to control real source completeness under ADR 0003; inadequate to fix unsafe standalone generic evaluator when invoked without preflight. Required separately for external sources.
- **Compare invalid types as `false`**: rejected because `not ... any(...)` can transform it into an unsafe allow.
- **Implicit coercion / keep v1 semantics**: rejected as a proposed safe default because malformed sources can satisfy `== false`.
- **New three-valued DSL**: higher-cost schema/ledger/replay migration; not justified by current witness, and conflicts with accepted ADR 0003's boundary until separately approved.
- **Call Cloud/MCP verifier for decision semantics**: rejected; adapters cannot become alternate Kernel policy or receipt authority.

## Compatibility and scope review

Reviewed source Pack conditions at `d347213`: `secrets-in-repo-guard` (`== 0`), `critical-cve-blocker` (`!= 'fixed'`, ordered numeric, `not any`), `cross-border-pii-guard` (typed Boolean equality), `ghg-scope-1-2-guard` (nonempty string and truthy references), `iso27001-policy-review` (typed Boolean and `any`), `aws/admin-drift-detection` (string equality/inequality), gas rehearsal (Boolean and string equality), and EIK saved-report example. Existing well-typed fixtures are expected to preserve their decisions, but **CI at repair HEAD must be inspected**. Wrong-typed or missing data may now change from a verdict or `unknown` to an evaluation error.

**Unresolved migration/compatibility question:** this is an observable `paygod/v1` DSL semantic change, and would alter replay behavior of historical malformed input if raw replay used the new evaluator. Before acceptance, the owner must choose either (A) a version-gated evaluator or (B) a documented breaking v1 security correction with explicit replay/version handling and original evaluator SHA pinned. No silent rewriting of frozen receipts or witnesses.

## Adversarial witnesses required

- Same literal typed truth vs malformed `missing/null/"false"/0/objects`; across `==`, `!=` and numeric comparison.
- A malformed high/critical CVE item under **negated** `any` cannot become `allow`; missing array also fails closed; valid low/high and empty array retain expected DSL result.
- Wrong/omitted upstream scanner status, incomplete scanner execution and trivy remediation semantics handled by independently accepted **admission/Pack** work [#116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116); successful DSL tests are not enough.
- Existing accepted six starter Packs and gas rehearsal + EIK fixture tests at exact candidate SHA; adapter mutation/authority and verifier witnesses unaffected.
- CLI invalid input must produce no canonical `allow` receipt; record exact exit code/output and artifact absence in a separately accepted CLI regression before merge.

## Approval, rollback and nonclaims

Before merge: exact-SHA CI green (except historical intentional RED witness), owner-reviewed architecture decision, version/replay plan, negative mutation, and independently checked CLI no-bundle-on-failure. Rollback: leave canonical `main` unchanged while draft; if released, use an approved versioned rollback and preserve exported historical receipts and verifier compatibility.

An accepted typed comparison engine **does not** establish source genuineness, scan-completion, CVE remediation, independent timestamp, external release authority, or an institutional pilot.
