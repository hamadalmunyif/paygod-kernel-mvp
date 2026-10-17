# ADR 0004 — Strict typed comparisons and fail-closed evaluation (PROPOSED)

Status: **PROPOSED / EXPERIMENTAL DRAFT, NOT ACCEPTED**  
Date: 2026-10-16  
Issue: [#111](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/111)  
Review draft: [#115](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/115)

## Problem and precise witness

The canonical `main@d347213848f03a6d25554631d0183a682879b11b` evaluator attempts numeric parsing, ordinal string comparison, then truthiness fallback. A missing or null path and string `"false"` can satisfy `input.input.block == false`. A numeric string `"0"` can satisfy numeric `== 0`. A wrong typed value can therefore produce an unsound permission outcome if the Pack author intended a real typed observation.

At exact [RED SHA `d2228a6`](https://github.com/hamadalmunyif/paygod-kernel-mvp/commit/d2228a6ea54baa55a0129dc27a99a531f9018d2e), [CI run 38914437974](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38914437974) compiled and ran: 7 failed, 40 passed, 47 total. The failures were source-derived mismatched comparisons, **not** an external exploit or source authenticity finding.

A naïve strict comparison that returns `false` on absent operands is **not safely compositional**: the existing `critical-cve-blocker` Pack uses `not vulnerabilities.any(v => v.cvss_score_x10 >= 70 and v.status != 'fixed')` to allow. If `v.status` is missing, returning false from `!=` causes `not any(...)` to allow. The source may also omit the entire array.

## Exact compatibility strategy discovered in CI

A global change to `PolicyExpression.Evaluate` made the Kernel CI, portable producer and standalone verifier producer jobs fail: their historical source fixture invokes the secrets Pack using `{"content":"..."}`, i.e. without `secrets_found`. Global fail-closed typed comparison therefore changed the long-standing witness execution. Tests and logs made this incompatibility concrete, not speculative.

**Revised proposed implementation on draft PR #115:**
- `legacy-v1` is the *default* evaluation profile for all existing Packs; prior expressions, including historic coercion and missing `.any` behavior, are unchanged. This is a historical compatibility choice, **not** a claim that a legacy Pack is safe for arbitrary external input.
- `typed-v1` is opt-in through `spec.policy.evaluation_profile` with a declared enum in `contracts/schemas/pack.schema.json` and updated schema-manifest SHA. In this profile, wrong-kind/null/missing comparisons or non-array `any()` throw a deterministic error.
- `RunCommand` pre-evaluates explicit nonlegacy profiles **before** writing plan, findings, ledger, manifest or receipt. A malformed input returns a failure status and creates no canonical evidence files. A deliberately separate CI case proves this at the CLI boundary.
- Example `examples/policy-typed-comparisons/pack.yaml` is synthetic and uses Pack metadata major version 2.0.0, **not** evidence of external scanner admission. No existing Pack upgrades automatically.
- Historic replay uses the original pinned Kernel/Pack semantics; the explicit evaluation profile must be pinned in the Pack source and bundle provenance. This draft retains default legacy behavior for compatibility and does not assert full cross-version replay proof.

The new evaluation profile is **proposed and not accepted** until the exact tested SHA is green, owner reviews this ADR, and remaining source admission / version/replay issues are judged.

## Decision proposal (conditional)

1. **Only with explicit `typed-v1` opt-in**, compare numbers to numbers, strings to strings and booleans to booleans. Retain existing numeric epsilon and ordinal string ordering. `legacy-v1` is unchanged by default.
2. In `typed-v1` only, an absent/null operand or mismatched/unsupported JSON type raises a deterministic `InvalidOperationException` before a verdict can be produced. This applies to `==`, `!=` and ordering comparisons. A Boolean `true` vs `false` comparison is well-typed even though `JsonValueKind` differs.
3. In `typed-v1`, `.any(...)` requires a **present JSON array**; missing/null/wrong-kind source is an evaluation error, not an empty array. A present empty array is permitted but is not proof of a completed external scan. Legacy behavior remains for historic fixtures.
4. This does **not** add a tri-state Kernel decision, pre-Kernel `WITHHELD`, trust-key proof, receipt format, authorization rail, or external source truth. ADR 0003 remains in force: mandatory source missing/unsupported => **external `WITHHELD / NOT RUN` without calling Kernel**. If generic direct `run` sees malformed type during evaluation, it must fail closed; no fake receipt/verdict can be minted.
5. The legacy truthiness of a standalone string/array/object path and `not path` is **not** changed in this proposal. This remains a separate source admission / Pack semantics risk and **must not** be marketed as fixed by typed comparison alone.
6. This ADR **does not approve** the repair or a production upgrade. The experiments are isolated to PR #115 until tests, risk review and explicit owner approval.

## Competing alternatives and rejected shortcuts

- **Only opt-in external preflight**: best way to control real source completeness under ADR 0003; inadequate to fix unsafe standalone generic evaluator when invoked without preflight. Required separately for external sources.
- **Compare invalid types as `false`**: rejected because `not ... any(...)` can transform it into an unsafe allow.
- **Implicit coercion / keep v1 semantics**: rejected as a proposed safe default because malformed sources can satisfy `== false`.
- **New three-valued DSL**: higher-cost schema/ledger/replay migration; not justified by current witness, and conflicts with accepted ADR 0003's boundary until separately approved.
- **Call Cloud/MCP verifier for decision semantics**: rejected; adapters cannot become alternate Kernel policy or receipt authority.

## Additional adversarial findings and containment (second pass)

- The RED/green comparison suite was necessary but not sufficient. In a Boolean expression `not input.required_flag`, the former `AsBool()` truthiness converted missing/null/string/array/number values to arbitrary truthiness. This could yield `true` under negation even without a comparison. In `typed-v1` **only**, top-level, `not`, `and/or` operands and `any()` predicates must be actual JSON Boolean. Legacy behavior remains unchanged for historical replays.
- A typed evaluator rejecting an input after writing the plan is not an acceptable no-artifact guarantee. The draft CLI first evaluates opt-in typed packs and only then writes canonical files. It additionally demands a fresh output directory; a reused directory could expose a prior receipt after a failed run. On failure no new canonical output is written and no existing evidence is deleted. This is not a proof of safe concurrent writers, atomic output commit or consumer freshness checks; those remain separate concerns.
- Even typed-v1 cannot prove source completeness or that omitted fields never matter if a policy does not reference them or short-circuits a condition. For example `not vulnerabilities.any(...)` on a syntactically valid empty array evaluates `true`, irrespective of scanner completion. An external admission gateway **must** validate source success, subject/digest, required schema fields, full result semantics and authorization before any real-world decision. This cannot be inferred from a typed Boolean rule.
- No silent migration: a versioned Pack and pinned Kernel SHA are needed for historic replay. Newly generated receipts bind Pack content by digest, but profile semantics must be checked against that exact version and the actual executable implementation.

## Additional fail-closed operator audit (2026-10-17)

In draft `typed-v1` Boolean operands were restricted to strict JSON booleans, but Boolean `>`, `>=`, `<`, and `<=` expressions still returned `false` through the comparison switch's default branch. Surrounding such an unsupported expression with `not (...)` could yield `true` and satisfy an `allow` condition, despite nonsensical Boolean ordering. The draft must **throw an evaluation exception for Boolean ordering**, rather than returning `false`, while preserving explicitly typed Boolean equality and inequality. Negative regression fixtures for all four operators must be green at a single exact HEAD. This is a typed-v1 draft-only fix; legacy behavior is not changed, and it does not provide source admission or repair Trivy Pack v1 (#116).

## Duplicate property admission hardening (2026-10-17)

An explicit `typed-v1` invocation must reject duplicate raw JSON object property names **before** materializing a `JsonNode`, canonical hashing, policy evaluation or writing any canonical artifact. Duplicate keys (including inside arrays and nested objects not referenced by a policy) can otherwise permit inconsistent interpretation across tools. The new pre-evaluation raw JSON traversal compares decoded property names ordinally; deliberately duplicated fixture inputs require exit code 2, `INPUT_JSON_DUPLICATE_KEY`, and no output directory or Receipt. Existing `legacy-v1` input parsing and historical replay behavior remain untouched. This is **local input-shape containment**, not source provenance, business authorization, signed issuer identity, or scanner completeness. It does not close #111 or #116 without remaining approvals.

## Compatibility and scope review

Reviewed source Pack conditions at `d347213`: `secrets-in-repo-guard` (`== 0`), `critical-cve-blocker` (`!= 'fixed'`, ordered numeric, `not any`), `cross-border-pii-guard` (typed Boolean equality), `ghg-scope-1-2-guard` (nonempty string and truthy references), `iso27001-policy-review` (typed Boolean and `any`), `aws/admin-drift-detection` (string equality/inequality), gas rehearsal (Boolean and string equality), and EIK saved-report example. Existing well-typed fixtures are expected to preserve their decisions, but **CI at repair HEAD must be inspected**. Wrong-typed or missing data changes to an evaluation error **only for explicitly opted-in `typed-v1`** Packs. Existing unmodified legacy Packs preserve their historical behavior, including risks that require source admission.

**Versioning disposition for draft:** choose a version-gated evaluator (`spec.policy.evaluation_profile: typed-v1`; absent means `legacy-v1`), plus explicit Pack major-version bump for newly authored examples. Existing Packs retain prior semantics. Before acceptance review whether trusted Pack version metadata and receipt Pack digest sufficiently pin the evaluation semantics for long-term replay, and whether any output contract must expose the profile directly. No silent rewriting of frozen receipts or witnesses.

## Adversarial witnesses required

- Same literal typed truth vs malformed `missing/null/"false"/0/objects`; across `==`, `!=` and numeric comparison.
- A malformed high/critical CVE item under **negated** `any` cannot become `allow`; missing array also fails closed; valid low/high and empty array retain expected DSL result.
- Wrong/omitted upstream scanner status, incomplete scanner execution and trivy remediation semantics handled by independently accepted **admission/Pack** work [#116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116); successful DSL tests are not enough.
- Existing accepted six starter Packs and gas rehearsal + EIK fixture tests at exact candidate SHA; adapter mutation/authority and verifier witnesses unaffected.
- CLI invalid input must produce no canonical `allow` receipt; record exact exit code/output and artifact absence in a separately accepted CLI regression before merge.

## Approval, rollback and nonclaims

Before merge: exact-SHA CI green (except historical intentional RED witness), owner-reviewed architecture decision, version/replay plan, negative mutation, and independently checked CLI no-bundle-on-failure. Rollback: leave canonical `main` unchanged while draft; if released, use an approved versioned rollback and preserve exported historical receipts and verifier compatibility.

An accepted typed comparison engine **does not** establish source genuineness, scan-completion, CVE remediation, independent timestamp, external release authority, or an institutional pilot.
