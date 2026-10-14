#!/usr/bin/env python3
"""Optional EIK structural preflight. NOT source authentication or a Kernel verdict.

For a Pack that declares explicit required input schemas, reject malformed or
missing typed data before any operator invokes the canonical PayGod CLI.
This command never calls Kernel, consumes external credentials, or writes a receipt.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


def emit(status: str, code: str, detail: str) -> int:
    print(json.dumps({
        "check": "eik-structural-input-v0",
        "status": status,
        "code": code,
        "detail": detail,
        "kernel_invoked": False,
        "source_authenticity": "not_verified",
        "source_completion": "not_verified",
        "execution_authorization": "not_verified",
    }, ensure_ascii=False))
    return 0 if status == "STRUCTURAL_ONLY_PASS" else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()

    try:
        pack = yaml.safe_load((args.pack / "pack.yaml").read_text(encoding="utf-8-sig"))
        input_data = json.loads(
            args.input.read_text(encoding="utf-8-sig"),
            parse_constant=lambda literal: (_ for _ in ()).throw(
                ValueError(f"Non-JSON numeric literal: {literal}")
            ),
        )
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return emit("WITHHELD_NOT_RUN", "INPUT_OR_PACK_UNREADABLE", str(exc))

    if not isinstance(pack, dict) or not isinstance(pack.get("spec"), dict):
        return emit("WITHHELD_NOT_RUN", "PACK_DECLARATION_MISSING", "No valid Pack spec")
    declarations = pack["spec"].get("inputs")
    if not isinstance(declarations, list) or not declarations:
        return emit("WITHHELD_NOT_RUN", "INPUT_SCHEMA_MISSING", "No declared typed Pack inputs")
    if not isinstance(input_data, dict):
        return emit("WITHHELD_NOT_RUN", "INPUT_NOT_OBJECT", "Input root must be an object")

    declared = set()
    for item in declarations:
        if not isinstance(item, dict):
            return emit("WITHHELD_NOT_RUN", "INPUT_DECLARATION_INVALID", "Input declaration is not an object")
        name = item.get("name")
        schema = item.get("schema")
        if not isinstance(name, str) or not name or name in declared:
            return emit("WITHHELD_NOT_RUN", "INPUT_DECLARATION_INVALID", "Missing or duplicate input name")
        declared.add(name)
        if not isinstance(schema, dict) or schema.get("type") != "object":
            return emit("WITHHELD_NOT_RUN", "INPUT_SCHEMA_INSUFFICIENT", f"{name}: requires explicit object schema")
        required = schema.get("required")
        if not isinstance(required, list) or not required or not all(
            isinstance(prop, str) and prop for prop in required
        ):
            return emit("WITHHELD_NOT_RUN", "INPUT_SCHEMA_INSUFFICIENT", f"{name}: required fields not declared")
        properties = schema.get("properties")
        if not isinstance(properties, dict) or any(
            prop not in properties
            or not isinstance(properties[prop], dict)
            or not isinstance(properties[prop].get("type"), str)
            for prop in required
        ):
            return emit("WITHHELD_NOT_RUN", "INPUT_SCHEMA_INSUFFICIENT", f"{name}: required fields lack explicit types")
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            return emit("WITHHELD_NOT_RUN", "INPUT_SCHEMA_INVALID", f"{name}: {exc}")
        if name not in input_data:
            return emit("WITHHELD_NOT_RUN", "REQUIRED_INPUT_MISSING", f"{name}: source observation absent")
        errors = list(Draft202012Validator(schema).iter_errors(input_data[name]))
        if errors:
            return emit("WITHHELD_NOT_RUN", "SCHEMA_REJECTED", f"{name}: input fails declared schema")

    return emit(
        "STRUCTURAL_ONLY_PASS",
        "TYPED_INPUT_SHAPE_MATCH",
        "Matches declared typed shape only. Confirm source completion, provenance, freshness, canonical representation and authorization separately before any Kernel run.",
    )


if __name__ == "__main__":
    sys.exit(main())
