# Standalone Third-Party Verifier Witness

Status: **standalone/no-checkout baseline originated in PR #53; current verifier v0.2 adds decision-critical receipt, manifest-locked ledger, Unicode, malformed-input, and default-clock compatibility witnesses.**

## Proven boundary

Inside CI, a recipient can verify a transferred Paygod evidence bundle using a versioned standalone verifier artifact without checking out `paygod-kernel-mvp`, rebuilding the kernel, re-running the pack, or possessing producer-local state.

The verifier checks:

- manifest integrity;
- artifact SHA-256 digests and byte counts;
- bundle-digest binding;
- exactly one manifest-locked `ledger.jsonl`;
- receipt-to-manifest binding;
- ledger hash-chain integrity;
- decision-critical receipt claims against the locked ledger;
- canonical `allow`, `deny`, `flag`, and `error` verdicts are ledger-bound;
- required decision fields and their types are validated before equality/binding checks.

Acceptance requires clean evidence -> `VALID`, payload tamper -> `INVALID`, decision-critical receipt tamper -> `INVALID`, a missing manifest-locked ledger -> `INVALID`, fail-closed behavior, and machine-readable results. Verifier v0.2 cross-checks receipt verdict/rule/reason, pack, input hash, and, when `PAYGOD_CLOCK` is injected, decision time against the locked manifest/ledger. For the supported non-strict local path where the receipt clock is `unset`, acceptance requires the verifier operator to pass `--allow-unbound-clock` explicitly. The result records `clock_binding: unbound-opt-in`; default verification rejects `unset`, preventing a receipt-only downgrade from an injected clock to an unbound clock. Manifest/ledger time consistency is still checked.

## Trust boundary

The recipient receives only:

1. an evidence bundle produced by Paygod; and
2. a standalone verifier distribution whose version/integrity metadata can be checked.

The recipient witness does not require repository checkout, producer workspace state, Docker, the .NET SDK, original pack replay, Paygod secrets, or hidden producer configuration.

## Next distribution boundary

The next gate is to package and test the verifier **outside repository CI** on an independent device/environment with published integrity/version metadata. Verifier v0.2 does not authenticate the runner/issuer identity by itself; that remains part of the external trust-root/provenance boundary.

A browser/client-side verifier may follow for iPad use and a future surface such as `verify.paygod.net`, but the hosting domain must not become the source of trust.

## Non-claims

PR #53 establishes a CI-level standalone/no-checkout verification witness. It does **not** yet establish:

- a published/signed external verifier trust root;
- a truly external device/party witness;
- truth or provenance of external evidence;
- institutional adoption or a live financial release workflow.

Do not describe this boundary as full external P4 until the external distribution witness passes.
