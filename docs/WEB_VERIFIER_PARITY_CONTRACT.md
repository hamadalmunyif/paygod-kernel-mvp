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

Observed on Kernel `main@203bee9ac5668975bf5248c57f922c214567d415`:

| Artifact | Role | Git blob |
| --- | --- | --- |
| `src/PayGod.Cli/Core/Canonicalizer.cs` | .NET implementation of `paygod-c14n-v1` | `52d4f67bb58e5d26ee690fdf52eec4196b6f0a99` |
| `spec/test-vectors/canonical-json.json` | canonical accepted/rejected corpus | `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8` |
| `spec/test-vectors/ledger-chaining.json` | ledger canonical/hash corpus | `ac16a235641f22101dab93187af0eb992f010987` |

`paygod-c14n-v1` is a restricted deterministic JSON profile, **not RFC 8785**. It accepts null, Boolean, string, array, object and safe integer values; rejects floating/exponent numeric forms and unsafe integers; requires NFC object/property names; and preserves string values without silent Unicode normalization.

## Website evidence snapshot

Observed website production source `paygod-cloud-starter@fcf272f0291b602dfbb9b75b4faf15fa01ca340b`:

- `website/src/verifier.mjs` implements browser `paygod-c14n-v1`, transport verification and optional recipient-supplied issuer trust.
- `website/tests/fixtures/kernel-c14n-reference-20261014.json` has Git blob `3880d3a45b417ae95cae9a7b8cebb1c8c47722d8`, exactly matching the Kernel canonical corpus blob above.
- `website/tests/kernel_c14n_reference.mjs` verifies canonical bytes and SHA-256 against that frozen corpus and separately rejects decimal, exponent and unsafe integer lexical forms.
- Browser and standalone Python verifier tests separately exercise bundle/manifest/ledger/receipt checks and issuer-auth negative cases.

This snapshot establishes **bounded implementation parity**, not full Kernel equivalence.

## Currently proven cross-runtime parity

The frozen canonical corpus contains 11 cases:

- 8 accepted canonicalization cases.
- 3 fail-closed rejection cases.

The website additionally checks three raw numeric lexical rejects before `JSON.parse`.

The shared evidence therefore supports this claim:

> The tested website implementation reproduces the frozen Kernel `paygod-c14n-v1` canonical bytes / hashes for the shared accepted vectors and rejects the shared canonical bad vectors under the tested implementation.

It does **not** support the stronger claim that the browser is a complete implementation of every Kernel verifier, policy, admission, replay or authority rule.

## Parity dimensions still to promote

A future Full Parity Corpus should move each dimension independently:

| Dimension | Current state | Promotion requirement |
| --- | --- | --- |
| Canonical JSON | **SHARED CORPUS / TESTED** | keep exact source blob pin and byte/hash parity |
| Ledger chaining | Kernel corpus exists; website tests ledger locally | import/pin the Kernel ledger corpus and compare exact hashes cross-runtime |
| Manifest / bundle digest | website local regression coverage | define versioned Kernel transport vectors and consume them unchanged |
| Receipt binding | website local regression coverage | shared positive + mutation corpus from Kernel |
| External receipt commitment | website tested locally | shared Kernel vector for coherent rewrite + original pin |
| Issuer signature / trust store | browser + Python demo tests | shared versioned trust/signature corpus with explicit recipient trust semantics |
| Replay | Kernel standalone/Docker witnesses exist | keep browser status explicit as `not_performed`; do not simulate execution authority |
| Time | producer clock checks exist | keep separate from trusted timestamp authority |
| Policy evaluation / typed-v1 | Kernel-only | **OUT OF WEBSITE PARITY** unless separately designed and approved |
| Evidence admission / source truth | ADR 0003 / source-specific | **OUT OF WEBSITE PARITY** |
| Issuer mandate / release authority | separate trust/authorization problem | **OUT OF WEBSITE PARITY** |

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

Create a versioned Full Parity Corpus that extends beyond canonical JSON to ledger, manifest/bundle, receipt binding, external receipt commitment and issuer-auth/trust cases. Run the same frozen corpus through .NET Kernel/reference tooling, standalone Python verifier and browser verifier.

A valid outcome may be either:

- `PARITY_CONFIRMED` for the scoped dimension, or
- `DIVERGENCE_FOUND` with exact vector, implementation and bytes.

Do not repair or normalize a divergence before preserving the failing witness.

## Nonclaims

This document does not accept ADR 0004, merge PR #115, prove external recipient adoption, certify a security scanner, configure production branch protection, authorize a payment/release, or elevate the website into Kernel authority.
