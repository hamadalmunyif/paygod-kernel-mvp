from __future__ import annotations

import base64
import binascii
import json
from pathlib import Path
import re

PROFILE = "paygod-ed25519-receipt-v1"
TRUST_PROFILE = "paygod-ed25519-trust-v1"
ALGORITHM = "Ed25519"
DOMAIN = b"PAYGOD-RECEIPT-v1\x00"
_KEY_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
_HEX64 = re.compile(r"^[a-f0-9]{64}$")


def signing_message(key_id: str, receipt_sha256: str) -> bytes:
    if not isinstance(key_id, str) or not _KEY_ID_RE.fullmatch(key_id):
        raise ValueError("invalid issuer key_id")
    if not isinstance(receipt_sha256, str) or not _HEX64.fullmatch(receipt_sha256):
        raise ValueError("receipt_sha256 must be 64 lowercase hex characters")
    return DOMAIN + key_id.encode("ascii") + b"\x00" + bytes.fromhex(receipt_sha256)


def _decode_b64(value: str, expected_length: int, label: str) -> bytes:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be base64 text")
    try:
        raw = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"{label} is not valid base64") from exc
    if len(raw) != expected_length:
        raise ValueError(f"{label} must decode to {expected_length} bytes")
    return raw


def load_trust_store(path: Path | None) -> dict[str, bytes]:
    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("profile") != TRUST_PROFILE:
        raise ValueError(f"trust store profile must be {TRUST_PROFILE}")
    keys = raw.get("keys")
    if not isinstance(keys, list):
        raise ValueError("trust store keys must be an array")

    result: dict[str, bytes] = {}
    for index, item in enumerate(keys):
        if not isinstance(item, dict):
            raise ValueError(f"trust store key entry {index} must be an object")
        if set(item) != {"key_id", "algorithm", "public_key_b64"}:
            raise ValueError(f"trust store key entry {index} has unsupported fields")
        key_id = item.get("key_id")
        if not isinstance(key_id, str) or not _KEY_ID_RE.fullmatch(key_id):
            raise ValueError(f"trust store key entry {index} has invalid key_id")
        if item.get("algorithm") != ALGORITHM:
            raise ValueError(f"trust store key entry {index} algorithm must be {ALGORITHM}")
        if key_id in result:
            raise ValueError(f"duplicate trust-store key_id: {key_id}")
        result[key_id] = _decode_b64(item.get("public_key_b64"), 32, "public_key_b64")
    return result


def verify_detached_signature(
    signature_path: Path,
    receipt_sha256: str,
    trusted_keys: dict[str, bytes],
) -> tuple[str, dict]:
    details = {
        "present": signature_path.is_file(),
        "profile": None,
        "algorithm": None,
        "key_id": None,
        "receipt_sha256_matches": False,
        "key_trusted": False,
        "signature_valid": False,
        "reason": None,
    }
    if not signature_path.is_file():
        details["reason"] = "signature_not_present"
        return "not_verified", details

    try:
        envelope = json.loads(signature_path.read_text(encoding="utf-8"))
        if not isinstance(envelope, dict):
            raise ValueError("signature envelope must be an object")
        expected_fields = {"profile", "algorithm", "key_id", "receipt_sha256", "signature_b64"}
        if set(envelope) != expected_fields:
            raise ValueError("signature envelope fields do not match the profile")

        details["profile"] = envelope.get("profile")
        details["algorithm"] = envelope.get("algorithm")
        details["key_id"] = envelope.get("key_id")

        if envelope.get("profile") != PROFILE:
            raise ValueError(f"signature profile must be {PROFILE}")
        if envelope.get("algorithm") != ALGORITHM:
            raise ValueError(f"signature algorithm must be {ALGORITHM}")

        key_id = envelope.get("key_id")
        if not isinstance(key_id, str) or not _KEY_ID_RE.fullmatch(key_id):
            raise ValueError("invalid signature key_id")

        committed_receipt = envelope.get("receipt_sha256")
        if not isinstance(committed_receipt, str) or not _HEX64.fullmatch(committed_receipt):
            raise ValueError("signature receipt_sha256 must be 64 lowercase hex characters")
        details["receipt_sha256_matches"] = committed_receipt == receipt_sha256
        if not details["receipt_sha256_matches"]:
            details["reason"] = "receipt_commitment_mismatch"
            return "failed", details

        signature = _decode_b64(envelope.get("signature_b64"), 64, "signature_b64")

        if not trusted_keys:
            details["reason"] = "no_trust_anchor_supplied"
            return "not_verified", details
        if key_id not in trusted_keys:
            details["reason"] = "key_id_not_in_trust_store"
            return "failed", details

        details["key_trusted"] = True
        try:
            from cryptography.exceptions import InvalidSignature
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        except ImportError:
            details["reason"] = "cryptography_backend_unavailable"
            return "not_verified", details

        public_key = Ed25519PublicKey.from_public_bytes(trusted_keys[key_id])
        try:
            public_key.verify(signature, signing_message(key_id, receipt_sha256))
        except InvalidSignature:
            details["reason"] = "signature_invalid"
            return "failed", details

        details["signature_valid"] = True
        details["reason"] = "verified"
        return "verified", details
    except Exception as exc:
        details["reason"] = f"signature_envelope_invalid: {exc}"
        return "failed", details
