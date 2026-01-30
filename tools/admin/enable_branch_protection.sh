#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_TOKEN:?Set GITHUB_TOKEN (or use gh auth login)}"
: "${REPO:?Set REPO as owner/name, e.g. acme/paygod-kernel}"
: "${BRANCH:=main}"

# This script enables strict PR gating on the protected branch using GitHub's REST API via `gh`.
# Requires: GitHub CLI (gh) and sufficient repo admin rights.

# Required status checks (MUST match job names exactly)
REQUIRED_CHECKS=(
  "CodeQL (C#)"
  "Dependency Review (PR)"
  "Secret Scan (gitleaks)"
  "SBOM (PR artifact)"
  "CI"
)

echo "Enabling branch protection for ${REPO}:${BRANCH}"
echo "Required checks:"
printf ' - %s
' "${REQUIRED_CHECKS[@]}"

# Build JSON payload for required status checks
checks_json=$(printf '%s
' "${REQUIRED_CHECKS[@]}" | jq -R . | jq -s '{strict:true, contexts:.}')

# Enable protection with required PR reviews + required status checks.
# Note: You can tweak review requirements below to match your governance.
gh api -X PUT "repos/${REPO}/branches/${BRANCH}/protection" \
  -H "Accept: application/vnd.github+json" \
  -f required_status_checks="$(echo "${checks_json}")" \
  -f enforce_admins=true \
  -f required_pull_request_reviews.dismiss_stale_reviews=true \
  -f required_pull_request_reviews.required_approving_review_count=1 \
  -f required_pull_request_reviews.require_code_owner_reviews=true \
  -f restrictions='null'

echo "Done. Verify in GitHub: Settings -> Branches -> Branch protection rules."
