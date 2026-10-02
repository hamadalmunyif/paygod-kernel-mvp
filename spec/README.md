# Paygod Specifications & Test Vectors

This directory contains the golden fixtures that define `paygod-c14n-v1` behavior.

Every independent implementation MUST produce the same canonical bytes for accepted vectors and the same explicit rejection class for rejected vectors.

## Canonical profile

`paygod-c14n-v1` is a restricted deterministic JSON profile, not RFC 8785.

It accepts null, booleans, strings, arrays, objects, and safe integers only. It rejects floats/decimals, unsafe integers, and non-NFC property names. String values are preserved without silent Unicode normalization.

## Contents

- `test-vectors/canonical-json.json` — accepted canonical forms plus fail-closed rejection vectors.
- `test-vectors/ledger-chaining.json` — ledger payload canonicalization and SHA-256 chaining.

## Verification

```bash
python3 tools/verify_spec.py
```

The Python verifier implementation is one implementation of the profile. The .NET canonicalizer is separately regression-tested and both must remain byte-compatible.
