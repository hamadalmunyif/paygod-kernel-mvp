# Standalone Third-Party Verifier Witness

Status: **v0.3 verification-contract repair in progress on Issue #67.**

## What the verifier proves

The standalone verifier can check a transferred Paygod evidence directory without checking out the repository, rebuilding the kernel, or replaying the original decision.

It verifies the **integrity dimension**:
- manifest structure and declared file set;
- artifact SHA-256 digests and byte counts;
- rejection of unexpected regular files and symlinks in the transferred directory;
- bundle-digest binding;
- exactly one manifest-locked `ledger.jsonl`;
- receipt-to-manifest binding;
- ledger hash-chain integrity under `paygod-c14n-v1`;
- decision-critical receipt claims against the locked ledger;
- optional external pinning of `receipt.json` with `--expect-receipt-sha256`.

The result also exposes:
- `receipt_sha256` — the digest a recipient can pin through another channel;
- `ledger_head` — the verified last ledger record hash.

## Verification dimensions

A top-level `status: valid` means **bundle integrity verified within this contract**. It does not mean every trust dimension is verified.

Example:

```json
{
  "status": "valid",
  "verification": {
    "integrity": "verified",
    "issuer_authenticity": "not_verified",
    "replay": "not_performed",
    "time_authority": "producer_supplied"
  }
}
```

The dimensions are deliberately independent:

- **Integrity** — are the transferred artifacts internally consistent and bound as declared?
- **Issuer authenticity** — is the receipt authenticated to a known issuer key? Not yet implemented in v0.3.
- **Replay** — was the original input/policy/runner material re-executed and compared? Not performed by this verifier.
- **Time authority** — the current timestamp is producer-supplied when `PAYGOD_CLOCK` is injected, or explicitly unbound in the supported local mode. It is not a third-party timestamp.

## Canonicalization profile

Receipts MUST declare:

```json
"canonicalization": { "json": "paygod-c14n-v1" }
```

`paygod-c14n-v1` is a restricted Paygod profile, not RFC 8785/JCS. It accepts null, booleans, strings, arrays, objects, and safe integers only. Floating-point/decimal/exponent numbers, unsafe integers, non-NFC object keys, and unsupported values fail closed. String values are preserved without silent Unicode normalization.

See `spec/README.md` and `spec/test-vectors/canonical-json.json`.

## External receipt commitment

A relying party that receives the receipt digest through an independent channel can pin it:

```bash
python paygod-verify.py evidence \
  --expect-receipt-sha256 <64-lowercase-hex> \
  --result verification-result.json
```

A mismatch fails closed.

This authenticates neither the issuer nor the external facts by itself; it only binds verification to the externally supplied digest.

## Clock handling

When the producer injects `PAYGOD_CLOCK`, the verifier checks its consistency with manifest/ledger time and reports:

```text
time_authority: producer_supplied
```

For the supported non-strict local path where the receipt clock is `unset`, acceptance requires `--allow-unbound-clock` and reports:

```text
time_authority: unbound
```

No current path claims trusted third-party time.

## Non-claims

The current verifier does **not** prove:
- truth or provenance of an external real-world fact;
- issuer identity or possession of an institutional signing key;
- trusted third-party time;
- replay of the policy decision;
- institutional adoption or willingness to pay;
- a live financial or operational release integration.

**Integrity is not authenticity. Authenticity is not external truth.**

## Next gate

After v0.5.1 closes, the next engineering activity is an **Internal Rehearsal** designed to attack these boundaries before any external pilot. Issuer signing and real provenance remain separately versioned follow-ups.
