#!/usr/bin/env python3
"""
AAEI v1.2 — Record Validator
============================
Validates JSON files against the AAEI v1.2 schema.

Setup:
  python3 -m pip install -r requirements.txt

Usage:
  python3 tools/validate_aaei.py --record path/to/record.json
  python3 tools/validate_aaei.py --record a.json b.json
  python3 tools/validate_aaei.py --examples

Exit code: 0 if every record validates, 1 otherwise,
2 if the jsonschema dependency is missing.

Repository: github.com/ValueLogicsAI/AAEI
License:    Apache 2.0
"""

import sys, json, argparse
from pathlib import Path

try:
    from jsonschema import validate, ValidationError, Draft202012Validator
except ImportError:
    sys.stderr.write(
        "ERROR: the 'jsonschema' package is required and is not installed.\n"
        "Install it with:\n"
        "  python3 -m pip install -r requirements.txt\n"
    )
    sys.exit(2)

REPO_ROOT    = Path(__file__).parent.parent
SCHEMA_PATH  = REPO_ROOT / "schemas" / "aaei_schema_v1_2.json"
EXAMPLES_DIR = REPO_ROOT / "examples"

def validate_record(path, schema):
    """Validates one record file. Prints the result. Returns True if it passed."""
    record = json.loads(Path(path).read_text(encoding="utf-8"))

    # Strip _comment fields before validation
    record = {k: v for k, v in record.items() if not k.startswith("_")}

    try:
        validate(instance=record, schema=schema, cls=Draft202012Validator)
        print(f"✓ PASSED  {path}")
        print(f"  role: {record.get('role')}")
        print(f"  problem: {record.get('problem')[:60]}...")
        print(f"  lifecycle_mode: {record.get('lifecycle_mode')}")
        print(f"  drift_status: {record.get('drift_status')}")
        return True
    except ValidationError as e:
        print(f"✗ FAILED  {path}")
        print(f"  Error: {e.message}")
        print(f"  Path:  {' > '.join(str(p) for p in e.absolute_path)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Validate AAEI v1.2 evidence records")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--record", nargs="+", help="Path to one or more JSON record files")
    target.add_argument("--examples", action="store_true",
                        help="Validate every record in examples/")
    parser.add_argument("--schema", default=str(SCHEMA_PATH), help="Path to schema file")
    args = parser.parse_args()

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))

    if args.examples:
        records = sorted(str(p) for p in EXAMPLES_DIR.glob("*.json"))
        if not records:
            print(f"✗ FAILED  no example records found in {EXAMPLES_DIR}")
            return 1
    else:
        records = args.record

    passed = [validate_record(path, schema) for path in records]
    if len(records) > 1:
        print(f"\n{sum(passed)}/{len(records)} records valid")
    return 0 if all(passed) else 1

if __name__ == "__main__":
    sys.exit(main())
