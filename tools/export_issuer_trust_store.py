#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import sys

from issuer_auth import ALGORITHM, TRUST_PROFILE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export a PEM Ed25519 public key as a Paygod external trust store."
    )
    parser.add_argument("--key-id", required=True)
    parser.add_argument("--public-key", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError as exc:
        raise SystemExit("cryptography package is required") from exc

    public_key = serialization.load_pem_public_key(args.public_key.read_bytes())
    if not isinstance(public_key, Ed25519PublicKey):
        raise SystemExit("public key must be Ed25519")

    raw = public_key.public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )
    trust = {
        "profile": TRUST_PROFILE,
        "keys": [{
            "key_id": args.key_id,
            "algorithm": ALGORITHM,
            "public_key_b64": base64.b64encode(raw).decode("ascii"),
        }],
    }
    args.output.write_text(
        json.dumps(trust, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(args.output),
        "key_id": args.key_id,
        "profile": TRUST_PROFILE,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
