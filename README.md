# AAEI — AI Accountability Evidence Interchange

**The missing evidence layer for AI agents and AI-enabled systems.**

Every AI agent makes an implicit promise: that running it produces value for someone.\
Almost none record that promise in a form anyone can check later.\
**AAEI gives that promise a shape.**

---

| | |
|---|---|
| **Version** | 1.2 |
| **Status** | Public draft · Proposed OMG standard |
| **License** | Apache License 2.0 |
| **Publisher** | ValueLogics.ai LLC |
| **Repository** | github.com/ValueLogicsAI/AAEI |
| **Prior art** | June 26, 2026 (public timestamp) |
| **MOF conformance** | ✓ 18/18 tests passing |
| **OMG target** | Q3 2026 · Orlando, FL · September 14–18, 2026 |

---

## The Problem

The OMG Business Motivation Model (BMM) defines the structure of business intent.\
It answers: *why does an organization act?*

**BMM does not record whether that intent produced a measurable outcome.**

That gap has been open for eleven years (BMM v1.3, 2015).

In the era of AI agents, this gap is critical. Organizations are deploying AI systems, automated workflows, and AI-enabled applications — with no baseline, no goal measure, no actual evidence, and no board-ready proof that any of it worked.

Auditors cannot verify AI claims. Boards cannot allocate capital on evidence. Procurement organizations cannot screen vendors. Regulators cannot audit outcomes.

**Not because the results aren't real. Because there is no standard to record them.**

---

## The Solution

AAEI is the evidence abstraction that closes the BMM gap.

```
BMM   →  Why the organization acts   (intent)
AAEI  →  Whether the action delivered  (evidence)
```

Twelve public fields. One question answered:

> **What was this AI system supposed to do, and did it?**

AAEI is deliberately minimal — not a runtime, not a scoring method, not a vendor's internal contract language. It exists so that any organization, auditor, standards body, or AI agent runtime can state and later verify one accountability claim about any AI system.

---

## Why This Matters Now

**For enterprises:** AI spend without accountability is AI spend without governance. AAEI gives finance, security, compliance, and board stakeholders a standard evidence format to request and verify.

**For AI vendors:** The organizations that prove value will win the next renewal. The organizations that can only claim it will not.

**For agent-to-agent commerce:** As autonomous agents begin transacting with each other, trust requires proof. AAEI is the evidence interchange layer that makes agent-to-agent accountability verifiable — not by assertion, but by standard.

**For standards bodies:** BMM defined motivation. Eleven years later, the evidence layer it requires is here.


## The A2A Vision — Agent-to-Agent Commerce Built on Evidence

The next wave of AI deployment is not agents serving humans. It is agents transacting with agents — autonomous systems that identify gaps, match capabilities, negotiate outcomes, and settle transactions without human intermediation at every step.

No current standard governs what an agent must prove before another agent trusts it. No current standard defines how an agent-to-agent transaction settles on the basis of verified value rather than claimed capability. Agents today transact on assertion. The standard they need is an evidence interchange format — a common record that travels with every agent, stating what it was deployed to deliver and whether it did.

**AAEI is that record.**

When one agent's value proposition addresses another agent's verified gap — and both carry AAEI-conformant evidence records — the transaction has a basis for settlement that is auditable, portable, and standard. The gap between what was promised and what was delivered is no longer a matter of trust. It is a matter of record.

This is why AAEI is proposed to the OMG AI Task Force alongside the Business Architecture Task Force. OMG standardized model-driven systems. The agent economy needs evidence-driven commerce. AAEI is the evidence interchange standard that makes it possible — built on the same MOF metamodel foundation OMG has used since 2001, extending the BMM intent model with the evidence layer it has needed since 2015, and following the CWM interchange format pattern OMG adopted in 2003.

The standard is minimal by design. AAEI does not define how agents are built, how they communicate, how they govern themselves, or how transactions are settled. It defines only what an accountability evidence record must contain. Every other concern remains open for OMG member organizations to implement — and to differentiate on.

---

