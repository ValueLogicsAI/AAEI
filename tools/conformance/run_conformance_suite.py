#!/usr/bin/env python3
"""
AAEI v1.2 — MOF Conformance Test Suite
=====================================
Runs all 18 conformance tests against the AAEI v1.2 schema.
Tests are categorized per the OMG submission paper (Section 4):

  CT-01–CT-04: Structural conformance
  CT-05–CT-08: Semantic conformance
  CT-09–CT-12: Generation conformance
  CT-13–CT-16: Interchange conformance
  CT-17–CT-18: Evidence integrity

Usage:
  python3 run_conformance_suite.py

Output:
  Console report + conformance_report.json

Repository: github.com/ValueLogicsAI/AAEI
License:    Apache 2.0
Author:     ValueLogics.ai LLC
"""

import json, sys, os, datetime
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, Draft202012Validator
except ImportError:
    print("Installing jsonschema...")
    os.system("pip install jsonschema --break-system-packages -q")
    import jsonschema
    from jsonschema import validate, ValidationError, Draft202012Validator

# ── Paths ─────────────────────────────────────────────────────────────────
SUITE_DIR  = Path(__file__).parent
SCHEMA_DIR = SUITE_DIR.parent.parent / "schemas"
SCHEMA_FILE = SCHEMA_DIR / "aaei_schema_v1_2.json"

if not SCHEMA_FILE.exists():
    # Try relative path for running from repo root
    SCHEMA_FILE = Path("schemas/aaei_schema_v1_2.json")

schema = json.loads(SCHEMA_FILE.read_text())

def ok(record):
    """Returns True if record validates against AAEI schema."""
    try:
        validate(instance=record, schema=schema,
                 cls=Draft202012Validator)
        return True
    except ValidationError:
        return False

def must_fail(record):
    """Returns True if record correctly fails validation."""
    try:
        validate(instance=record, schema=schema,
                 cls=Draft202012Validator)
        return False  # Should have failed
    except ValidationError:
        return True

