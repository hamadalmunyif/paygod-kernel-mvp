# Kernel ↔ Website Verifier Parity Contract

Status: **PROPOSED / DOCUMENTATION CONTRACT — NOT A PRODUCTION OR AUTHORITY CLAIM**  
Date: 2026-10-17

## Purpose

Define what the PayGod website/browser verifier may claim to implement from the canonical Kernel, how that relationship is evidenced, and what remains outside browser parity.

The Kernel remains the source of decision semantics and canonical protocol definitions. The website is a **recipient-side verifier surface**. It must not become an alternate policy engine, receipt issuer, source-admission authority or release authority.

## Authority order

1. Versioned Kernel source and specifications.
2. Frozen Kernel test corpus / Git blob identities.
3. Independent implementations that reproduce the frozen corpus.
4. Website build and browser verifier tests.
5. Deployment metadata and live browser smoke.

A lower layer cannot redefine a higher layer. A green website build cannot change Kernel semantics.

## Canonical source snapshot

Observed on Kernel `main@81e8020065434d0af3557444c28bd3e128d06899`:

| Artifact | Role | Git blob |
| --- | --- | --- |
| `src/PayGod.Cli/Core/Canonicalizer.cs` | .NET implementation of `paygod-c14n-v1` | `52d4f67bb58e5d26ee690fdf52eec4196b6f0a99` |
| `spec/test-vectors/canonical-json.json` | canonical accepted/rejected corpus | `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8` |
| `spec/test-vectors/ledger-chaining.json` | ledger canonical/hash corpus | `ac16a235641f22101dab93187af0eb992f010987` |
| `spec/test-vectors/transport-parity-v1.json` | portable transport verifier corpus | `d3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da` |

`paygod-c14n-v1` is a restricted deterministic JSON profile, **not RFC 8785**. It accepts null, Boolean, string, array, object and safe integer values; rejects floating/exponent numeric forms and unsafe integers; requires NFC object/property names; and preserves string values without silent Unicode normalization.

## Website evidence snapshot

Observed pinned website source snapshot `paygod-cloud-starter@af7061963367288c6fb3830e5723e5f5bc63230e` on `website/paygod-production`:

- `website/src/verifier.mjs` implements browser `paygod-c14n-v1`, transport verification and optional recipient-supplied issuer trust.
- `website/tests/fixtures/kernel-c14n-reference-20261014.json` has Git blob `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8`, exactly matching the Kernel canonical corpus blob above.
- `website/tests/kernel_c14n_reference.mjs` verifies canonical bytes and SHA-256 against that frozen corpus and separately rejects decimal, exponent and unsafe integer lexical forms.
- Browser and standalone Python verifier tests separately exercise bundle/manifest/ledger/receipt checks and issuer-auth negative cases.

This pinned source snapshot establishes the website implementation context used by the parity evidence below. It does **not** by itself prove live production state; deployment metadata and live smoke remain separate release evidence.

## Currently proven cross-runtime parity

The frozen canonical corpus contains 11 cases:

- 8 accepted canonicalization cases.
- 3 fail-closed rejection cases.

The website additionally checks three raw numeric lexical rejects before `JSON.parse`.

The shared evidence therefore supports this claim:

> The tested website implementation reproduces the frozen Kernel `paygod-c14n-v1` canonical bytes / hashes for the shared accepted vectors and rejects the shared canonical bad vectors under the tested implementation.

It does **not** support the stronger claim that the browser is a complete implementation of every Kernel verifier, policy, admission, replay or authority rule.

## Current parity state

The first six rows below are the dimensions for which frozen shared corpora are consumed across the tested implementations. The remaining rows are explicit boundary dimensions: they are intentionally **not** established by browser/shared-corpus parity and are listed to prevent overclaiming.

