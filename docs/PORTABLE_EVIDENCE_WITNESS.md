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
- the historical witness did not change kernel decision semantics; canonicalization is subsequently repaired/versioned by v0.5.1.

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
integrity verified / failed
```

## Non-claims

This CI witness proves portability and bundle integrity within its documented boundary. A successful integrity result does not imply issuer authenticity, replay, trusted time, or external truth. It does **not** prove:

- truth or authenticity of an external real-world fact;
- a published/signed external verifier trust root;
- an external-device/party witness outside repository CI;
- a live financial execution integration.

Integrity is not provenance.
