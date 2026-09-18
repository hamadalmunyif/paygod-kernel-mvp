# Portable Evidence Witness

Status: **passed in CI and merged via PR #52**.

## Proven boundary

Paygod evidence can leave the environment that produced it and be independently verified from transferred artifacts without replaying the original decision.

The merged witness covers:

- artifact-only handoff between producer and verifier jobs;
- Linux producer -> Windows verifier;
- receipt, manifest/digest, and ledger verification where present;
- machine-readable verification output;
- fail-closed rejection after a one-byte evidence mutation;
- no change to kernel decision semantics or canonicalization rules.

```text
Environment A (producer)
        |
        | execute once
        v
Evidence bundle
        |
        | transfer artifacts only
        v
Environment B (verifier)
        |
        | no producer temp/workspace state
        | no hidden local configuration
        | no re-execution of the original decision
        v
VALID / INVALID
```

## Non-claims

This CI witness proves portability and integrity within its documented boundary. It does **not** prove:

- truth or authenticity of an external real-world fact;
- a published/signed external verifier trust root;
- an external-device/party witness outside repository CI;
- a live financial execution integration.

Integrity is not provenance.
