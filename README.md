# AAEI — AI Accountability Evidence Interchange
**Proposed OMG Standard · Apache 2.0 · v1.2.0**

> Author once. Generate anywhere. Prove it paid off.

---

## What is AAEI?

AAEI is an open standard for portable, verifiable AI accountability evidence.

It defines the minimum field set required to prove that an AI system,
generated platform, or automated workflow delivered what it promised —
across any vendor, platform, architecture, or regeneration cycle.

**OMG submission target: August 17, 2026**
**Prior art clock started: June 26, 2026**
**License: Apache 2.0**
**Maintained by: ValueLogics.ai LLC**

---

## The Problem AAEI Solves

Every AI platform today can generate software. None of them can prove
the generated software preserved the business logic it was supposed to implement.

When you regenerate a platform — new framework, new cloud provider,
new architecture — you get different files. The question no existing
standard answers is:

> Did the business logic survive? Are the rules, metrics, workflows,
> and proof obligations exactly what they were before?

File hashes prove files did not change.
**AAEI proves business logic did not change.**

---

## Portable Logic — The Core Concept

Traditional software locks business logic inside implementation files.
Change the framework, migrate the database, regenerate the platform —
and there is no standard way to prove the logic survived intact.

AAEI introduces **portable logic** — business intent, rules, metrics,
and proof obligations expressed as a standard evidence contract that
travels with the system regardless of how it is implemented.

```
Without AAEI:
  Business logic = trapped in code
  Regeneration   = hope nothing broke
  Audit trail    = none

With AAEI:
  Business logic = portable contract + VLH fingerprint
  Regeneration   = cryptographically verified continuity
  Audit trail    = immutable AAEI evidence record
```

The Value Logic Hash (VLH) — introduced in v1.2 — is the cryptographic
fingerprint of the portable logic contract. If VLH matches before and
after regeneration, the business logic was preserved exactly.
If it does not match, something changed — and the system can say
precisely what.

---

## Field Reference

### v1.0 — Core Fields (8)

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Who the value contract serves |
| `problem_statement` | string | Business problem being addressed |
| `bau_measure` | decimal | Baseline — pre-solution measurement |
| `ps_measure` | decimal | Post-solution measurement |
| `delta` | decimal | Measured or projected improvement |
| `fib_id` | string | Unique contract identifier |
| `sha256_hash` | string | Immutable proof anchor |
| `lifecycle_mode` | enum | `saas` / `full` / `agency` |

### v1.1 — ESG Fields (3 new)

| Field | Type | Description |
|-------|------|-------------|
| `energy_proxy_pct` | decimal | Runtime compute energy reduction (proxy) |
| `token_reduction_pct` | decimal | AI token exposure reduction |
| `network_reduction_pct` | decimal | Network transfer reduction |

### v1.2 — Portable Logic Fields (3 new)

| Field | Type | Description |
|-------|------|-------------|
| `vlh` | string | Value Logic Hash — SHA-256 fingerprint of the canonical logic contract (rules + metrics + workflows + proof requirements). Proves logic continuity across regeneration. |
| `ldr_ratio` | decimal | Logic Density Ratio — authored KV lines ÷ source LOC analyzed. Measures compression efficiency. Lower = better. Industry baseline = 1.0. |
| `source_snapshot_hash` | string | SHA-256 of original source files before ValueLogics processing. Proves provenance of what was analyzed. |

**Total: 14 fields across 3 versions.**

---

## The LDR Standard

LDR (Logic Density Ratio) is a portable, auditable measure of
how efficiently business logic has been compressed into a
canonical representation.

```
LDR = authored KV lines ÷ source LOC analyzed

Examples:
  Event Concierge HQ (Lovable → ValueLogics):
    LDR = 1,211 ÷ 8,071 = 0.15  (85% reduction)

  IBM z/OS COBOL SAM1/SAM2:
    LDR = 120 ÷ 922 = 0.13  (87% reduction)

  Industry baseline (no compression):
    LDR = 1.0
```

