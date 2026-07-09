#!/usr/bin/env python3
"""
AAEI v1.2 — Record Validator
============================
Validates a JSON file against the AAEI v1.2 schema.

Usage:
  python3 tools/validate_aaei.py --record path/to/record.json

Repository: github.com/ValueLogicsAI/AAEI
License:    Apache 2.0
"""

import sys, json, argparse
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, Draft202012Validator
except ImportError:
    import os; os.system("pip install jsonschema --break-system-packages -q")
    from jsonschema import validate, ValidationError, Draft202012Validator

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "aaei_schema_v1_2.json"

def main():
    parser = argparse.ArgumentParser(description="Validate an AAEI v1.2 evidence record")
    parser.add_argument("--record", required=True, help="Path to JSON record file")
    parser.add_argument("--schema", default=str(SCHEMA_PATH), help="Path to schema file")
    args = parser.parse_args()

    schema = json.loads(Path(args.schema).read_text())
    record = json.loads(Path(args.record).read_text())

    # Strip _comment fields before validation
    record = {k: v for k, v in record.items() if not k.startswith("_")}

    try:
        validate(instance=record, schema=schema, cls=Draft202012Validator)
        print(f"✓ PASSED  {args.record}")
        print(f"  role: {record.get('role')}")
        print(f"  problem: {record.get('problem')[:60]}...")
        print(f"  lifecycle_mode: {record.get('lifecycle_mode')}")
        print(f"  drift_status: {record.get('drift_status')}")
        return 0
    except ValidationError as e:
        print(f"✗ FAILED  {args.record}")
        print(f"  Error: {e.message}")
        print(f"  Path:  {' > '.join(str(p) for p in e.absolute_path)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
