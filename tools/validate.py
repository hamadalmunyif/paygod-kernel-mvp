import sys
import json
import argparse
import re
from jsonschema import validate, ValidationError, FormatChecker

# Custom format checkers for strict compliance
checker = FormatChecker()

@checker.checks("uuid")
def is_uuid(instance):
    if not isinstance(instance, str): return True
    return bool(re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', instance, re.I))

def main():
    parser = argparse.ArgumentParser(description='Paygod Strict Schema Validator')
    parser.add_argument('--schema', '-s', required=True, help='Path to JSON Schema file')
    parser.add_argument('--instance', '-i', required=True, help='Path to JSON data file')
    args = parser.parse_args()

    try:
        with open(args.schema, 'r') as sf:
            schema = json.load(sf)
        
        with open(args.instance, 'r') as ifile:
            instance = json.load(ifile)

        # Enforce strict validation
        validate(instance=instance, schema=schema, format_checker=checker)
        
        print(json.dumps({"valid": True, "file": args.instance}))
        sys.exit(0)

    except ValidationError as e:
        print(json.dumps({
            "valid": False,
            "error": e.message,
            "path": list(e.path),
            "schema_path": list(e.schema_path)
        }, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"valid": False, "error": str(e)}))
        sys.exit(2)

if __name__ == "__main__":
    main()
