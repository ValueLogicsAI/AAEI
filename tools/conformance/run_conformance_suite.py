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

Each CT test runs its inline assertions AND its fixture file
(tools/conformance/ct-NN-*.json): the fixture must carry the same id,
category and name as the test, every pass_fixture* record must validate,
and a non-null fail_fixture must be rejected.

Supplementary checks (SC-01–SC-03) run after the 18 conformance tests and
are counted separately. They do not change the 18-test conformance count.

Setup:
  python3 -m pip install -r requirements.txt

Usage:
  python3 tools/conformance/run_conformance_suite.py
  python3 tools/conformance/run_conformance_suite.py --report PATH

Output:
  Console report. No file is written unless --report PATH is given.

Exit code: 0 if every conformance test and supplementary check passes,
1 otherwise, 2 if the jsonschema dependency is missing.

Repository: github.com/ValueLogicsAI/AAEI
License:    Apache 2.0
Author:     ValueLogics.ai LLC
"""

import argparse, json, re, sys, datetime
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, Draft202012Validator
except ImportError:
    sys.stderr.write(
        "ERROR: the 'jsonschema' package is required and is not installed.\n"
        "Install it with:\n"
        "  python3 -m pip install -r requirements.txt\n"
    )
    sys.exit(2)

# ── Paths ─────────────────────────────────────────────────────────────────
SUITE_DIR  = Path(__file__).parent
REPO_ROOT  = SUITE_DIR.parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"
SCHEMA_FILE = SCHEMA_DIR / "aaei_schema_v1_2.json"
EXAMPLES_DIR = REPO_ROOT / "examples"
XMI_EXAMPLE  = REPO_ROOT / "mof" / "aaei_xmi_example.xml"

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

# ── Fixture execution ─────────────────────────────────────────────────────
def load_fixture(test_id):
    """Returns (path, fixture) for the single fixture file of a test id."""
    matches = sorted(SUITE_DIR.glob(f"{test_id.lower()}-*.json"))
    if len(matches) != 1:
        raise AssertionError(
            f"expected exactly one fixture file for {test_id}, found {len(matches)}")
    return matches[0], json.loads(matches[0].read_text(encoding="utf-8"))

def fixture_problems(test_id, category, name):
    """Runs a test's fixture file. Returns a list of problems (empty = fixture passes)."""
    path, fx = load_fixture(test_id)
    problems = []
    for key, expected in (("id", test_id), ("category", category), ("name", name)):
        if fx.get(key) != expected:
            problems.append(f"{path.name}: {key} is {fx.get(key)!r}, test declares {expected!r}")
    pass_keys = [k for k in fx if k.startswith("pass_fixture")]
    if not pass_keys:
        problems.append(f"{path.name}: no pass_fixture")
    for key in pass_keys:
        if not ok(fx[key]):
            problems.append(f"{path.name}: {key} does not validate")
    if fx.get("fail_fixture") is not None and not must_fail(fx["fail_fixture"]):
        problems.append(f"{path.name}: fail_fixture validates but must be rejected")
    return problems

