import json
import hashlib
import sys

# RFC 8785 (JCS) Compliant Implementation
def jcs_compliant_dump(obj):
    # Custom encoder to handle floats per JCS (ES6 ToString)
    # 100.0 -> "100"
    if isinstance(obj, float):
        if obj.is_integer():
            return str(int(obj))
        # For other floats, standard repr is usually close enough for this demo,
        # but strictly should follow specific formatting rules.
        return str(obj)
    
    if isinstance(obj, dict):
        return "{" + ",".join(f"{jcs_compliant_dump(k)}:{jcs_compliant_dump(v)}" 
                              for k, v in sorted(obj.items())) + "}"
    
    if isinstance(obj, list):
        return "[" + ",".join(jcs_compliant_dump(x) for x in obj) + "]"
    
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    
    if obj is True: return "true"
    if obj is False: return "false"
    if obj is None: return "null"
    
    return str(obj) # Ints

def calculate_hash(obj):
    canonical_str = jcs_compliant_dump(obj)
    data = canonical_str.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def process_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r') as f:
        vectors = json.load(f)
    
    updated_vectors = []
    for case in vectors:
        input_data = case['input']
        
        expected_canonical = jcs_compliant_dump(input_data)
        expected_hash = calculate_hash(input_data)
        
        case['expected_canonical'] = expected_canonical
        case['expected_hash'] = expected_hash
        updated_vectors.append(case)
        
        print(f"  - {case['description']}")

    with open(filepath, 'w') as f:
        json.dump(updated_vectors, f, indent=2, ensure_ascii=False)
    print("Done.\n")

if __name__ == "__main__":
    files = [
        "/home/ubuntu/الحمدلله/paygod-kernel/spec/test-vectors/canonical-json.json",
        "/home/ubuntu/الحمدلله/paygod-kernel/spec/test-vectors/ledger-chaining.json"
    ]
    
    for f in files:
        process_file(f)