# ── Test definitions ──────────────────────────────────────────────────────
def run_tests():
    results = []

    def test(ct_id, category, name, fn):
        try:
            passed = fn()
            results.append({
                "id": ct_id, "category": category, "name": name,
                "status": "PASS" if passed else "FAIL",
                "error": None
            })
        except Exception as e:
            results.append({
                "id": ct_id, "category": category, "name": name,
                "status": "FAIL", "error": str(e)
            })

    # ── CT-01: Required fields presence ───────────────────────────────────
    test("CT-01", "structural", "Required fields presence", lambda:
        ok({"role": "support-agent", "problem": "4hr ticket delay"}) and
        must_fail({"problem": "missing role field"}) and
        must_fail({"role": "missing problem"})
    )

    # ── CT-02: Nullable optional attributes ───────────────────────────────
    test("CT-02", "structural", "Nullable optional attributes", lambda:
        ok({
            "role": "cfo-agent", "problem": "manual reconciliation",
            "bau_measure": None, "ps_measure": None, "delta": None,
            "motivation_ref": None, "desired_result": None,
            "evidence_chain_id": None, "hash": None,
            "lifecycle_mode": None, "proof_package_ref": None, "drift_status": None
        })
    )

    # ── CT-03: No additional properties ───────────────────────────────────
    test("CT-03", "structural", "No additional properties", lambda:
        ok({"role": "ciso-agent", "problem": "ungoverned AI"}) and
        must_fail({"role": "ciso-agent", "problem": "ungoverned AI", "undeclared_field": "not allowed"})
    )

    # ── CT-04: Measure object structure ───────────────────────────────────
    test("CT-04", "structural", "Measure object structure", lambda:
        ok({
            "role": "cto-agent", "problem": "refactoring drag",
            "bau_measure": {"value": 240, "unit": "minutes"},
            "ps_measure": {"value": 30, "unit": "minutes"},
            "delta": {"value": 210, "unit": "minutes", "direction": "reduction"}
        }) and
        must_fail({
            "role": "cto-agent", "problem": "refactoring drag",
            "bau_measure": {"value": "not-a-number", "unit": "minutes"}
        })
    )

    # ── CT-05: lifecycle_mode enumeration ─────────────────────────────────
    test("CT-05", "semantic", "lifecycle_mode enumeration constraint", lambda:
        all(ok({"role": "r", "problem": "p", "lifecycle_mode": m})
            for m in ["active","completed","suspended","archived"]) and
        ok({"role": "r", "problem": "p", "lifecycle_mode": None}) and
        must_fail({"role": "r", "problem": "p", "lifecycle_mode": "running"})
    )

    # ── CT-06: drift_status enumeration ───────────────────────────────────
    test("CT-06", "semantic", "drift_status enumeration constraint", lambda:
        all(ok({"role": "r", "problem": "p", "drift_status": d})
            for d in ["on_track","at_risk","drifting"]) and
        ok({"role": "r", "problem": "p", "drift_status": None}) and
        must_fail({"role": "r", "problem": "p", "drift_status": "drifted"})
    )

    # ── CT-07: hash format constraint ─────────────────────────────────────
    test("CT-07", "semantic", "hash format constraint", lambda:
        ok({"role": "r", "problem": "p", "evidence_chain_id": "ec_01", "hash": "sha256:9a31b7f2c4"}) and
        must_fail({"role": "r", "problem": "p", "evidence_chain_id": "ec_01", "hash": "md5:notvalid"}) and
        must_fail({"role": "r", "problem": "p", "evidence_chain_id": "ec_01", "hash": "sha256:abc"})  # too short
    )

    # ── CT-08: BMM bridge field independence ──────────────────────────────
    test("CT-08", "semantic", "BMM bridge field independence", lambda:
        ok({
            "role": "cfo-agent", "problem": "AI spend waste",
            "motivation_ref": "bmm://goals/reduce-ai-spend",
            "desired_result": "10% reduction in unproven AI investment"
        }) and
        ok({"role": "cfo-agent", "problem": "AI spend waste", "motivation_ref": None, "desired_result": None})
    )

    # ── CT-09: Minimal M1 instance ────────────────────────────────────────
    test("CT-09", "generation", "Minimal M1 instance — role + problem only", lambda:
        ok({"role": "ceo", "problem": "cost of delay"})
    )

    # ── CT-10: Full M1 instance — all 12 fields ───────────────────────────
    test("CT-10", "generation", "Full M1 instance — all 12 fields", lambda:
        ok({
            "role": "support-triage-agent",
            "problem": "manual ticket routing causes 4hr median delay",
            "bau_measure": {"value": 240, "unit": "minutes"},
            "ps_measure": {"value": 30, "unit": "minutes"},
            "motivation_ref": "bmm://goals/reduce-support-cycle-time",
            "desired_result": "30-minute median routing time",
            "delta": {"value": 210, "unit": "minutes", "direction": "reduction"},
            "evidence_chain_id": "ec_8f21a4b3",
            "hash": "sha256:9a31b7f2c4e8d6a1",
            "lifecycle_mode": "active",
            "drift_status": "on_track",
            "proof_package_ref": "https://evidence.valuelogics.ai/proof/ec_8f21a4b3"
        })
    )

    # ── CT-11: AI agent M1 instance ───────────────────────────────────────
    test("CT-11", "generation", "AI agent M1 instance", lambda:
        ok({
            "role": "sales-qualification-agent",
            "problem": "unqualified leads waste 40% of rep capacity",
            "bau_measure": {"value": 40, "unit": "percent"},
            "ps_measure": {"value": 10, "unit": "percent"},
            "delta": {"value": 30, "unit": "percent", "direction": "reduction"},
            "lifecycle_mode": "active",
            "drift_status": "on_track"
        })
    )

    # ── CT-12: ESG-extended M1 instance ───────────────────────────────────
    test("CT-12", "generation", "ESG-extended M1 instance", lambda:
        ok({
            "role": "esg-compliance-agent",
            "problem": "enterprise procurement eliminating vendors without ESG proof",
            "bau_measure": {"value": 0, "unit": "ESG proof packages"},
            "ps_measure": {"value": 1, "unit": "audit-ready ESG proof package"},
            "delta": {"value": 1, "unit": "proof packages", "direction": "increase"},
            "evidence_chain_id": "ec_esg_2026_q3",
            "lifecycle_mode": "active",
            "proof_package_ref": "https://evidence.valuelogics.ai/esg/ec_esg_2026_q3"
        })
    )

    # ── CT-13: JSON round-trip ────────────────────────────────────────────
    test("CT-13", "interchange", "JSON serialization round-trip", lambda: (
        lambda r: ok(json.loads(json.dumps(r)))
    )({
        "role": "ciso-agent", "problem": "ungoverned AI agents",
        "bau_measure": {"value": 1500000, "unit": "USD"},
        "lifecycle_mode": "active", "drift_status": "on_track"
    }))

    # ── CT-14: Null field omission compatibility ───────────────────────────
    test("CT-14", "interchange", "Null field omission compatibility", lambda:
        ok({"role": "cfo-agent", "problem": "reporting waste"}) and
        ok({
            "role": "cfo-agent", "problem": "reporting waste",
            "bau_measure": None, "ps_measure": None, "delta": None,
            "motivation_ref": None, "desired_result": None,
            "evidence_chain_id": None, "hash": None,
            "lifecycle_mode": None, "proof_package_ref": None, "drift_status": None
        })
    )

    # ── CT-15: Unicode string encoding ────────────────────────────────────
    test("CT-15", "interchange", "String field Unicode encoding", lambda:
        ok({
            "role": "agent-de-qualification-des-ventes",
            "problem": "40% des prospects ne correspondent pas aux critères"
        }) and
        ok({"role": "エージェント", "problem": "AI価値の説明責任"})
    )

    # ── CT-16: Numeric precision ──────────────────────────────────────────
    test("CT-16", "interchange", "Numeric precision in measure objects", lambda:
        ok({
            "role": "cmo-agent", "problem": "conversion leakage",
            "bau_measure": {"value": 2.37, "unit": "percent"},
            "ps_measure": {"value": 4.15, "unit": "percent"},
            "delta": {"value": 1.78, "unit": "percent", "direction": "increase"}
        })
    )

    # ── CT-17: hash requires evidence_chain_id ────────────────────────────
    test("CT-17", "evidence_integrity", "hash requires evidence_chain_id", lambda:
        ok({
            "role": "cio-agent", "problem": "cloud waste",
            "evidence_chain_id": "ec_ldr_cloud_2026",
            "hash": "sha256:7c4a2b1e9f"
        }) and
        must_fail({
            "role": "cio-agent", "problem": "cloud waste",
            "hash": "sha256:7c4a2b1e9f"
            # evidence_chain_id missing — hash without chain is not verifiable
        })
    )

    # ── CT-18: drift_status closed enumeration ────────────────────────────
    test("CT-18", "evidence_integrity", "drift_status closed enumeration", lambda:
        ok({"role": "ceo", "problem": "AI execution delay", "drift_status": "at_risk"}) and
        must_fail({"role": "ceo", "problem": "AI execution delay", "drift_status": "slightly_off_track"}) and
        must_fail({"role": "ceo", "problem": "AI execution delay", "drift_status": "ok"})
    )

    return results

