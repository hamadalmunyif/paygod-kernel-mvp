# Paygod Specifications & Test Vectors

This directory contains the golden fixtures that define `paygod-c14n-v1` behavior.

Every independent implementation MUST produce the same canonical bytes for accepted vectors and the same explicit rejection class for rejected vectors.

## Canonical profile

`paygod-c14n-v1` is a restricted deterministic JSON profile, not RFC 8785.

It accepts null, booleans, strings, arrays, objects, and safe integers only. It rejects floats/decimals, unsafe integers, and non-NFC property names. String values are preserved without silent Unicode normalization.

## Contents

- `test-vectors/canonical-json.json` — accepted canonical forms plus fail-closed rejection vectors.
- `test-vectors/ledger-chaining.json` — ledger payload canonicalization and SHA-256 chaining.
- `test-vectors/transport-parity-v1.json` — frozen portable-evidence transport corpus for manifest/bundle/receipt binding, external receipt commitment, coherent rewrite and recipient-supplied issuer-trust parity across independent verifier implementations. Its Git blob identity is part of the review evidence; the included RFC 8032-derived key material is public test-only material, never an operational trust root.

## Verification

```bash
python3 tools/verify_spec.py
```

The Python verifier implementation is one implementation of the profile. The .NET canonicalizer is separately regression-tested and both must remain byte-compatible.

## Transport parity boundary

`paygod-transport-parity-v1` is verifier test evidence, not execution or authorization evidence. A passing implementation may claim parity only for the explicit transport cases in the frozen corpus. It does not prove source admission, scanner completeness, policy correctness, replay execution, trusted time, issuer mandate or payment/release authority.
