# AAEI v1.2 — MOF M2 Metamodel Specification

**Standard:** AI Accountability Evidence Interchange  
**Version:** 1.2  
**MOF conformance:** MOF 2.5.1 (formal/16-11-01) at M2  
**Conformance tests:** 18/18 passing (see tools/conformance/)  
**License:** Apache 2.0  
**Repository:** github.com/ValueLogicsAI/AAEI  

---

## 1. Metamodel Layer

AAEI occupies the M2 layer of the OMG four-layer metamodel architecture,
peer to UML, BMM, CWM, and BPMN. It conforms to MOF 2.5.1 as its M3.

```
M3  MOF 2.5.1
M2  AAEI v1.2 (this specification)
M1  AAEI accountability contracts (specific evidence commitments)
M0  Runtime evidence records (actual measured outcomes)
```

---

## 2. Primary Metaclass: AccountabilityEvidence

```
AccountabilityEvidence
├── role               : String          [1]   required
├── problem            : String          [1]   required
├── bau_measure        : BaselineMetric  [0..1] nullable
├── ps_measure         : GoalMeasure     [0..1] nullable  (displays as "Goal Measure")
├── motivation_ref     : BMM_MotivRef    [0..1] nullable  (BMM bridge)
├── desired_result     : BMM_DesiredRes  [0..1] nullable  (BMM bridge)
├── delta              : OutcomeDelta    [0..1] nullable
├── evidence_chain_id  : String          [0..1] nullable
├── hash               : IntegrityHash  [0..1] nullable
├── lifecycle_mode     : LifecycleMode  [0..1] nullable
├── proof_package_ref  : String          [0..1] nullable
└── drift_status       : DriftStatus    [0..1] nullable
```

**Closed world:** additionalProperties = false.
No attributes beyond these 12 may appear in a conformant M1 instance.

---

## 3. Supporting Type Definitions

### BaselineMetric / GoalMeasure
```
{
  value : Real    [1]   required
  unit  : String  [1]   required
}
```

### OutcomeDelta
```
{
  value     : Real                            [1]
  unit      : String                          [1]
  direction : Enumeration {reduction, increase, neutral}  [1]
}
```

### Enumerations

**LifecycleMode** — four literals:
- `active` — system is deployed and being measured
- `completed` — measurement cycle complete, outcome recorded
- `suspended` — measurement paused
- `archived` — record retained for audit, system retired

**DriftStatus** — three literals:
- `on_track` — actual ≥ goal measure
- `at_risk` — actual trending below goal measure
- `drifting` — actual has fallen below goal measure threshold

**IntegrityHash** — pattern constraint:
- Format: `sha256:{hex string, minimum 6 characters}`
- Example: `sha256:9a31b7f2c4e8d6a1`

---

## 4. Structural Constraints (OCL-expressible)

```
-- C1: hash presence implies evidence_chain_id presence
context AccountabilityEvidence
inv HashRequiresChain:
  self.hash <> null implies
  (self.evidence_chain_id <> null and self.evidence_chain_id.size() > 0)

-- C2: delta direction is closed enumeration
context OutcomeDelta
inv ValidDirection:
  Set{'reduction', 'increase', 'neutral'}->includes(self.direction)

-- C3: lifecycle_mode is closed enumeration
context AccountabilityEvidence
inv ValidLifecycle:
  self.lifecycle_mode = null or
  Set{'active','completed','suspended','archived'}->includes(self.lifecycle_mode)

-- C4: drift_status is closed enumeration
context AccountabilityEvidence
inv ValidDrift:
  self.drift_status = null or
  Set{'on_track','at_risk','drifting'}->includes(self.drift_status)
```

---

## 5. BMM Bridge Fields

`motivation_ref` and `desired_result` are nullable string references
that anchor an AAEI record to an existing BMM motivation model.

They do not require a live BMM model to be present.
They do not modify BMM's internal structure.
A conformant AAEI record is valid with or without these fields populated.

When populated, recommended format for `motivation_ref`:
`bmm://{element-type}/{element-identifier}`

---

## 6. XMI Serialization

See `mof/aaei_xmi_example.xml` for a MOF-conformant XMI serialization
of an AAEI M1 instance.

---

## 7. Conformance

Run the full conformance suite:
```bash
python3 tools/conformance/run_conformance_suite.py
```

Expected output: 18/18 tests passing across five categories:
structural (4) · semantic (4) · generation (4) · interchange (4) · evidence integrity (2)
