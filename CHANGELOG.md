# AAEI Changelog

## v1.2.0 — Portable Logic Fields
**Released: July 2, 2026**

### New fields (3)

- `vlh` — Value Logic Hash. SHA-256 fingerprint of the canonical logic
  contract — not files, but meaning. Proves business logic continuity
  across regeneration. If VLH matches before and after, every rule,
  metric, workflow, and proof obligation survived intact.

- `ldr_ratio` — Logic Density Ratio. Authored KV lines ÷ source LOC
  analyzed. Portable, auditable measure of logic compression efficiency.
  Industry baseline = 1.0. ValueLogics proof points: 0.15 (Event
  Concierge HQ) and 0.13 (IBM COBOL SAM1/SAM2). A validated LDR report
  requires all three v1.2 fields together — ratio alone is not the standard.

- `source_snapshot_hash` — SHA-256 of original source files before
  processing. Proves provenance of what was analyzed.

### Hash chain formalized
The complete proof chain from source analysis to board-ready ROI Replay
is now defined in the schema: source_snapshot → VLH → generated_surface
→ functional_equivalence → aaei_proof.

### VMware parallel documented
ValueLogics virtualizes business logic the same way VMware virtualized
compute. VLH is the VM identity equivalent — proves the migrated/
regenerated system carries the same logic as the original.

---

## v1.1.0 — ESG Fields
**Released: June 29, 2026**

### New fields (3)

- `energy_proxy_pct` — Runtime compute energy reduction proxy
- `token_reduction_pct` — AI token exposure reduction
- `network_reduction_pct` — Network transfer reduction

### Proof point
Event Concierge HQ benchmark: 17.1% latency, 98.1% network,
85.0% token exposure reduction. All measurements sourced from
direct benchmark instrumentation on converted Lovable application.

---

## v1.0.0 — Core Fields
**Released: June 26, 2026**

### Fields (8)
role, problem_statement, bau_measure, ps_measure, delta,
fib_id, sha256_hash, lifecycle_mode

### Prior art clock started
Apache 2.0 publication June 26, 2026.
OMG submission target August 17, 2026.
