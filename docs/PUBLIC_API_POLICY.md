# Public API Policy

This document defines the public contract of the Paygod Kernel.

## 1. Canonical JSON profile

Paygod does **not** currently claim RFC 8785 / JCS conformance.

The canonical profile used by decision-critical hashes is `paygod-c14n-v1`. It is intentionally restricted so independent implementations can fail closed instead of guessing about numeric or Unicode semantics.

### Accepted JSON values

- `null`;
- booleans;
- strings;
- arrays;
- objects;
- integers in the inclusive range `[-9007199254740991, 9007199254740991]`.

### Rejected values

- floating-point / decimal JSON numbers;
- exponent-form JSON numbers;
- integers outside the safe-integer range;
- object/property names that are not already NFC-normalized;
- unsupported or unknown runtime value types.

String **values** are preserved as supplied; the canonicalizer does not silently normalize their Unicode. Object/property names must already be NFC before canonicalization.

Objects are ordered using ordinal UTF-16 key ordering. JSON strings use deterministic escaping, including escaping non-ASCII UTF-16 code units. Output is UTF-8 without BOM and hashes use SHA-256 over the canonical UTF-8 bytes.

This is a Paygod-specific restricted profile. A future RFC 8785 profile, if added, MUST be separately versioned and validated against independent JCS test vectors.

## 2. Decision-domain numeric rule

Decision-critical domain inputs MUST avoid floating-point values. Use scaled integers with an explicit unit, for example:

- money: `amount_minor: 125050`, `currency: "SAR"`;
- rates: `rate_bps: 250` for 2.50%;
- CVSS: `cvss_score_tenths: 98` for 9.8;
- emissions: integer mass units such as `scope1_kgco2e`.

## 3. Verification semantics

A top-level verifier `status: valid` means **bundle integrity verification succeeded within the documented trust boundary**. It does not imply issuer authenticity, replay, external truth, or trusted time.

Machine-readable verifier output exposes these dimensions separately:

- `integrity`;
- `issuer_authenticity`;
- `replay`;
- `time_authority`.

## 4. CLI contract

The `paygod` binary uses stable machine-readable outputs where documented. Verification failures fail closed and return a non-zero exit code.

## 5. Schemas

Schemas under `contracts/schemas/` are versioned contracts. Breaking semantic changes require an explicit version/migration, not a silent reinterpretation.

## Breaking-change rule

A change to canonicalization, digest construction, decision semantics, or verifier trust claims must be versioned, documented, and covered by cross-implementation regression evidence.
