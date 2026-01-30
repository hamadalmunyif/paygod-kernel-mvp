import json, uuid, hashlib
from datetime import datetime

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))

def sha256(data):
    return 'sha256:' + hashlib.sha256(data.encode('utf-8')).hexdigest()

genesis={
    'entry_id': str(uuid.uuid4()),
    'entry_index': 0,
    'timestamp': datetime.utcnow().isoformat()+'Z',
    'prev_hash': 'sha256:' + '0'*64,
    'record_hash': 'sha256:' + '0'*64,
    'record_type': 'observation', # Changed from 'genesis' to 'observation' to match enum
    'record_payload': {}
}

payload={'record_id': str(uuid.uuid4()), 'source': 'simulation', 'amount': 1000}

entry={
    'entry_id': str(uuid.uuid4()),
    'entry_index': 1,
    'timestamp': datetime.utcnow().isoformat()+'Z',
    'prev_hash': sha256(canonical_json(genesis)),
    'record_hash': sha256(canonical_json(payload)),
    'record_type': 'observation',
    'record_payload': payload
}

with open('tmp_entry.json','w') as f:
    json.dump(entry,f,indent=2)

print("Wrote tmp_entry.json")
