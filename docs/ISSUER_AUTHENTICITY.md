# Issuer Authenticity — Detached Ed25519 Receipt Commitment

Status: **v0.5.2 minimal issuer-authentication profile.**

This layer is separate from bundle integrity.

A successful issuer-authentication result means only:

> a recipient-trusted Ed25519 public key verified a signature over this exact receipt commitment.

It does **not** prove:
- external evidence truth;
- regulator authorization;
- source provenance beyond the signing key;
- trusted third-party time;
- policy replay;
- permission to execute a payment or other downstream action.

## Files

The evidence directory may contain an optional detached control file:

`receipt.sig.json`

It is intentionally not included in `manifest.files`. The receipt binds the manifest and the signature binds the receipt; putting the signature back inside the manifest/receipt chain would create a circular commitment.

Signature envelope:

```json
{
  "profile": "paygod-ed25519-receipt-v1",
  "algorithm": "Ed25519",
  "key_id": "paygod-2026-01",
  "receipt_sha256": "<64 lowercase hex>",
  "signature_b64": "<64-byte Ed25519 signature, base64>"
}
```

The recipient supplies trust separately with a trust store:

```json
{
  "profile": "paygod-ed25519-trust-v1",
  "keys": [
    {
      "key_id": "paygod-2026-01",
      "algorithm": "Ed25519",
      "public_key_b64": "<32-byte raw Ed25519 public key, base64>"
    }
  ]
}
```

The evidence bundle MUST NOT be allowed to define its own trusted public key.

## Exact signed message

The Ed25519 message is byte-for-byte:

```text
ASCII("PAYGOD-RECEIPT-v1")
0x00
ASCII(key_id)
0x00
raw_32_bytes(SHA256(receipt.json bytes))
```

Equivalent notation:

```text
PAYGOD-RECEIPT-v1\0 || key_id || \0 || bytes.fromhex(receipt_sha256)
```

`key_id` is restricted to `[A-Za-z0-9._:-]{1,128}`.

The domain prefix prevents a valid Paygod receipt signature from being silently reinterpreted as a signature for another protocol.

## Key handling

Private issuer keys MUST stay outside the repository.

Example local key creation:

```bash
openssl genpkey -algorithm Ed25519 -out /secure/path/paygod-issuer.pem
openssl pkey -in /secure/path/paygod-issuer.pem -pubout -out /secure/path/paygod-issuer.pub.pem
```

Install the established crypto backend:

```bash
python -m pip install -r tools/requirements-issuer-auth.txt
```

Export the public key into an external trust store:

```bash
python tools/export_issuer_trust_store.py \
  --key-id paygod-2026-01 \
  --public-key /secure/path/paygod-issuer.pub.pem \
  --output trusted-issuers.json
```

Sign an already-produced receipt commitment:

```bash
python tools/sign_receipt_commitment.py evidence \
  --key-id paygod-2026-01 \
  --private-key /secure/path/paygod-issuer.pem
```

This writes `evidence/receipt.sig.json`.

Verify integrity and issuer authenticity:

```bash
python tools/verify_portable_evidence.py evidence \
  --trusted-issuer-keys trusted-issuers.json \
  --require-issuer-authenticity \
  --result verification-result.json
```

Without `--require-issuer-authenticity`, a missing/untrusted signature does not redefine bundle integrity.

## Result states

```text
issuer_authenticity = verified
```

Only when:
- `receipt.sig.json` has the supported profile;
- its `receipt_sha256` equals the actual receipt bytes;
- `key_id` exists in the externally supplied trust store;
- the trusted key is valid Ed25519 material;
- the Ed25519 signature verifies.

```text
issuer_authenticity = not_verified
```

Examples:
- no signature supplied;
- no external trust anchor supplied;
- crypto backend unavailable.

```text
issuer_authenticity = failed
```

Examples:
- signature envelope malformed;
- signed receipt digest does not match;
- key id is absent from a supplied trust store;
- signature is cryptographically invalid.

## Still open before production key operations

This minimal profile does not yet define:
- key rotation;
- revocation;
- organization-level certificate chains;
- hardware-backed key custody;
- regulator or CA authorization;
- transparency-log publication.

Those are separate gates and should be added only when the real workflow requires them.
