import json
import os
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def iter_pack_yamls(packs_root: Path, include_drafts: bool):
    for p in packs_root.rglob("pack.yaml"):
        # normalize path parts
        parts = [x.lower() for x in p.parts]
        if not include_drafts and ("_drafts" in parts):
            continue
        yield p


def main():
    repo_root = Path(os.environ.get("GITHUB_WORKSPACE", Path.cwd())).resolve()

    # allow args:
    include_drafts = "--include-drafts" in sys.argv

    schema_path = repo_root / "contracts" / "schemas" / "pack.schema.json"
    packs_root = repo_root / "packs"

    if not schema_path.exists():
        print(json.dumps({"ok": False, "code": "SCHEMA_MISSING", "message": f"Missing schema: {schema_path}"}))
        return 2

    if not packs_root.exists():
        print(json.dumps({"ok": False, "code": "PACKS_DIR_MISSING", "message": f"Missing packs dir: {packs_root}"}))
        return 2

    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)

    pack_files = list(iter_pack_yamls(packs_root, include_drafts=include_drafts))
    if not pack_files:
        print(json.dumps({"ok": False, "code": "NO_PACKS_FOUND", "message": "No pack.yaml found under packs/"}))
        return 2

    errors = []
    for pack_path in pack_files:
        try:
            doc = load_yaml(pack_path)
        except Exception as e:
            errors.append({
                "file": str(pack_path.relative_to(repo_root)).replace("\\", "/"),
                "code": "YAML_PARSE_ERROR",
                "message": str(e),
            })
            continue

        if doc is None:
            errors.append({
                "file": str(pack_path.relative_to(repo_root)).replace("\\", "/"),
                "code": "YAML_EMPTY",
                "message": "YAML is empty",
            })
            continue

        v_errors = sorted(validator.iter_errors(doc), key=lambda e: e.path)
        if v_errors:
            for e in v_errors:
                errors.append({
                    "file": str(pack_path.relative_to(repo_root)).replace("\\", "/"),
                    "code": "SCHEMA_VALIDATION_ERROR",
                    "path": "/".join([str(x) for x in e.path]),
                    "message": e.message,
                })

    if errors:
        print(json.dumps({"ok": False, "code": "PACK_CONTRACT_FAILED", "errors": errors}, ensure_ascii=False, indent=2))
        return 2

    print(json.dumps({"ok": True, "message": f"VALID: {len(pack_files)} pack.yaml files"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
