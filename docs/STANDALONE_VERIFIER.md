# Standalone Third-Party Verifier Witness

## Objective

Prove that a party outside the Paygod producer environment can verify a transferred Paygod evidence bundle without checking out `paygod-kernel-mvp`, rebuilding the kernel, re-running the pack, or possessing producer-local state.

This is the next portability boundary after PR #52 proved artifact-only cross-OS verification inside CI.

## Trust boundary

The verifier receives only:

1. an evidence bundle produced by Paygod; and
2. a standalone verifier distribution whose integrity/version can be identified independently.

It MUST NOT require:

- a checkout of `paygod-kernel-mvp`;
- the producer workspace or temporary files;
- Docker;
- the .NET SDK;
- re-execution of the original pack or decision;
- Paygod secrets or hidden configuration.

## Verification contract

For an untampered bundle the verifier must return `VALID` and machine-readable results covering, where present:

- manifest integrity;
- artifact SHA-256 digests;
- bundle digest binding;
- receipt-to-manifest binding;
- ledger hash-chain integrity.

For a bundle changed after production, verification must return `INVALID` with a non-zero process result or an equivalent fail-closed browser result.

## Distribution target

The first implementation should be a self-contained verifier artifact. A browser/client-side verifier is the preferred follow-on distribution because it can run on an iPad and later be served from a surface such as `verify.paygod.net` without making that domain the source of trust.

The verifier must remain useful if the web surface is unavailable: the evidence format and verification rules are the trust primitive, not the hosting domain.

## Acceptance witness

```text
Paygod producer
      |
      v
 evidence bundle
      |
      +------------------------+
                               |
                    standalone verifier
                               |
                               v
                      VALID / INVALID
```

Acceptance requires both:

1. clean evidence -> `VALID`;
2. one-byte tamper -> `INVALID`.

## Non-claims

PR #52 established a Linux-producer to Windows-verifier artifact-only CI witness. This work does not claim third-party/P4 verification until the standalone distribution is built and the acceptance witness passes without repository checkout.