| Dimension | Current state | Evidence |
| --- | --- | --- |
| Canonical JSON | **SHARED PARITY CONFIRMED / BOUNDED** | blob `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8`; website canonical gate passes |
| Ledger chaining | **SHARED PARITY CONFIRMED / BOUNDED** | blob `ac16a235641f22101dab93187af0eb992f010987`; website ledger gate passes |
| Manifest / bundle digest | **SHARED TRANSPORT CORPUS / TESTED** | transport blob `d3e682cb7f4f82cc88c4b8fd3ec7fb99d53357da` |
| Receipt binding | **SHARED TRANSPORT CORPUS / TESTED** | same frozen transport corpus |
| External receipt commitment | **SHARED TRANSPORT CORPUS / TESTED** | wrong-pin + coherent-rewrite cases |
| Issuer signature / trust store | **SHARED TRANSPORT CORPUS / TESTED** | trusted issuer + wrong trust key cases |
| Replay | Kernel standalone/Docker witnesses exist | browser remains explicit `not_performed`; execution replay is not browser parity |
| Time | producer clock checks exist | remains separate from trusted timestamp authority |
| Policy evaluation / typed-v1 | Kernel-only | **OUT OF WEBSITE PARITY** unless separately designed and approved |
| Evidence admission / source truth | ADR 0003 / source-specific | **OUT OF WEBSITE PARITY** |
| Issuer mandate / release authority | separate trust/authorization problem | **OUT OF WEBSITE PARITY** |

The first Kernel transport-corpus run preserved a real divergence: JS passed while Python returned `cryptography_backend_unavailable` for the trusted-issuer case. The corpus was not rewritten. The existing pinned issuer-auth backend was installed in the CI path. Codex then identified two cross-platform byte-preservation risks: Python text-mode materialization and Git checkout newline conversion. Both were corrected without changing corpus bytes or expected outcomes: Python now writes exact UTF-8 bytes, and `.gitattributes` pins the frozen corpora to `eol=lf` with an explicit CI `git check-attr eol` gate. PR #125 passed 8/8 workflow families at exact head `0585ee622ffe7683ce36beac322beebc95025a0b`, Codex completed with no findings, and the corpus/fixes were merged to Kernel `main@81e8020065434d0af3557444c28bd3e128d06899`.

Website PR #22 copies the exact same transport corpus blob. Its current exact head `bf43c9627c8868a59e15cedca11357841e23abe5` passes LF-checkout enforcement, canonical parity, ledger parity, browser-JS transport parity, vendored-Python transport parity, privacy-contract checks, and existing verifier regressions. It remains pre-merge evidence until the website merge train completes and the merged production SHA is correlated to deployment/live smoke.

## Required claim language

Allowed when exact evidence is green:

- “matches the pinned Kernel canonical corpus”
- “recipient-side integrity verification”
- “issuer authenticity verified against recipient-supplied trusted key” when that exact check succeeds
- “replay not performed” when execution was not independently replayed
- “producer-supplied time” when no independent time authority exists

Not allowed from browser parity alone:

- “same as the Kernel in all semantics”
- “source is true/authentic”
- “scanner completed correctly”
- “decision was authorized”
- “release/payment is authorized”
- “trusted timestamp”
- “independently replayed” when replay was not executed

## Change control

Any change to `paygod-c14n-v1`, its canonical source corpus, or decision-critical transport format must:

1. change through the Kernel first;
2. create a new reviewed Kernel commit and, where applicable, a new corpus blob identity;
3. update the website consumer explicitly;
4. run cross-runtime negative and positive tests;
5. preserve prior versioned fixtures needed for historical verification;
6. avoid silently relabeling an older website implementation as compatible.

The **corpus Git blob** is the strongest identity for exact shared test bytes. Branch names and moving `main` SHAs are contextual provenance, not substitutes for the frozen blob.

## Next falsifiable milestone

The next milestone is no longer another local parity vector. It is **exact-SHA release correlation**:

1. merge the Kernel-owned corpus and documentation through controlled reviewed PRs;
2. merge website parity changes in dependency order;
3. require a push-triggered Website Verifier on the exact merged production-branch SHA;
4. require Vercel production deployment metadata to point to that exact SHA;
5. perform live production smoke on the public routes;
6. record the final merged Kernel and website SHAs in the Observatory evidence record.

Until that release correlation is complete, parity is verified in source/CI but not yet described as deployed exact-SHA production evidence.

## Nonclaims

This document does not accept ADR 0004, merge PR #115, prove external recipient adoption, certify a security scanner, configure production branch protection, authorize a payment/release, or elevate the website into Kernel authority.
