# EIK reference: saved GitHub Actions report → admission → Kernel → recipient

**Status:** Experimental runnable reference on this PR, **synthetic fixtures only**. No GitHub API/scanner integration, live monitoring, deployment gate, payment, production release authorization, completed external institutional review, or sourced fact certification.

This reference tests a complete developer flow using the **existing** PayGod CLI. It is not an EIK SDK or general-purpose GitHub connector. A maintainer or coding agent can replicate it with no PayGod account or upstream PR. The user can keep a local Pack private.

## Contract and exact trust boundaries

1. **Source:** a saved, explicitly labeled synthetic CI-scan JSON document. Its raw bytes and SHA-256 are preserved in the **producer workspace**, outside the canonical evidence directory. The fixture reports `run_state=completed`, `scanner_result=ok`, `scanner_exit_code=0`, `report_complete=true`, a pinned 40-character hex revision and nonnegative integer finding counts. This is a **declared** completion state, not independent proof that a real scanner ran.
2. **Admission:** `eik_reference.py` rejects missing/invalid/failed saved reports, duplicate JSON keys, numeric floats, false typed counts, contradictory counts and unrecognized fixture types. `tools/eik_admit.py` then checks the generated input against the Pack's required, typed shape. If either fails, `WITHHELD_NOT_RUN` is an **external orchestration outcome** and the Kernel is not called.
3. **Kernel:** once structurally admissible, the script invokes the published `PayGod.Cli run` with the example Pack. The **Kernel alone** creates the `allow`/`deny` verdict and the manifest/ledger/receipt/bundle identity. A producer-supplied clock is required for this deterministic demonstration.
4. **Handoff:** upload **only** `eik-output/evidence/` to the receiving job, not its sibling source/admission files. A separate job output supplies the expected receipt SHA-256 as an **untrusted producer-supplied comparison commitment**. A trusted independent out-of-band commitment would require a separate authenticated delivery channel.
5. **Verifier:** a Windows recipient job with **no source checkout** downloads the canonical evidence and standalone verifier source; it performs an integrity check without replaying Kernel. `valid` is not a claim of external source truth, authentic organizational release, trusted time or independent recipient acceptance.

## Quickstart (repo root; Linux/macOS)

Requires .NET SDK 8, Python 3.11+ and standard Python requirements. Do not reuse an existing output directory.

```bash
python3 -m pip install -r tools/requirements.txt
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
dotnet run --project src/PayGod.Cli -- test --pack examples/eik-github-actions/pack

export PAYGOD_CLOCK=2026-10-14T00:00:00Z  # producer supplied, not a trusted timestamp
export PAYGOD_STRICT=1
python3 examples/eik-github-actions/eik_reference.py \
  --source examples/eik-github-actions/fixtures/clean.json \
  --cli ./out/PayGod.Cli \
  --out eik-output

python3 tools/verify_portable_evidence.py eik-output/evidence \
  --expect-receipt-sha256 "$(sha256sum eik-output/evidence/receipt.json | cut -d' ' -f1)" \
  --result eik-verification.json

python3 tools/test_eik_github_reference.py --cli ./out/PayGod.Cli
```

The printed producer digest above is **not an independent authenticated pin**. For real cross-party evidence, the recipient must obtain the expected digest through an appropriately authenticated separate channel. The producer example does not prove the correctness of its own scanner observations.

On Windows, use the PowerShell equivalent to set `PAYGOD_CLOCK` and calculate the SHA-256; the GitHub Actions reference uses Windows in the recipient step.

## Test matrix

| Saved source | Before Kernel | Canonical output | Scoped recipient |
| --- | --- | --- | --- |
| `clean.json` | structural/admission pass | `allow` for synthetic zero findings | integrity valid |
| `findings.json` | structural/admission pass | `deny` for synthetic findings | integrity valid |
| `failed-zero.json` | `WITHHELD_NOT_RUN` | **no** receipt/bundle | not run |
| `missing.json` | `WITHHELD_NOT_RUN` | **no** receipt/bundle | not run |
| absent source file | `WITHHELD_NOT_RUN` | **no** receipt/bundle | not run |
| one-byte change after receipt | no new authority | existing bundle modified | verifier rejects |
| wrong separately supplied receipt SHA | no new authority | otherwise valid bundle | verifier rejects |

Run locally with the explicit test script above or inspect [the optional GitHub Actions workflow](../../.github/workflows/eik-reference.yml). In CI, the reference is tested without outside API access or secrets; no upstream project is modified.

## Native alternative and falsifier

GitHub required reviews, environment protections and artifact attestations may already address most release/evidence requirements. This example does **not** check or replace them, and an `allow` policy verdict is **never authorization to deploy**.

Evidence that would justify work beyond this fixture: an unfamiliar authorized developer/coding agent completes the exercise without project-operator intervention, its missing-source cases remain withheld, a genuine **saved read-only source report** can be represented without fabricating completion, and an independent recipient can explain the exact trust ceiling. Then compare against direct CLI and GitHub-native attestation/protection in setup time, interventions, false admissions and recipient understanding. Those metrics have **not yet been measured** here.

This reference cannot be promoted to production evidence admission without authenticated source retrieval, versioned scanner result semantics and failure exit codes, complete coverage/permissions, explicit deployment authorization and a specific reliance context. Existing [Issue #111](https://github.com/hamadalmunyif/paygod-kernel-mvp/issues/111) also tracks unsafe generic policy-expression coercion; **do not bypass admission by calling `run` with unchecked third-party inputs**.

**Build privately · Verify independently · Contribute optionally.**
