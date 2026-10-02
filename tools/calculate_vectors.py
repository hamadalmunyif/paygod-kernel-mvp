import hashlib
import json
from pathlib import Path

from verify_portable_evidence import canonical_json


def calculate_hash(obj):
    canonical = canonical_json(obj)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def process_file(filepath: Path):
    print(f"Processing {filepath}...")
    vectors = json.loads(filepath.read_text(encoding="utf-8"))

    for case in vectors:
        if "expected_error" in case:
            continue
        input_data = case["input"]
        case["expected_canonical"] = canonical_json(input_data)
        case["expected_hash"] = calculate_hash(input_data)
        print(f"  - {case['description']}")

    filepath.write_text(
        json.dumps(vectors, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for name in ("canonical-json.json", "ledger-chaining.json"):
        process_file(root / "spec" / "test-vectors" / name)
