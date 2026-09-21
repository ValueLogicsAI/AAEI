# Value Logic Hash (VLH) — Specification v1.0
**DRAFT · ValueLogics.ai LLC · July 2, 2026**

> **Status: DRAFT — separate from AAEI v1.2.**
> This document is draft portable-logic / LDR / VLH work. VLH is not an
> AAEI v1.2 field, and nothing here is submitted, tested, or covered by the
> AAEI v1.2 conformance suite. AAEI v1.2 is the twelve-field schema at
> `schemas/aaei_schema_v1_2.json`. See `drafts/README.md`.

---

## Definition

```
Value Logic Hash = SHA-256 fingerprint of the business logic
contract — not the files, but the meaning: the business problem,
every rule, every metric, the goal measures, the workflow
definitions, the API contracts, the functional equivalence tests,
and the proof requirements required to regenerate and prove a system.
```

---

## Why it exists

A file hash proves: *these files did not change.*

A Value Logic Hash proves: *this business logic, behavior, and
value promise did not change — even if the generated code is
completely different.*

This distinction matters when:
- Regenerating a platform with a new framework
- Migrating from one cloud provider to another
- Refactoring implementation without changing business intent
- Proving to an auditor that modernization preserved the original logic

---

## What goes into the VLH

```
VLH = sha256(canonical_json({
  "problem_statement":          string,
  "role":                       string,
  "bau_measure":                string | number,
  "goal_measure":               string,
  "business_rules":             sorted list of rule statements,
  "workflow_definitions":       sorted list of workflow IDs,
  "api_contracts":              sorted list of endpoint signatures,
  "functional_equivalence_tests": sorted list of test identifiers,
  "proof_requirements":         sorted list of proof field IDs,
  "evidence_requirements":      sorted list of evidence field IDs
}))
```

**Critical rules for deterministic computation:**
- JSON keys must be sorted alphabetically (`sort_keys=True`)
- All string values must be normalized (trim whitespace, lowercase)
- Lists must be sorted before hashing
- Encoding: UTF-8
- No timestamps, no IDs, no file paths in the hash input
  (those change — the logic does not)

---

## What does NOT go into the VLH

```
NOT included:
  - File names or paths
  - LOC counts
  - Timestamps
  - Framework names
  - Cloud provider names
  - Package versions
  - fib_id or sha256_hash (those are record-level fields)
  - Any implementation detail
```

The VLH captures *what the system must do*, not *how it does it*.

---

## The hash chain

```
1. source_snapshot_hash   ← SHA-256 of original source files
                             (proves what was analyzed)
         ↓
2. value_logic_hash (VLH) ← SHA-256 of extracted logic contract
                             (proves what business meaning was found)
         ↓
3. generated_surface_hash ← SHA-256 of emitted artifacts
                             (proves what was compiled)
         ↓
4. functional_equiv_hash  ← SHA-256 of behavior test results
                             (proves the generated system behaves correctly)
         ↓
5. aaei_proof_hash        ← SHA-256 of the full draft-profile record
                             (proves the evidence record is intact)
```

Steps 3 and 4 are computed by the VDSC implementation layer.
Steps 1, 2, and 5 are fields of the draft extended profile
(`drafts/ldr_vlh_extended_profile_draft.json`). They are not AAEI v1.2 fields.

---

## Verification rule

Before any regeneration:
1. Recompute VLH from current KV value map
2. Compare to VLH sealed in `scf_contract` at signing
3. If match → regeneration proceeds
4. If mismatch → regeneration blocked + diff report showing what changed

The comparison happens inside the vault. The system outputs pass/fail plus a
diff report. The canonical field list that feeds the hash is not exposed in
that output.

---

## The VMware parallel

VMware's vMotion could migrate a running virtual machine from one
physical host to another. The VM's identity — its memory state, CPU
registers, network connections — was preserved exactly even though the
underlying hardware changed completely.

The VLH does the same thing for business logic.

The implementation host changes.
The logic identity does not.

```
VMware:          virtualizes compute
ValueLogics:     virtualizes business logic

VMware:          collapses servers into hosts
ValueLogics:     collapses codebases into value contracts

VMware:          needed VM identity (MAC address, UUID)
ValueLogics:     needs VLH (logic fingerprint)
```

---

## Examples

The rows below illustrate what a VLH would be computed from. They are
examples based on stated line counts, not independently checked results.

| System | VLH would be computed from | Status |
|--------|----------------------------|--------|
| Event Concierge HQ | 1,211 KV lines from 8,071 LOC Lovable app | Example |
| IBM COBOL SAM1/SAM2 | 120 KV lines from 922 LOC COBOL source | Example |
| Acme Industrial Corp SF | bc_acme_sf_001 VDSC contract | Example |

---

## Relationship to LDR

LDR measures compression efficiency.
VLH proves compression was lossless.

```
LDR alone:   "We compressed 8,071 lines to 1,211 lines."
VLH alone:   "The logic contract is intact." (but no compression measure)
LDR + VLH:   "We compressed 85% — and every rule, metric,
              and proof obligation survived. Cryptographically proven."
```

The quoted statements above, including "Cryptographically proven", are
illustrative future-state language showing what each kind of report would
say. They are not achieved results.

A validated LDR standard report requires both.

---

## Draft profile field reference

```json
{
  "vlh":                  "SHA-256 hex string (64 chars)",
  "ldr_ratio":            0.15,
  "source_snapshot_hash": "SHA-256 hex string (64 chars)"
}
```

Defined in the draft extended profile
(`drafts/ldr_vlh_extended_profile_draft.json`). Not part of AAEI v1.2. Unsubmitted.
