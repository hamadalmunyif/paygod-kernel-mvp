# Security Policy & Governance Boundary Contract

## Architectural Governance

Security and architectural merge witnesses are evaluated independently within the repository CI boundary.

- The current `main` development boundary is subject to the repository's active required CI and security gates.
- A passing integrity or authenticity witness establishes only the property and scope explicitly tested by that witness.
- Integrity does not establish provenance, external truth, regulatory authorization, or production fitness.
- Production support lifecycle commitments, externally attested release provenance, institutional key-distribution governance, and independent release-signing infrastructure have not yet been declared or proven.

## Current Security Testing Boundary

Current automated security evaluation applies to the code and artifacts exercised by the active `main` branch CI contract.

Historical artifacts are outside the current main-branch assurance boundary unless explicitly covered by a maintained regression witness.

## Current Proven Claims

The repository currently includes automated witnesses for areas including:

- source/build regression testing;
- dependency and source-code security scanning;
- repository-boundary enforcement;
- portable evidence integrity verification;
- fail-closed tamper rejection;
- detached Ed25519 receipt authentication against a recipient-supplied trust store.

Each witness remains bounded by its documented non-claims.

## Not Yet Proven

The repository does not currently claim:

- production-grade release provenance through GitHub Artifact Attestations;
- universal Cosign/Sigstore release signing;
- institutional key rotation or revocation governance;
- regulator authorization;
- production operational fitness;
- commercial support lifecycle guarantees.

## Reporting a Vulnerability

We take the security of Paygod Kernel seriously. If you discover a security vulnerability:

1. **Do NOT open a public GitHub issue.**
2. Email `security@paygod.org`.
3. Include a detailed description of the vulnerability and steps to reproduce it.
4. Allow reasonable time for investigation and remediation before public disclosure.

## Disclosure Policy

We follow a responsible-disclosure process:

- Please avoid public disclosure while a reported vulnerability is being investigated and remediated.
- We will coordinate disclosure when a fix is available.
- Reporter credit may be included unless anonymity is requested.

## Ledger & Evidence Data Minimization

**Ledger = immutable decision facts only, strictly non-PII.**  
**Evidence = references only (hashes, pointers, minimal metadata), never raw sensitive data.**

Requirements:

- Ledger entries MUST NOT contain PII, secrets, or raw payloads.
- Evidence in the current MVP boundary MUST be stored as references (IDs/URIs) plus integrity material (hashes/attestations).
- Sensitive source material must remain outside the repository and ledger and be represented only by the minimum required reference/commitment material.

Rationale:

- minimizes breach impact;
- preserves the decision-evidence boundary;
- enables deterministic verification without storing sensitive source payloads.

## Required Merge Governance

The canonical required merge-witness contract is defined in [GATES.md](GATES.md).

A witness intended to be required MUST report a terminal status on every pull request targeting `main`. The effective GitHub ruleset and the written contract in `GATES.md` must remain aligned. Ruleset drift is a governance defect.