A validated LDR report MUST include a VLH proving that the
extracted business intent, rules, metrics, workflows, and
success conditions are preserved across regeneration.

**The files may change. The logic contract must not.**

---

## The Value Logic Hash (VLH)

VLH is the cryptographic fingerprint of the business logic
contract — not the files, but the meaning.

```
VLH = sha256(
  problem_statement +
  role +
  bau_measure +
  goal_measure +
  business_rules +
  workflow_definitions +
  api_contracts +
  functional_equivalence_tests +
  proof_requirements +
  evidence_requirements
)
```

### Hash Chain

```
source_snapshot_hash     ← what was analyzed (files)
        ↓
value_logic_hash (VLH)  ← what was extracted (meaning)
        ↓
generated_surface_hash   ← what was emitted (artifacts)
        ↓
functional_equiv_hash    ← what was verified (behavior)
        ↓
aaei_proof_hash          ← what was proven (ROI + ESG)
```

### Why it matters

```
Normal hash:   "These files did not change."
VLH:           "This business logic, behavior, and value
                promise did not change — even if the
                generated code is completely different."
```

### The VMware Parallel

VMware virtualized physical compute.
VMware collapsed many physical servers into one logical host.
VMware needed VM identity to prove a migrated VM was the same VM.

ValueLogics virtualizes business logic.
ValueLogics collapses many lines of brittle application code
into one semantic logic contract.
ValueLogics needs the VLH to prove a regenerated platform
carries the same business logic as the original.

---

## Example AAEI Record (v1.2)

```json
{
  "role": "Operations / IT Leadership",
  "problem_statement": "Manual process overhead and unmeasured AI operating cost",
  "bau_measure": 8071,
  "ps_measure": 1211,
  "delta": 85.0,
  "fib_id": "fib_vl-esg-f47cfe2677fb",
  "sha256_hash": "c43e712c0d8b9e6240c8a1f2b3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2",
  "lifecycle_mode": "saas",
  "energy_proxy_pct": 17.1,
  "token_reduction_pct": 85.0,
  "network_reduction_pct": 98.1,
  "vlh": "a3f9e2c1d8b47f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2",
  "ldr_ratio": 0.15,
  "source_snapshot_hash": "f47cfe2677fb3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b"
}
```

---

## Proof Points

| Metric | Value | Source |
|--------|-------|--------|
| LDR — Event Concierge HQ | 0.15 | open_lovable.zip · wc -l verified |
| LDR — IBM COBOL SAM1/SAM2 | 0.13 | github.com/IBM/zopeneditor-sample · wc -l verified |
| Token reduction | 85.0% | Measured code surface proxy |
| Network reduction | 98.1% | Direct benchmark — 166,500 → 3,200 bytes |
| Runtime latency reduction | 17.1% | Direct benchmark — 210ms → 174ms |
| Package footprint reduction | 99.7% | Direct benchmark — 338 MB → 1 MB |
| Developer hours saved | 272 hrs ($40,800) | Estimated @ $150/hr |
| Prior art clock | June 26, 2026 | AAEI v1.0 published |

---

## Roadmap

| Version | Fields | Status |
|---------|--------|--------|
| v1.0 | 8 core fields | Published June 26, 2026 |
| v1.1 | + 3 ESG fields | Published June 29, 2026 |
| v1.2 | + 3 portable logic fields (VLH, LDR, snapshot) | This release |
| v1.3 | Functional equivalence hash · DriftWatch integration | Planned |

---

## OMG Submission

AAEI is being submitted to the Object Management Group (OMG)
as a proposed standard for AI accountability evidence interchange.

**Submission target: August 17, 2026**
**Primary contact: Dr. Morley Stone, IHMC (mstone@ihmc.us)**
**Submitter: Anthony Sarno, ValueLogics.ai LLC (as@valuelogics.ai)**

---

## Contact

Anthony Sarno, Founder & CEO
ValueLogics.ai LLC · Lake Worth Beach, FL
as@valuelogics.ai · +1(728)-230-5573
valuelogics.ai

*"Less to author. More proof."*
