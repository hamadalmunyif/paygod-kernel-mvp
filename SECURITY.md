# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Paygod Kernel seriously. If you discover a security vulnerability, please follow these steps:

1.  **Do NOT open a public GitHub issue.**
2.  Email our security team at `security@paygod.org`.
3.  Include a detailed description of the vulnerability and steps to reproduce it.
4.  We will acknowledge your report within 48 hours.

## Disclosure Policy
We follow a **Responsible Disclosure** policy:
*   We ask that you give us a reasonable amount of time (90 days) to fix the issue before making it public.
*   We will notify you when the fix is ready and coordinate the release of the advisory.
*   We will credit you in the release notes (unless you prefer to remain anonymous).

## Supply Chain Security
To ensure the integrity of the Paygod Kernel:
*   All releases are signed with **Cosign/Sigstore**.
*   We publish **SBOMs** (Software Bill of Materials) in CycloneDX format for every release.
*   The CI pipeline runs automated secret scanning (Gitleaks) and dependency checks.


## Ledger & Evidence Data Minimization (MVP policy)

**Ledger = immutable facts only, strictly non-PII.**  
**Evidence = references only (hashes, pointers, minimal metadata), never raw sensitive data.**

Requirements:
- Truth ledger entries MUST NOT contain PII, secrets, or raw payloads.
- Evidence in MVP MUST be stored as references (IDs/URIs) plus integrity material (hashes/attestations).
- Any sensitive content must remain outside the repo/ledger and be referenced only by pointer + hash.

Rationale:
- Minimizes breach impact.
- Enables deterministic verification without storing sensitive material.

## Branch Protection (required)

For the Security Gate to be **merge-blocking**, `main` must enforce **Required status checks**.
See `docs/SECURITY_ROADMAP.md` for exact check names and setup steps.
