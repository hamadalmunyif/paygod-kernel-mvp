# Dual-attested Trivy execution study — bounded witness

**Status:** first-party technical witness, DRAFT PR #121, not production authorization.

[Exact green run #38934075192](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38934075192) at `7077309aeebaeab7cb43c9f3f9d47cbba76eecfd`: Linux producer and Windows no-checkout receiver both succeeded.

The producer executed Trivy v0.75.0 against a pinned public Alpine image and recorded the *actual invoked* CLI arguments, scanner executable SHA256, version, exit status, report SHA256/length, and workflow branch/commit. GitHub Artifact Attestations signed the **raw report** and **execution-observation JSON** independently. Both signatures were validated with patched GitHub CLI and exact signer Workflow/ref/commit.

The research Pack's normalized input binds both `source_sha256` and `scan_execution_sha256`. Only the canonical Kernel created its `deny` receipt. The Windows job separately verified the GH attestations, PayGod integrity and the source/statement/input/receipt digest chain, and refused report, statement, bundle and semantic-input mutations. Seventeen hermetic malformed-execution-record negatives also passed.

**Limits:** A signed first-party report of observed execution is not independent proof of complete scan coverage, immutable runner process provenance, CVE accuracy, or vendor backports. The binary SHA is not itself publisher trust. GitHub already supplies native attestations and Trivy native blocking. The new PayGod binding is mechanically demonstrated but not proven commercially superior to these native controls.

The transferred external sidecars are **not inside** the Kernel's canonical manifest; receipt input hashes bind their digests, so a recipient must independently verify both sidecars and their native GitHub attestations. The expected PayGod receipt digest is producer-supplied. Verifier `valid` means scoped integrity, not issuer authority; replay and trusted time remain unverified.

No external independent organizational recipient, bank, production release, institutional signer, regulator acceptance, or eligible B2-REAL case participated. Keep issues #116 and #114 open. PR #121 stacks on #120, which stacks on #118. Preserve v1 CVSS Pack and RED #117. Do not merge or deploy without explicit owner review and any necessary ADR.

## Later same-commit cross-run isolation evidence — 2026-10-16

The first green run above is preserved as a dated earlier witness. A subsequent [**both-green run #38945282939**](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38945282939) at exact source SHA `5b7b48d3d5216c020b31e25094bd34e83c39d0a7` added a separate comparison of `workflow_run_id` and `workflow_run_attempt` to caller-provided **expected** values in BOTH the bridge and Windows no-checkout recipient, in addition to the GitHub-native signature signer/ref/commit checks. The hermetic matrix now covers **23 negative cases** (including wrong expected run and attempt), plus live receiver negative replacements. The [Pack Contract Gate](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38945290261) also passed at that source SHA.

This is a **first-party same-workflow** consistency check. The expected run ID and attempt in this test are supplied by OUR GitHub Actions execution context, **not** an external authority; the expected PayGod Receipt SHA still comes from our producer job. The [pre-existing neutral recipient E-004 protocol](NEUTRAL_RECIPIENT_PROTOCOL.md) now explicitly asks an unrelated reviewer to obtain these expected references independently and to measure the value, if any, over Trivy+GitHub's native equivalents.

The run's short-retention public-image artifacts are [source+canonical evidence #12065506509](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38945282939/artifacts/12065506509) and [verifier code #12065252168](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38945282939/artifacts/12065252168). No external recipient yet; no production issue or native-only value claim is closed by this test.


## 2026-10-16 — Hidden Trivy configuration isolation, adversarial workflow witness

**New current measured source SHA before this documentation append:** `516152e33b4713a12312fe86f8e61499cf456d2a`. [Full Linux+Windows successful GitHub Actions run #38958628395](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38958628395) and same-source [Pack Contract Gate](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs?query=branch%3Aresearch%2Ftrivy-signed-execution-statement-20261016) succeeded.

**Problem addressed:** Trivy can inherit settings from `TRIVY_*` environment variables and local `trivy.yaml`/`.trivyignore` files, potentially filtering findings despite an apparently unfiltered CLI command. Official documentation: [Trivy Configuration](https://trivy.dev/docs/dev/docs/configuration/).

- The `scan_capture.py` research subprocess now **removes inherited `TRIVY_*` environment variables** and invokes `--config=`, `--ignorefile=`, `--secret-config=` to suppress default file-sourced policies/filters. The capture records the names, *not secret values*, of scrubbed environment keys and an explicit `config_isolation_mode` string in the **separately GitHub-signed** execution statement.
- The receiver's typed `execution_statement.py` requires exactly those CLI arguments and the isolation contract, and rejects unknown or malformed environment key names. The synthetic negative matrix now runs **26 negatives** against command, source, run, severity overrides, configuration record and contract fields.
- The public-image Actions workflow deliberately injects **`TRIVY_SEVERITY=LOW`** into the Trivy invocation step as a negative control. It still observes 21 findings including **2 HIGH**, and canonical Kernel issues **`deny`**, which is inconsistent with an effective inherited LOW-only filter. This is a bounded first-party test of the scrubbing path, **not a universal proof no other source-specific filter exists**.
- At the successful source SHA: raw Trivy report SHA-256 `45cd425c69872e40eef6eb06180a89f4ac9c61b2023e17d6e66a7608c168991f`; scanner binary SHA-256 `93f9da8e4ba5e0c1c76d8234ed2494cf9afb0a96fd21953e424bb795f3299b8e`; actual canonical **`deny`** receipt SHA-256 `a1b4b76b5f51d2682ce8ac86bad5a126b55f34de19eeadafa5556da1ae8dbfd9`. Windows no-checkout recipient independently revalidated GitHub source/statement attestations, scoped PayGod integrity and source→execution→canonical input→receipt binding. Source/evidence [artifact #12071871496](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38958628395/artifacts/12071871496), verifier [artifact #12071482200](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38958628395/artifacts/12071482200); seven-day artifact retention.
- Native-only Trivy severity blocking and GitHub's own source attestation remain the baseline. The incremental case for a PayGod policy decision/receipt must be established by a **neutral recipient** with independently pinned issuer/policy/receipt expectations; that experiment remains **NOT RUN**.

**Still not established:** independently attested scanner process integrity, scanner release/supply chain publisher trust or vulnerability database state, guarantee of full package/advisory coverage, verified issuer authenticity/trusted time/replay, a legally authorized release, external recipient or commercial value. The signed record is a first-party observation, not an independently certified complete scan. Issue #116 remains OPEN; do not promote old numeric-CVSS Pack v1 or automatically merge research PRs #118 → #120 → #121.