# ── Run and report ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 62)
    print("  AAEI v1.2 — MOF Conformance Test Suite")
    print("  github.com/ValueLogicsAI/AAEI · Apache 2.0")
    print("=" * 62)
    print()

    results = run_tests()
    passed  = [r for r in results if r["status"] == "PASS"]
    failed  = [r for r in results if r["status"] == "FAIL"]

    categories = ["structural","semantic","generation","interchange","evidence_integrity"]
    for cat in categories:
        cat_results = [r for r in results if r["category"] == cat]
        cat_pass    = sum(1 for r in cat_results if r["status"] == "PASS")
        print(f"  {cat.upper().replace('_',' '):<25}  {cat_pass}/{len(cat_results)}")
        for r in cat_results:
            icon = "✓" if r["status"] == "PASS" else "✗"
            print(f"    {icon} {r['id']}  {r['name']}")
            if r["error"]:
                print(f"         ERROR: {r['error']}")
        print()

    print("=" * 62)
    total = len(results)
    n_pass = len(passed)
    print(f"  RESULT: {n_pass}/{total} tests passing")
    if n_pass == total:
        print(f"  STATUS: ✓ AAEI v1.2 MOF CONFORMANCE VERIFIED")
    else:
        print(f"  STATUS: ✗ {len(failed)} test(s) FAILED — see above")
    print("=" * 62)

    # Write machine-readable report
    report = {
        "standard": "AAEI v1.2 — AI Accountability Evidence Interchange",
        "mof_version": "MOF 2.5.1 (formal/16-11-01)",
        "run_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "schema": "schemas/aaei_schema_v1_2.json",
        "repository": "github.com/ValueLogicsAI/AAEI",
        "license": "Apache 2.0",
        "summary": {
            "total": total,
            "passed": n_pass,
            "failed": len(failed),
            "conformant": n_pass == total
        },
        "results": results
    }
    report_path = Path(__file__).parent / "conformance_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n  Report written: tools/conformance/conformance_report.json")

    sys.exit(0 if n_pass == total else 1)