## Quick Start

```bash
# Clone
git clone https://github.com/ValueLogicsAI/AAEI
cd AAEI

# Install the one dependency (jsonschema, pinned). Requires Python 3.10 or later.
python3 -m pip install -r requirements.txt

# Validate an example record
python3 tools/validate_aaei.py --record examples/example_02_ai_agent.json

# Validate all three example records
python3 tools/validate_aaei.py --examples

# Run the full MOF conformance suite
python3 tools/conformance/run_conformance_suite.py
```

Expected: `18/18 tests passing · STATUS: ✓ AAEI v1.2 MOF CONFORMANCE VERIFIED`

The suite also runs three supplementary checks (SC-01 to SC-03), counted separately from the 18 conformance tests. It writes no file unless you pass `--report PATH`. The tools do not install anything: if `jsonschema` is missing they stop with an error and exit code 2.

---

## The 12 Public Fields

| Field | Answers |
|---|---|
| `role` | Who was this system meant to serve? |
| `problem` | What problem, constraint, or risk existed? |
| `bau_measure` | What was the baseline before intervention? |
| `ps_measure` *(Goal Measure)* | What outcome was promised? |
| `motivation_ref` | Which BMM motivation element drove this? *(BMM bridge)* |
| `desired_result` | What end state was the motivation targeting? *(BMM bridge)* |
| `delta` | What changed between baseline and actual? |
| `evidence_chain_id` | How is this record linked to its source events? |
| `hash` | How can the record be integrity-checked? |
| `lifecycle_mode` | What accountability lifecycle applies? |
| `proof_package_ref` | Where is the externalized proof package? |
| `drift_status` | Has value delivery drifted from goal? |

> `ps_measure` is the schema field name retained for backward compatibility.\
> It is always displayed as **Goal Measure** in ValueLogics tooling and documentation.

Two fields — `motivation_ref` and `desired_result` — provide direct structural bridges to existing BMM models. AAEI does not modify BMM. It extends it.

---

## Example Record

```json
{
  "role": "support-triage-agent",
  "problem": "Manual ticket routing causes 4-hour median delay before first response",
  "bau_measure": { "value": 240, "unit": "minutes" },
  "ps_measure":  { "value": 30,  "unit": "minutes" },
  "motivation_ref": "bmm://goals/reduce-support-cycle-time",
  "desired_result": "30-minute median first-response time",
  "delta": { "value": 210, "unit": "minutes", "direction": "reduction" },
  "evidence_chain_id": "ec_8f21a4b3c9d2",
  "hash": "sha256:9a31b7f2c4e8d6a1",
  "lifecycle_mode": "active",
  "drift_status": "on_track",
  "proof_package_ref": "https://evidence.valuelogics.ai/proof/ec_8f21a4b3c9d2"
}
```

---

## Position in the OMG Stack

AAEI is proposed as a MOF-conformant M2 metamodel — peer to UML, BMM, CWM, and BPMN.

```
M3  MOF 2.5.1  (formal/16-11-01)       The metamodeling language
M2  BMM v1.3   (formal/08-09-02)       Why the organization acts  ← AAEI extends this
M2  AAEI v1.2  (proposed)              Whether the action delivered
M1  AAEI accountability contracts      Specific evidence commitments
M0  Runtime evidence records           Actual measured outcomes
```

AAEI follows the CWM precedent (formal/03-03-02, 2003):\
standardize the interchange schema — leave the implementation to the vendor.

**MDA starts with a platform-independent model.**\
**AAEI starts one level higher — with a value-independent contract that defines what the system must prove.**

---

## What AAEI Does Not Prescribe

By design, AAEI is silent on:

- How value is calculated
- How evidence is collected
- How runtime behavior is governed
- How drift is detected
- How proof packages are generated
- How security gates are implemented

These are implementation concerns — left open so any organization can build a conformant system its own way. The standard defines the receipt, not the engine.

---

## Repository Structure

