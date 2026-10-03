#!/usr/bin/env python3
import base64
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from issuer_auth import ALGORITHM, PROFILE, TRUST_PROFILE, signing_message
from test_verify_portable_evidence import _write_valid_bundle
from verify_portable_evidence import verify


RFC8032_SEED = bytes.fromhex(
    "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60"
)
RFC8032_PUBLIC = bytes.fromhex(
    "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
)
RFC8032_EMPTY_SIGNATURE = bytes.fromhex(
    "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
    "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
)
RFC8032_WRONG_PUBLIC = bytes.fromhex(
    "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c"
)
KEY_ID = "rfc8032-test-vector-1"


def _crypto():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
    return Ed25519PrivateKey, Ed25519PublicKey


def _new_bundle(root: Path) -> Path:
    bundle = root / "bundle"
    bundle.mkdir()
    _write_valid_bundle(bundle)
    return bundle


def _write_trust_store(
    root: Path,
    public_key: bytes = RFC8032_PUBLIC,
    key_id: str = KEY_ID,
) -> Path:
    path = root / "trusted-issuers.json"
    path.write_text(json.dumps({
        "profile": TRUST_PROFILE,
        "keys": [{
            "key_id": key_id,
            "algorithm": ALGORITHM,
            "public_key_b64": base64.b64encode(public_key).decode("ascii"),
        }],
    }, indent=2) + "\n", encoding="utf-8")
    return path


def _sign_bundle(bundle: Path, key_id: str = KEY_ID) -> dict:
    Ed25519PrivateKey, _ = _crypto()
    receipt_sha = hashlib.sha256((bundle / "receipt.json").read_bytes()).hexdigest()
    private_key = Ed25519PrivateKey.from_private_bytes(RFC8032_SEED)
    signature = private_key.sign(signing_message(key_id, receipt_sha))
    envelope = {
        "profile": PROFILE,
        "algorithm": ALGORITHM,
        "key_id": key_id,
        "receipt_sha256": receipt_sha,
        "signature_b64": base64.b64encode(signature).decode("ascii"),
    }
    (bundle / "receipt.sig.json").write_text(
        json.dumps(envelope, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return envelope


class IssuerAuthenticityTests(unittest.TestCase):
    def test_rfc8032_official_vector_1(self):
        _, Ed25519PublicKey = _crypto()
        Ed25519PublicKey.from_public_bytes(RFC8032_PUBLIC).verify(
            RFC8032_EMPTY_SIGNATURE,
            b"",
        )

    def test_correct_key_and_receipt_commitment_is_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            _sign_bundle(bundle)
            trust = _write_trust_store(root)

            result = verify(bundle, trusted_issuer_keys_path=trust)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "verified")
            self.assertTrue(result["issuer_signature"]["key_trusted"])
            self.assertTrue(result["issuer_signature"]["signature_valid"])

    def test_wrong_public_key_fails_authenticity_not_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            _sign_bundle(bundle)
            trust = _write_trust_store(root, RFC8032_WRONG_PUBLIC)

            result = verify(bundle, trusted_issuer_keys_path=trust)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "failed")
            self.assertEqual(result["issuer_signature"]["reason"], "signature_invalid")

    def test_one_byte_receipt_mutation_breaks_signature_commitment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            _sign_bundle(bundle)
            trust = _write_trust_store(root)
            receipt = bundle / "receipt.json"
            receipt.write_bytes(receipt.read_bytes() + b" ")

            result = verify(bundle, trusted_issuer_keys_path=trust)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "failed")
            self.assertEqual(result["issuer_signature"]["reason"], "receipt_commitment_mismatch")

    def test_substituted_receipt_digest_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            envelope = _sign_bundle(bundle)
            envelope["receipt_sha256"] = "f" * 64
            (bundle / "receipt.sig.json").write_text(
                json.dumps(envelope, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            trust = _write_trust_store(root)

            result = verify(bundle, trusted_issuer_keys_path=trust)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "failed")
            self.assertEqual(result["issuer_signature"]["reason"], "receipt_commitment_mismatch")

    def test_malformed_signature_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            envelope = _sign_bundle(bundle)
            envelope["signature_b64"] = "***not-base64***"
            (bundle / "receipt.sig.json").write_text(
                json.dumps(envelope, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            trust = _write_trust_store(root)

            result = verify(bundle, trusted_issuer_keys_path=trust)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "failed")
            self.assertIn("signature_envelope_invalid", result["issuer_signature"]["reason"])

    def test_absent_signature_is_not_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            trust = _write_trust_store(root)

            result = verify(bundle, trusted_issuer_keys_path=trust)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "not_verified")
            self.assertEqual(result["issuer_signature"]["reason"], "signature_not_present")

    def test_signature_without_external_trust_anchor_is_not_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            _sign_bundle(bundle)

            result = verify(bundle)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "not_verified")
            self.assertEqual(result["issuer_signature"]["reason"], "no_trust_anchor_supplied")

    def test_key_id_not_in_trust_store_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle = _new_bundle(root)
            _sign_bundle(bundle)
            trust = _write_trust_store(root, RFC8032_PUBLIC, "different-key-id")

            result = verify(bundle, trusted_issuer_keys_path=trust)

            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["verification"]["integrity"], "verified")
            self.assertEqual(result["verification"]["issuer_authenticity"], "failed")
            self.assertEqual(result["issuer_signature"]["reason"], "key_id_not_in_trust_store")


if __name__ == "__main__":
    unittest.main()
