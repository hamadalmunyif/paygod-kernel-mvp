import json
import hashlib
import sys
import os
import jcs

def canonicalize(obj):
    # Use actual JCS library for RFC 8785 compliance
    return jcs.canonicalize(obj).decode('utf-8')

def calculate_hash(obj):
    canonical_bytes = jcs.canonicalize(obj)
    return hashlib.sha256(canonical_bytes).hexdigest()

def verify_file(filepath):
    print(f"🔍 Verifying {os.path.basename(filepath)}...")
    try:
        with open(filepath, 'r') as f:
            vectors = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False
    
    all_passed = True
    for i, case in enumerate(vectors):
        desc = case.get('description', f"Case #{i}")
        input_data = case['input']
        expected_canonical = case['expected_canonical']
        expected_hash = case['expected_hash']
        
        # 1. Verify Canonical Form
        actual_canonical = canonicalize(input_data)
        if actual_canonical != expected_canonical:
            print(f"❌ Failed: {desc}")
            print(f"   Expected Canonical: {expected_canonical}")
            print(f"   Actual Canonical:   {actual_canonical}")
            all_passed = False
            continue

        # 2. Verify Hash
        actual_hash = calculate_hash(input_data)
        if actual_hash != expected_hash:
            print(f"❌ Failed: {desc}")
            print(f"   Expected Hash: {expected_hash}")
            print(f"   Actual Hash:   {actual_hash}")
            all_passed = False
            continue
            
        print(f"✅ Passed: {desc}")
    
    return all_passed

if __name__ == "__main__":
    # Use relative path from the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    base_dir = os.path.join(project_root, "spec", "test-vectors")
    
    files = [
        os.path.join(base_dir, "canonical-json.json"),
        os.path.join(base_dir, "ledger-chaining.json")
    ]
    
    success = True
    for f in files:
        if not os.path.exists(f):
            print(f"⚠️ Warning: Test vector file not found: {f}")
            continue
            
        if not verify_file(f):
            success = False
            print("")
    
    if success:
        print("\n✨ All Test Vectors Verified Successfully!")
        sys.exit(0)
    else:
        print("\n💥 Verification Failed!")
        sys.exit(1)
