\# Gates



\## Main branch merge gates



To merge into `main`, the following must pass:



\- \*\*BAP Proof Seal\*\* (GitHub Actions)

&nbsp; - `pass\*.json` examples under `packs/\*\*/examples` must validate.

&nbsp; - `fail\*.json` examples under `packs/\*\*/examples` must be rejected.

&nbsp; - Proof artifacts are uploaded by the workflow.




- **Pack Contract Gate** (GitHub Actions)
  - All pack.yaml under packs/** (excluding _drafts) must validate against contracts/schemas/pack.schema.json.

- **Repository Entry Point**
  - START_HERE.md is the canonical onboarding document for developers.
