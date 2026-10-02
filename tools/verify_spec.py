import hashlib
import json
import os
import sys

from verify_portable_evidence import canonical_json


def calculate_hash(obj):
    canonical = canonical_json(obj)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_file(filepath):
    print(f"Verifying {os.path.basename(filepath)}...")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            vectors = json.load(f)
    except Exception as e:
        print(f"FAILED to load JSON: {e}")
        return False

    all_passed = True
    for i, case in enumerate(vectors):
        desc = case.get("description", f"Case #{i}")
        input_data = case["input"]
        expected_error = case.get("expected_error")

        if expected_error is not None:
            try:
                canonical_json(input_data)
            except Exception as exc:
                if expected_error.lower() in str(exc).lower():
                    print(f"PASS reject: {desc}")
                    continue
                print(f"FAIL reject: {desc}")
                print(f"   Expected error containing: {expected_error}")
                print(f"   Actual error: {exc}")
                all_passed = False
                continue
            print(f"FAIL reject: {desc}")
            print("   Input was accepted but MUST be rejected by paygod-c14n-v1")
            all_passed = False
            continue

        expected_canonical = case["expected_canonical"]
        expected_hash = case["expected_hash"]

        try:
            actual_canonical = canonical_json(input_data)
        except Exception as exc:
            print(f"FAIL: {desc}")
            print(f"   Unexpected canonicalization error: {exc}")
            all_passed = False
            continue

        if actual_canonical != expected_canonical:
            print(f"FAIL: {desc}")
            print(f"   Expected Canonical: {expected_canonical}")
            print(f"   Actual Canonical:   {actual_canonical}")
            all_passed = False
            continue

        actual_hash = calculate_hash(input_data)
        if actual_hash != expected_hash:
            print(f"FAIL: {desc}")
            print(f"   Expected Hash: {expected_hash}")
            print(f"   Actual Hash:   {actual_hash}")
            all_passed = False
            continue

        print(f"PASS: {desc}")

    return all_passed


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    base_dir = os.path.join(project_root, "spec", "test-vectors")

    files = [
        os.path.join(base_dir, "canonical-json.json"),
        os.path.join(base_dir, "ledger-chaining.json"),
    ]

    success = True
    for f in files:
        if not os.path.exists(f):
            print(f"Warning: test vector file not found: {f}")
            continue
        if not verify_file(f):
            success = False
            print("")

    if success:
        print("\nAll Paygod test vectors verified successfully.")
        sys.exit(0)

    print("\nVerification failed.")
    sys.exit(1)
