# AAEI v1.2 → BMM Mapping

**AAEI v1.2 — AI Accountability Evidence Interchange**
Enhancement to OMG Business Motivation Model (BMM, formal/08-09-02, v1.3 2015)

---

## Overview

BMM defines the structure of business intent (why an organization acts).
AAEI adds the evidence abstraction that records whether that intent produced
a measurable outcome. The two standards are additive and coequal.

```
BMM   → answers: Why does the organization act?
AAEI  → answers: Did the action produce the motivated outcome?
```

---

## Field-Level Mapping

| AAEI Field | MOF Metaclass | BMM Concept | BMM Mapping |
|---|---|---|---|
| `role` | AccountabilityRole | Assessment.assessedElement | The organizational unit the system was deployed to serve |
| `problem` | ConstraintStatement | Assessment.conclusion | The identified gap, risk, or constraint the motivation addresses |
| `bau_measure` | BaselineMetric | Means.frequency (extended) | The quantified BAU condition before intervention |
| `ps_measure` (Goal Measure) | GoalMeasure | DesiredResult.quantification | The quantified desired result — what was promised |
| `motivation_ref` | BMM_MotivationRef | **Direct bridge → BMM.End or BMM.Means** | References the specific BMM element that motivated deployment |
| `desired_result` | BMM_DesiredResult | **Direct bridge → BMM.DesiredResult** | References the BMM DesiredResult being targeted |
| `delta` | OutcomeDelta | Assessment.conclusion (quantified) | The measured difference between baseline and actual |
| `evidence_chain_id` | EvidenceChainRef | Influence.category (extended) | Links this record to its chain of source events |
| `hash` | IntegrityHash | No BMM analog — new | SHA-256 integrity check for the evidence record |
| `lifecycle_mode` | LifecycleMode | Strategy.category (extended) | active / completed / suspended / archived |
| `proof_package_ref` | ProofPackageRef | No BMM analog — new | URI to externalized proof package |
| `drift_status` | DriftStatus | Assessment.result (extended) | on_track / at_risk / drifting |

---

## The BMM Bridge

Two AAEI fields provide direct structural bridges to BMM:

**`motivation_ref`** — references the specific BMM motivation element
(an End, a Means, or an Assessment) that drove the AI system's deployment.
Format: `bmm://{element-type}/{element-id}`
Example: `bmm://goals/reduce-support-cycle-time`

**`desired_result`** — references the BMM DesiredResult the motivation
was targeting. This is the business outcome statement from the BMM model.
Example: `"30-minute median first-response time"`

Both fields are nullable (multiplicity [0..1]). A valid AAEI record does
not require a live BMM model. When present, these fields anchor the
evidence record to an existing BMM motivation model.

---

## What AAEI Does Not Change in BMM

AAEI is additive. The full BMM taxonomy is unchanged:
Vision · Mission · Goal · Objective · Strategy · Tactic · Directive ·
Assessment · Influencer · Business Policy · Business Rule

AAEI adds one new structural concern: evidence.
BMM asks why. AAEI records whether.

---

## References

- BMM v1.3: formal/08-09-02, OMG, 2015
- AAEI v1.2: github.com/ValueLogicsAI/AAEI, Apache 2.0, June 26, 2026
- MOF 2.5.1: formal/16-11-01, OMG, 2016
