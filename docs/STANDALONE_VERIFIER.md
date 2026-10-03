# Standalone Third-Party Verifier Witness

Status: **v0.4 integrity + optional detached Ed25519 issuer authentication.**

## What integrity verification proves

The standalone verifier can verify a transferred Paygod evidence bundle without repository checkout, pack replay, Docker, the .NET SDK, or producer workspace state.

Integrity verification checks:

- manifest structure and bundle digest;
- artifact SHA-256 digests and byte counts;
- no unexpected regular files or symlinks in the transferred directory;
- exactly one manifest-locked `ledger.jsonl`;
- receipt-to-manifest binding;
- ledger hash-chain integrity under `paygod-c14n-v1`;
- decision-critical receipt claims against the locked ledger;
- an optional externally supplied `--expect-receipt-sha256` commitment.

The result exposes `receipt_sha256` and the verified `ledger_head`.

## Verification dimensions

A top-level `status: valid` is retained for CLI compatibility, but it means only that the **integrity** checks in this verifier succeeded.

The machine-readable result separates:

```text
integrity            verified | failed
issuer_authenticity  verified | not_verified | failed
replay               not_performed
time_authority       producer_supplied | unbound | failed
```

`producer_supplied` time means the receipt/manifest/ledger agree on the injected producer clock. It is not third-party trusted timestamping.

## Canonicalization contract

The verifier accepts `paygod-c14n-v1`, not an RFC 8785 claim.

The profile accepts null, booleans, strings, arrays, objects, and safe integers only. It rejects floats/decimals, unsafe integers, and non-NFC property names. String values are preserved without silent Unicode normalization.

## Issuer authenticity

An optional detached `receipt.sig.json` can authenticate the receipt commitment against a recipient-supplied external Ed25519 trust store.

Issuer authenticity is deliberately separate from integrity. A bad/missing signature does not silently redefine an otherwise valid integrity result. Callers that require an authenticated issuer can add:

```bash
--trusted-issuer-keys trusted-issuers.json \
--require-issuer-authenticity
```

See [Issuer Authenticity](ISSUER_AUTHENTICITY.md).

## External receipt commitment

A relying party can pin a receipt received over another channel:

```bash
python paygod-verify.py evidence \
  --expect-receipt-sha256 <64-lowercase-hex>
```

A mismatch fails closed. This proves equality with the externally committed receipt bytes; it does not by itself authenticate who supplied that external commitment.

## Unbound clock compatibility

Legacy/local output whose receipt clock is `unset` requires explicit `--allow-unbound-clock`. The result reports `time_authority: unbound`.

## Non-claims

The verifier does not currently prove:

- organization/regulator authorization merely because a trusted signing key verified;
- truth or provenance of external evidence;
- trusted third-party time;
- replay of the original decision;
- institutional adoption;
- a live financial/payment release.

Those capabilities require separate evidence and MUST NOT be inferred from `status: valid`.