```
AAEI/
├── README.md
├── CHANGELOG.md
├── LICENSE                                Apache 2.0
├── NOTICE                                 Prior art declaration
├── requirements.txt                       Pinned dependency (jsonschema)
│
├── .github/
│   └── workflows/
│       └── conformance.yml               CI: runs the suite on a clean checkout
│
├── schemas/
│   └── aaei_schema_v1_2.json             JSON Schema (Draft 2020-12)
│
├── examples/
│   ├── example_01_standard_application.json
│   ├── example_02_ai_agent.json
│   └── example_03_esg_extended.json
│
├── mappings/
│   ├── aaei_to_bmm_mapping.md            AAEI ↔ BMM field mapping
│   └── aaei_cwm_mda_positioning.md       Position in OMG stack
│
├── mof/
│   ├── aaei_mof_metamodel.md             MOF M2 metaclass specification
│   └── aaei_xmi_example.xml              XMI serialization example
│
├── tools/
│   ├── validate_aaei.py                  CLI record validator
│   └── conformance/
│       ├── run_conformance_suite.py      18/18 conformance test runner
│       ├── ct-01 through ct-18 .json    Individual test fixtures (executed by the runner)
│       ├── sc-01 .json                   Supplementary check fixture
│       └── conformance_report.json      Machine-readable pass report (July 9, 2026 run)
│
├── docs/                                  Draft material — not part of AAEI v1.2
│   └── vlh_spec_v1_0.md                  Draft VLH specification
│
└── drafts/                                Draft LDR / VLH extended profile — not part of AAEI v1.2
    ├── README.md
    ├── ldr_vlh_extended_profile_draft.json
    └── examples/
        ├── ibm_cobol_sam1_v1_2.json
        └── event_concierge_hq_v1_2.json
```

The OMG submission paper is **NOT INCLUDED** in this repository.

---

## MOF Conformance

AAEI v1.2 has **18/18 MOF conformance tests passing** across five categories:

| Category | Tests | Status |
|---|---|---|
| Structural | CT-01 to CT-04 | ✓ 4/4 |
| Semantic | CT-05 to CT-08 | ✓ 4/4 |
| Generation | CT-09 to CT-12 | ✓ 4/4 |
| Interchange | CT-13 to CT-16 | ✓ 4/4 |
| Evidence Integrity | CT-17 to CT-18 | ✓ 2/2 |

Run them yourself: `python3 tools/conformance/run_conformance_suite.py`

---

## OMG Submission

AAEI v1.2 is a proposed OMG standard; Letters of Intent identify it for submission.

AAEI v1.2 is proposed to three OMG working groups for the Q3 2026 Technical Meeting:

1. **Business Architecture Task Force** — as the evidence layer BMM has needed since 2015
2. **AI Task Force** — as the accountability standard for AI agent governance and A2A commerce
3. **MDA Working Group** — as the value evidence layer above the platform-independent model

**LOI deadline:** August 17, 2026\
**Target meeting:** Q3 2026 · Orlando, FL · September 14–18, 2026\
**Contact:** as@valuelogics.ai\
**Full submission paper:** NOT INCLUDED in this repository

---

## Intellectual Property

AAEI v1.2 is Apache License 2.0. No patents are asserted or pending.

The evidence interchange schema is fully public — clone it, implement it, build on it.

The value contract execution layer, ROI calculation methodology, proof generation system, and compiler are proprietary trade secrets of ValueLogics.ai LLC and are not part of this repository. This mirrors the CWM precedent exactly: OMG adopted the warehouse metadata interchange schema in 2003 without requiring IBM, Oracle, or Unisys to disclose their warehouse engines.

---

## Contributing and Adoption

Organizations interested in implementing AAEI, co-submitting to OMG, or joining the standards discussion are welcome to open an issue or contact as@valuelogics.ai.

If you are building AI agents, AI-enabled applications, or agentic infrastructure — and you want your systems to carry verifiable accountability evidence — AAEI is designed for you to implement today.

---

*Copyright 2026 ProveIT ROI LLC d/b/a ValueLogics.ai LLC · Apache License 2.0*
