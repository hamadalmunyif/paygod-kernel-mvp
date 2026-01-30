#!/usr/bin/env python3
"""
Lint: forbid provider-specific indicators in packs/core/**.

Policy:
- Core packs must be cloud-agnostic. Provider-specific packs must live under packs/providers/<cloud>/...

This script scans selected files under packs/core and fails if it finds provider tokens.

Allowlist:
- Repo-root file: .paygod-provider-lint-allowlist
- Lines:
  - <glob>                      # ignore whole file
  - <glob>::<token>             # allow a specific token in matching files

Config:
- tools/ci/provider_lint_config.json
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class AllowRule:
    glob: str
    token: Optional[str]  # None => ignore file entirely


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_config(repo: Path) -> dict:
    cfg_path = repo / "tools" / "ci" / "provider_lint_config.json"
    if not cfg_path.exists():
        return {}
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def _load_allowlist(repo: Path, allowlist_rel: str) -> List[AllowRule]:
    path = repo / allowlist_rel
    if not path.exists():
        return []
    rules: List[AllowRule] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "::" in line:
            g, t = line.split("::", 1)
            rules.append(AllowRule(glob=g.strip(), token=t.strip().lower()))
        else:
            rules.append(AllowRule(glob=line, token=None))
    return rules


def _is_allowed(allow: List[AllowRule], rel_path: str, token: str) -> bool:
    token_l = token.lower()
    for rule in allow:
        if fnmatch(rel_path, rule.glob):
            if rule.token is None:
                return True
            if rule.token == token_l:
                return True
    return False


def _compile_token_regex(token: str) -> re.Pattern:
    t = token.strip()
    if not t:
        raise ValueError("Empty token")
    if re.search(r"\W", t):
        return re.compile(re.escape(t), re.IGNORECASE)
    return re.compile(rf"(?<![A-Za-z0-9_]){re.escape(t)}(?![A-Za-z0-9_])", re.IGNORECASE)


def _iter_target_files(repo: Path, include_globs: List[str], exclude_globs: List[str]) -> Iterable[Path]:
    core = repo / "packs" / "core"
    if not core.exists():
        return []
    files: List[Path] = []
    for pat in include_globs:
        files.extend(core.glob(pat))
    uniq = []
    seen = set()
    for f in files:
        if f.is_file() and f not in seen:
            seen.add(f)
            uniq.append(f)
    def is_excluded(rel: str) -> bool:
        return any(fnmatch(rel, g) for g in exclude_globs)
    return [f for f in uniq if not is_excluded(str(f.relative_to(repo)).replace("\\", "/"))]


def main() -> int:
    repo = _repo_root()
    cfg = _load_config(repo)

    tokens: List[str] = cfg.get("tokens", [])
    if not tokens:
        tokens = [
            "aws", "arn", "eks", "iam", "sts",
            "azure", "aks", "entra", "aad",
            "gcp", "gke", "google",
            "cloudformation", "terraform",
        ]

    include_globs: List[str] = cfg.get("include_globs", ["**/pack.yaml", "**/tests/cases.yaml"])
    exclude_globs: List[str] = cfg.get("exclude_globs", [
        "**/README.md",
        "**/*.md",
    ])

    allowlist_rel: str = cfg.get("allowlist_file", ".paygod-provider-lint-allowlist")
    allow_rules = _load_allowlist(repo, allowlist_rel)

    token_re = [(t, _compile_token_regex(t)) for t in tokens]

    violations: List[Tuple[str, str, int, str]] = []

    for file_path in _iter_target_files(repo, include_globs, exclude_globs):
        rel = str(file_path.relative_to(repo)).replace("\\", "/")
        text = file_path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            for token, rx in token_re:
                if rx.search(line):
                    if _is_allowed(allow_rules, rel, token):
                        continue
                    violations.append((rel, token, i, line.strip()))

    if violations:
        print("❌ Provider-specific indicators found in packs/core. Move the pack to packs/providers/<cloud>/ or allowlist explicitly.\n")
        for rel, token, lineno, snippet in violations[:200]:
            print(f"- {rel}:{lineno}: token='{token}' :: {snippet}")
        if len(violations) > 200:
            print(f"... and {len(violations) - 200} more")
        print(f"\nAllowlist file: {allowlist_rel}")
        return 1

    print("✅ Provider lint passed: packs/core is cloud-agnostic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
