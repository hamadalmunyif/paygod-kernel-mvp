import hashlib
import json
import uuid
from datetime import datetime

def canonical_json(obj):
    """Canonical JSON representation for consistent hashing."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))

def sha256(data):
    return "sha256:" + hashlib.sha256(data.encode('utf-8')).hexdigest()

class Ledger:
    def __init__(self):
        self.chain = []
        # Genesis block
        self.chain.append({
            "entry_id": str(uuid.uuid4()),
            "entry_index": 0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "prev_hash": "sha256:" + "0"*64,
            "record_hash": "sha256:" + "0"*64,
            "record_type": "genesis",
            "record_payload": {}
        })

    def append(self, record_type, payload):
        prev_entry = self.chain[-1]
        prev_hash = sha256(canonical_json(prev_entry))
        
        record_hash = sha256(canonical_json(payload))
        
        entry = {
            "entry_id": str(uuid.uuid4()),
            "entry_index": len(self.chain),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "prev_hash": prev_hash,
            "record_hash": record_hash,
            "record_type": record_type,
            "record_payload": payload
        }
        
        self.chain.append(entry)
        return entry

    def verify(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            
            calculated_prev_hash = sha256(canonical_json(prev))
            if current["prev_hash"] != calculated_prev_hash:
                return False, i
        return True, -1

if __name__ == "__main__":
    ledger = Ledger()
    print("Genesis Block Created.")
    
    # Simulate adding a record
    obs = {
        "record_id": str(uuid.uuid4()),
        "source": "simulation",
        "amount": 1000
    }
    entry = ledger.append("observation", obs)
    print(f"Added Entry #{entry['entry_index']} - Hash: {entry['record_hash']}")
    
    # Verify chain
    valid, index = ledger.verify()
    if valid:
        print("✅ Ledger Integrity Verified.")
    else:
        print(f"❌ Ledger Corrupted at Index {index}")