# ── Test definitions ──────────────────────────────────────────────────────
def run_tests():
    results = []

    def test(ct_id, category, name, fn):
        try:
            passed = fn()
            problems = fixture_problems(ct_id, category, name)
            results.append({
                "id": ct_id, "category": category, "name": name,
                "status": "PASS" if passed and not problems else "FAIL",
                "error": "; ".join(problems) if problems else None
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

# ── Supplementary checks ──────────────────────────────────────────────────
# Counted separately from the 18 conformance tests.
def local_name(tag):
    """XML local name without its namespace."""
    return tag.rsplit("}", 1)[-1]

def plain_attributes(element):
    """Attributes that are not in an XML namespace (drops xmi:id, xmi:type)."""
    return {k: v for k, v in element.attrib.items() if not k.startswith("{")}

def xmi_example_problems():
    """
    Checks mof/aaei_xmi_example.xml against the schema's closed world.
    Names, required attributes, enumerations and the hash pattern all come
    from the schema. Numeric typing is not checked: the repository defines
    no XMI-to-JSON value mapping and no XMI schema.
    """
    problems = []
    root = ET.parse(XMI_EXAMPLE).getroot()  # raises if not well-formed XML
    if local_name(root.tag) != "XMI":
        problems.append(f"root element is {local_name(root.tag)!r}, expected 'XMI'")
    instances = [e for e in root.iter() if local_name(e.tag) == "AccountabilityEvidence"]
    if not instances:
        problems.append("no AccountabilityEvidence instance")
    props = schema["properties"]
    for inst in instances:
        attrs = plain_attributes(inst)
        for name, value in attrs.items():
            if name not in props:
                problems.append(f"attribute {name!r} is not an AAEI field")
                continue
            enum = [x for x in props[name].get("enum", []) if x is not None]
            if enum and value not in enum:
                problems.append(f"{name}={value!r} is not one of {enum}")
            pattern = props[name].get("pattern")
            if pattern and not re.search(pattern, value):
                problems.append(f"{name}={value!r} does not match {pattern}")
        for req in schema["required"]:
            if not attrs.get(req):
                problems.append(f"required attribute {req!r} is missing")
        for child in inst:
            cname = local_name(child.tag)
            if "properties" not in props.get(cname, {}):
                problems.append(f"element {cname!r} is not an AAEI object field")
                continue
            sub, cattrs = props[cname]["properties"], plain_attributes(child)
            for name, value in cattrs.items():
                if name not in sub:
                    problems.append(f"{cname}.{name} is not declared by the schema")
                elif sub[name].get("enum") and value not in sub[name]["enum"]:
                    problems.append(f"{cname}.{name}={value!r} is not one of {sub[name]['enum']}")
            for req in props[cname].get("required", []):
                if req not in cattrs:
                    problems.append(f"{cname}.{req} is missing")
    return problems

def example_problems():
    """Every examples/*.json record must validate (keys starting with '_' are comments)."""
    paths = sorted(EXAMPLES_DIR.glob("*.json"))
    if not paths:
        return [f"no example records found in {EXAMPLES_DIR}"]
    problems = []
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        record = {k: v for k, v in record.items() if not k.startswith("_")}
        if not ok(record):
            problems.append(f"{path.name} does not validate")
    return problems

def run_supplementary():
    results = []

    def check(sc_id, name, fn):
        try:
            problems = fn()
        except Exception as e:
            problems = [str(e)]
        results.append({
            "id": sc_id, "category": "supplementary", "name": name,
            "status": "PASS" if not problems else "FAIL",
            "error": "; ".join(problems) if problems else None
        })

    # ── SC-01: delta.direction closed enumeration (metamodel constraint C2) ─
    def sc_01():
        base = {"role": "r", "problem": "p"}
        inline = (
            all(ok({**base, "delta": {"value": 1, "unit": "u", "direction": d}})
                for d in ["reduction", "increase", "neutral"]) and
            must_fail({**base, "delta": {"value": 1, "unit": "u", "direction": "sideways"}})
        )
        problems = [] if inline else ["inline assertions failed"]
        return problems + fixture_problems(
            "SC-01", "supplementary", "delta direction enumeration constraint")
    check("SC-01", "delta direction enumeration constraint", sc_01)

    # ── SC-02: XMI example is well-formed and closed-world consistent ──────
    check("SC-02", "XMI example well-formed and closed-world consistent", xmi_example_problems)

    # ── SC-03: all example records validate ───────────────────────────────
    check("SC-03", "Example records validate", example_problems)

    return results

def print_group(title, group):
    n_ok = sum(1 for r in group if r["status"] == "PASS")
    print(f"  {title:<25}  {n_ok}/{len(group)}")
    for r in group:
        icon = "✓" if r["status"] == "PASS" else "✗"
        print(f"    {icon} {r['id']}  {r['name']}")
        if r["error"]:
            print(f"         ERROR: {r['error']}")
    print()

# ── Run and report ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AAEI v1.2 MOF conformance test suite")
    parser.add_argument("--report", metavar="PATH",
                        help="write a machine-readable JSON report to PATH (default: no file is written)")
    args = parser.parse_args()

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
        print_group(cat.upper().replace('_',' '), [r for r in results if r["category"] == cat])

    supplementary = run_supplementary()
    sc_failed = [r for r in supplementary if r["status"] == "FAIL"]
    print_group("SUPPLEMENTARY CHECKS", supplementary)

    print("=" * 62)
    total = len(results)
    n_pass = len(passed)
    print(f"  RESULT: {n_pass}/{total} tests passing")
    print(f"  SUPPLEMENTARY: {len(supplementary) - len(sc_failed)}/{len(supplementary)} checks passing")
    if failed:
        print(f"  STATUS: ✗ {len(failed)} test(s) FAILED — see above")
    elif sc_failed:
        print(f"  STATUS: ✗ {len(sc_failed)} supplementary check(s) FAILED — see above")
    else:
        print(f"  STATUS: ✓ AAEI v1.2 MOF CONFORMANCE VERIFIED")
    print("=" * 62)

    if args.report:
        report = {
            "standard": "AAEI v1.2 — AI Accountability Evidence Interchange",
            "mof_version": "MOF 2.5.1 (formal/16-11-01)",
            "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "schema": "schemas/aaei_schema_v1_2.json",
            "repository": "github.com/ValueLogicsAI/AAEI",
            "license": "Apache 2.0",
            "summary": {
                "total": total,
                "passed": n_pass,
                "failed": len(failed),
                "conformant": n_pass == total
            },
            "results": results,
            "supplementary_summary": {
                "total": len(supplementary),
                "passed": len(supplementary) - len(sc_failed),
                "failed": len(sc_failed)
            },
            "supplementary": supplementary
        }
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\n  Report written: {args.report}")

    sys.exit(0 if not failed and not sc_failed else 1)
