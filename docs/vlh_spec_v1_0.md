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
Value Logic Hash = SHA-256 fingerprint of a business logic contract —
not the files, but the meaning: what the system must do, and what it
must prove.
```

---

## Why it exists

A file hash proves: *these files did not change.*

A Value Logic Hash proves: *this business logic, behavior, and value promise
did not change — even if the generated code is completely different.*

This distinction matters when:

- Regenerating a platform with a new framework
- Migrating from one cloud provider to another
- Refactoring implementation without changing business intent
- Proving to an auditor that modernization preserved the original logic

---

## Properties of the hash input

The VLH is computed over a canonical representation of a system's business
logic contract. The specific composition of that representation, and the
canonicalization procedure applied to it, are part of the ValueLogics
implementation layer and are not published.

What the specification does state:

- The input is **semantic**, not syntactic. It describes what the system must
  do and what it must prove — never how it is implemented.
- The input is **deterministic**. The same logic contract yields the same hash
  on any conformant implementation.
- The input is **order-independent**. Rearranging equivalent content does not
  change the hash.
- The output is a 64-character SHA-256 hexadecimal string.

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
  - Record-level identifier or integrity fields
  - Any implementation detail
```

The VLH captures *what the system must do*, not *how it does it*. Anything that
changes when the implementation changes is excluded by design — that exclusion
is what makes the hash stable across regeneration.

---

## The hash chain

```
1. source_snapshot_hash   ← SHA-256 of original source files
                             (proves what was analyzed)
         ↓
2. value_logic_hash (VLH) ← SHA-256 of the extracted logic contract
                             (proves what business meaning was found)
         ↓
3. generated_surface_hash ← SHA-256 of emitted artifacts
                             (proves what was produced)
         ↓
4. functional_equiv_hash  ← SHA-256 of behavior test results
                             (proves the generated system behaves correctly)
         ↓
5. aaei_proof_hash        ← SHA-256 of the full draft-profile record
                             (proves the evidence record is intact)
```

Each hash serves a distinct audit purpose and they are not interchangeable.
Steps 1, 2 and 5 are fields of the draft extended profile
(`drafts/ldr_vlh_extended_profile_draft.json`). They are not AAEI v1.2 fields.
Steps 3 and 4 are produced by the implementing system.

---

## Verification rule

Before any regeneration:

1. The current logic contract is re-hashed.
2. The result is compared against the VLH sealed at signing.
3. Match → regeneration proceeds.
4. Mismatch → regeneration is blocked, and a diff report identifies what changed.

The comparison is performed by the implementing system. Its output is a
pass/fail result and a diff report. Neither the canonical representation nor the
procedure that produced the hash appears in that output.

---

## The VMware parallel

VMware's vMotion could migrate a running virtual machine from one physical host
to another. The VM's identity — its memory state, CPU registers, network
connections — was preserved exactly even though the underlying hardware changed
completely.

The VLH does the same thing for business logic.

The implementation host changes.
The logic identity does not.

```
VMware:          virtualizes compute
ValueLogics:     virtualizes business logic

VMware:          needed VM identity (MAC address, UUID)
ValueLogics:     needs VLH (logic fingerprint)
```

---

## Relationship to LDR

LDR measures compression efficiency.
VLH proves compression was lossless.

A ratio on its own says only that a system got smaller, which is not a claim
worth making — a system can be made smaller by discarding behavior. A VLH on its
own says the logic is intact but carries no measure of what was gained.

A validated LDR report therefore requires both. This is a rule of the draft
standard, not an achieved result: no LDR report has yet been independently
validated under it.

---

## Draft profile field reference

```json
{
  "vlh":                  "SHA-256 hex string (64 chars)",
  "ldr_ratio":            "decimal",
  "source_snapshot_hash": "SHA-256 hex string (64 chars)"
}
```

Defined in the draft extended profile
(`drafts/ldr_vlh_extended_profile_draft.json`). Not part of AAEI v1.2.
Unsubmitted.
