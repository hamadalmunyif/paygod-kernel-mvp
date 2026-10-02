# Paygod Specifications & Test Vectors

This directory contains the golden fixtures that define the byte-level behavior of the Paygod Kernel.

## Compliance profile

Paygod currently uses the restricted profile **`paygod-c14n-v1`**. It is deliberately **not** advertised as RFC 8785/JCS.

Any implementation of Paygod canonicalization MUST produce the same canonical bytes for accepted cases and MUST reject the same invalid cases.

The profile accepts:
- JSON `null`, booleans, strings, arrays, and objects;
- integers only, within `[-9007199254740991, 9007199254740991]`;
- object/property names that are already NFC-normalized.

The profile rejects:
- floating-point, decimal, and exponent-form JSON numbers;
- integers outside the safe-integer range;
- non-NFC object/property names;
- unsupported values rather than silently coercing them.

String **values are preserved without Unicode normalization**. Domain packs may derive normalized views for matching, but canonicalization must not silently alter raw evidence semantics.

## Contents

- `test-vectors/canonical-json.json` — accepted and rejected `paygod-c14n-v1` cases.
- `test-vectors/ledger-chaining.json` — ledger payload canonicalization and SHA-256 chaining vectors.

## Verify

```bash
python3 tools/verify_spec.py
```

The Python reference used here is the same restricted canonicalization implementation embedded in the standalone verifier. C# regression tests cover the producer side; CI is responsible for keeping the runtimes aligned.

## Why the restriction exists

Paygod hashes decision-critical JSON across runtimes. Ambiguous floating-point rendering or silent Unicode normalization can create false verification failures or, worse, different commitments for what appears to be the same business input. The restricted profile removes those ambiguities while the project is still pre-pilot.
