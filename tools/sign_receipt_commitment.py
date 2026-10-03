#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys

from issuer_auth import ALGORITHM, PROFILE, signing_message


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a detached Ed25519 signature over a Paygod receipt commitment."
    )
    parser.add_argument("bundle", type=Path, help="Evidence bundle directory containing receipt.json")
    parser.add_argument("--key-id", required=True, help="Stable trusted issuer key identifier")
    parser.add_argument("--private-key", required=True, type=Path, help="PEM Ed25519 private key outside the repository")
    parser.add_argument("--output", type=Path, help="Defaults to <bundle>/receipt.sig.json")
    args = parser.parse_args()

    receipt_path = args.bundle / "receipt.json"
    if not receipt_path.is_file():
        raise SystemExit("missing receipt.json")

    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError as exc:
        raise SystemExit("cryptography package is required for signing") from exc

    private_key = serialization.load_pem_private_key(args.private_key.read_bytes(), password=None)
    if not isinstance(private_key, Ed25519PrivateKey):
        raise SystemExit("private key must be Ed25519")

    receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    signature = private_key.sign(signing_message(args.key_id, receipt_sha))
    envelope = {
        "profile": PROFILE,
        "algorithm": ALGORITHM,
        "key_id": args.key_id,
        "receipt_sha256": receipt_sha,
        "signature_b64": base64.b64encode(signature).decode("ascii"),
    }

    output = args.output or (args.bundle / "receipt.sig.json")
    output.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "key_id": args.key_id,
        "receipt_sha256": receipt_sha,
        "profile": PROFILE,
        "algorithm": ALGORITHM,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
