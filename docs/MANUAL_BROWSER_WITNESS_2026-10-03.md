# Manual Browser Witness — 2026-10-03

## Scope

Manual recipient-side verification of the production browser verifier at:

`https://www.paygod.net/verifier/`

This witness is part of the Internal Rehearsal evidence. It is **not** an external pilot and does not prove market demand, issuer authorization, external evidence truth, policy replay, or trusted third-party time.

## Fixture

Transport profile: `paygod-demo-transport/1`

Receipt canonicalization profile: `paygod-c14n-v1`

Recorded synthetic decision:
- metric: `electricity_consumption`
- value: `420 kWh`
- rule: `review-consumption`
- verdict: `FLAG`

Commitments observed from the fixture:
- receipt SHA-256: `d019ae508d5d108bf959789d5e6ab212ae9d357ab08661cdbd0085efa8409cac`
- manifest SHA-256: `7e9b0eb366b6de06c70590145e146811fc3fd16222612afb2c7bfff2b12c528e`
- ledger head: `9315508573392cd79b9f5acf15b7ef117cd715ed770b3abb6f016c62b6091adb`

## Manual path

```text
Producer page
  -> download evidence bundle
  -> open separate /verifier/
  -> choose downloaded bundle
  -> run verification
```

The separate verifier opened empty and did not inherit producer state.

## Witness A — no external receipt pin

Observed:
- Integrity: `VERIFIED`
- Issuer authenticity: `NOT VERIFIED`
- Replay: `NOT PERFORMED`
- Time authority: `PRODUCER SUPPLIED`
- External receipt pin: `NOT PROVIDED`
- Checks: `11/11 passed`

## Witness B — correct external receipt pin

Expected receipt SHA-256 supplied manually through the separate verifier:

`d019ae508d5d108bf959789d5e6ab212ae9d357ab08661cdbd0085efa8409cac`

Observed:
- Integrity: `VERIFIED`
- External receipt pin: `MATCHED`
- Checks: `12/12 passed`

## Witness C — altered external receipt pin

One character of the expected receipt commitment was changed before re-verification.

Observed:
- Integrity: `FAILED`
- External receipt pin: `MISMATCH`
- Checks: `11/12 passed`
- Explicit failure: `External receipt commitment: check failed.`

## Conclusion

The production browser verifier demonstrated the intended two-way receipt-pin behavior:

```text
correct external commitment -> accept
altered external commitment -> fail closed
```

This witness establishes a manual mobile-browser path for:
- portable evidence handoff;
- independent browser integrity verification;
- external receipt commitment match;
- fail-closed rejection on commitment mismatch.

It does not upgrade issuer authenticity beyond `NOT VERIFIED`. That is the next cryptographic boundary addressed by the detached Ed25519 issuer-authentication profile.


## Witness D — recipient-supplied Ed25519 trust store

After the production verifier was upgraded to browser verifier v0.4, the same signed synthetic bundle was loaded in the separate verifier.

### D1 — signed bundle without recipient trust anchor

Observed:
- Integrity: `VERIFIED`
- Issuer authenticity: `NOT VERIFIED`
- Replay: `NOT PERFORMED`
- Time authority: `PRODUCER SUPPLIED`
- External receipt pin: `NOT PROVIDED`
- Issuer signature key id: `paygod-demo-issuer-2026-10-03`
- Issuer-signature reason: `no_trust_anchor_supplied`
- Integrity checks: `11/11 passed`

This shows that the presence of a detached signature does not let the evidence bundle nominate its own trust anchor.

### D2 — same signed bundle with recipient-supplied demo trust store

The recipient then loaded a separate `paygod-ed25519-trust-v1` trust store containing the demo public key and re-ran verification.

Observed:
- Integrity: `VERIFIED`
- Issuer authenticity: `VERIFIED`
- Replay: `NOT PERFORMED`
- Time authority: `PRODUCER SUPPLIED`
- External receipt pin: `NOT PROVIDED`
- Integrity checks: `11/11 passed`

The production browser UI explicitly reported that the detached receipt signature verified under a recipient-supplied trusted Ed25519 key.

### Interpretation boundary

This witness proves only that:
- the signed receipt commitment is unchanged;
- the detached Ed25519 signature validates;
- the verifying recipient supplied a public key that the verifier treated as trusted.

It does **not** prove:
- the external measurement is true;
- the demo key represents production PayGod authority;
- the signer is regulator-authorized;
- replay occurred;
- time is third-party trusted;
- execution is authorized.

The key used in this witness is explicitly a **demo/test key only**.

### Production identifiers

- kernel issuer-auth merge: `224d06fb32ee`
- website production commit: `8532995e4c50`
- production verifier: `https://www.paygod.net/verifier/`

## Updated conclusion

The 2026-10-03 production mobile-browser witnesses now cover:

```text
portable handoff
  -> independent integrity verification
  -> correct external receipt pin -> MATCH
  -> altered external receipt pin -> FAIL CLOSED
  -> signed bundle without recipient trust -> NOT VERIFIED
  -> signed bundle + recipient trust store -> ISSUER AUTHENTICITY VERIFIED
```

These are engineering witnesses for Internal Rehearsal readiness. They are not external-pilot evidence.
