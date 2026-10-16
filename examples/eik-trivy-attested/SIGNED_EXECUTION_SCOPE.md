# Dual-attested Trivy execution study — bounded witness

**Status:** first-party technical witness, DRAFT PR #121, not production authorization.

[Exact green run #38934075192](https://github.com/hamadalmunyif/paygod-kernel-mvp/actions/runs/38934075192) at `7077309aeebaeab7cb43c9f3f9d47cbba76eecfd`: Linux producer and Windows no-checkout receiver both succeeded.

The producer executed Trivy v0.75.0 against a pinned public Alpine image and recorded the *actual invoked* CLI arguments, scanner executable SHA256, version, exit status, report SHA256/length, and workflow branch/commit. GitHub Artifact Attestations signed the **raw report** and **execution-observation JSON** independently. Both signatures were validated with patched GitHub CLI and exact signer Workflow/ref/commit.

The research Pack's normalized input binds both `source_sha256` and `scan_execution_sha256`. Only the canonical Kernel created its `deny` receipt. The Windows job separately verified the GH attestations, PayGod integrity and the source/statement/input/receipt digest chain, and refused report, statement, bundle and semantic-input mutations. Seventeen hermetic malformed-execution-record negatives also passed.

**Limits:** A signed first-party report of observed execution is not independent proof of complete scan coverage, immutable runner process provenance, CVE accuracy, or vendor backports. The binary SHA is not itself publisher trust. GitHub already supplies native attestations and Trivy native blocking. The new PayGod binding is mechanically demonstrated but not proven commercially superior to these native controls.

The transferred external sidecars are **not inside** the Kernel's canonical manifest; receipt input hashes bind their digests, so a recipient must independently verify both sidecars and their native GitHub attestations. The expected PayGod receipt digest is producer-supplied. Verifier `valid` means scoped integrity, not issuer authority; replay and trusted time remain unverified.

No external independent organizational recipient, bank, production release, institutional signer, regulator acceptance, or eligible B2-REAL case participated. Keep issues #116 and #114 open. PR #121 stacks on #120, which stacks on #118. Preserve v1 CVSS Pack and RED #117. Do not merge or deploy without explicit owner review and any necessary ADR.
