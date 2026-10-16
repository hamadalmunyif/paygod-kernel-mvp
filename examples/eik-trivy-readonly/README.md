# Trivy → PayGod: read-only shadow admission experiment

**Status: HARNESS_ONLY / NOT A SCANNER CONNECTOR / NOT A CANONICAL KERNEL DECISION / NOT A RELEASE GATE**  
Origin: [Issue #116](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/116). Comparison witness: [RED PR #117](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/117).  
Owner basis: `main@d347213848f03a6d25554631d0183a682879b11b`.

## Why this exists

The existing `critical-cve-blocker` v1 policy checks `v.status != 'fixed'`. According to Trivy maintainer's explanation [discussion #11021](https://github.com/aquasecurity/trivy/discussions/11021), `Status=fixed` means **a fix is available from the advisory**, not that the installed package is fixed. This specific false-`allow` was reproduced via an intentionally RED **synthetic** Pack case in PR #117 (`Expected deny, Got allow`).

Trivy itself documents that JSON vulnerability fields `VulnerabilityID`, `PkgName`, `InstalledVersion` and `Severity` are populated in reported findings, while `FixedVersion` and other fields can be empty. See [Trivy reporting](https://trivy.dev/docs/latest/guide/configuration/reporting/) and [vulnerability analysis](https://trivy.dev/docs/latest/guide/scanner/vulnerability/).

## What the example actually does

`tools/eik_trivy_shadow.py` consumes a **saved** Trivy JSON report with a caller-supplied expected artifact and claimed scanner exit code. It enforces a bounded JSON/schema sanity check, refuses obvious filters (e.g. `--ignore-unfixed` and `--severity`), requires subject digest identity to match `Metadata.RepoDigests`, preserves every finding's raw `trivy_status` and `InstalledVersion`, and emits only a **non-authoritative diagnostic**.

Three possible states:
- `SHADOW_BLOCK_CANDIDATE`: reported high/critical finding, including when `Status=fixed`. **Not** a PayGod `deny`, and not a calculated CVSS-specific policy result.
- `WITHHELD_NOT_RUN`: invalid, unknown, incomplete, unbound or unproved input. **No Kernel invocation**, no PayGod receipt. Can include a clean-looking report that lacks independent proof of complete scanning.
- There is intentionally **no `allow` or `fixed_verified` output**, including for a zero-finding report. The script cannot authenticate provenance or completeness of a saved scan.

The script's exit code `0` means a JSON **diagnostic** was returned; it is **never release permission**. The `source_attested` output is always `false`. A report hash is only local byte integrity, not genuine scanner execution, report freshness or subject correctness.

## Command (research only)

```bash
python3 tools/eik_trivy_shadow.py \
  --report /path/to/saved-trivy-image.json \
  --expected-artifact 'registry.example/app@sha256:<64-lowercase-hex-digest>' \
  --scanner-exit-code 0 \
  --scanner-arg=image \
  --scanner-arg=--format=json
```

The example assumes Trivy JSON SchemaVersion `2` and a pinned `ArtifactName` appearing identically in `Metadata.RepoDigests`; real-world Trivy formats and scanners vary. Unsupported reports **remain withheld**, rather than being normalized by guessing. The CLI flags are supplied by the caller and **do not prove** what Trivy really executed.

Run hermetic synthetic test:

```bash
python3 tools/test_eik_trivy_shadow.py
```

## Why this is not the production fix

This code neither modifies `packs/core/critical-cve-blocker/pack.yaml` nor calls `PolicyEngine` or `RunCommand`. It does not establish that a package is fixed, does not compare package versions lexicographically, and does not upgrade historical receipts. It is a falsification/contract experiment under ADR 0003.

To progress:
1. Acquire genuine **permissioned** saved Trivy report **plus separately authenticated producer completion, immutable subject digest, unfiltered args and exit code**. Preserve raw source bytes.
2. Document actual scanner output version/schema and vendor advisory/backport semantics. Distinguish source `trivy_status` from any *externally proven* remediation state.
3. Propose a **new versioned Pack** and admission contract. Compare native Trivy output + GitHub attestations to PayGod's purported additional value.
4. Test cross-system source/subject swaps, filtered scans, tampering, null/unknown CVSS, duplicate keys, and third-party receiver. No local normalization may issue receipts, invented decisions or `allow`.
5. Use a separate ADR and canonical Kernel PR with protected CI; seek owner's explicit merge/release approval. Issue #116 is not closed by this example.

This synthetic shadow experiment may run in parallel with the optional typed-policy proposal [PR #115](https://github.com/hamadalmunyif/paygod-kernel-mvp/pull/115); neither depends on approval of the other.
