# Paygod Specifications & Test Vectors

This directory contains the **Golden Fixtures** that define the exact behavior of the Paygod Kernel.

## 🏆 The Compliance Standard
Any implementation of Paygod (whether in Rust, Go, .NET, or Python) **MUST** pass these test vectors bit-for-bit.

> **Why?** Paygod relies on cryptographic ledger chaining. A single byte difference in JSON serialization (e.g., a space or a float representation) will change the hash, breaking the chain and failing audit verification.

## 📂 Contents

*   **`test-vectors/canonical-json.json`**: Defines strict serialization rules (RFC 8785).
    *   *Coverage:* Sorting, Whitespace, Unicode, Emojis, Floats, Escaping.
*   **`test-vectors/ledger-chaining.json`**: Defines how ledger entries are linked via SHA-256 hashes.

## 🧪 How to Verify
We provide a reference verification tool in `tools/verify_spec.py`.

### Run Verification (CI)
```bash
python3 tools/verify_spec.py
```

### Manual Check (Python)
```python
import json
import hashlib

# Your implementation MUST match this logic exactly:
def calculate_hash(obj):
    # 1. Canonicalize (RFC 8785)
    canonical = json.dumps(obj, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
    # 2. Encode UTF-8
    data = canonical.encode('utf-8')
    # 3. SHA-256 Hash
    return hashlib.sha256(data).hexdigest()
```
