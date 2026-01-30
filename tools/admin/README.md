# Admin utilities

These scripts **do not run in CI**. They are intended for repository admins to apply settings
that cannot be enforced purely via git-tracked files.

## enable_branch_protection.sh

Enables PR gating on `main` by turning on Branch Protection required checks.

### Prerequisites
- GitHub CLI (`gh`)
- `jq`
- Repo admin rights

### Usage
```bash
export REPO="OWNER/REPO"
export BRANCH="main"
gh auth login
./tools/admin/enable_branch_protection.sh
```

> Required checks must match the **job names** shown in GitHub Actions.
