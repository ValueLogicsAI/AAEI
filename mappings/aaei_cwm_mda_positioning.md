# AAEI in the OMG Standards Stack

## Position in the Four-Layer Metamodel

```
M3  MOF (formal/16-11-01)        The metamodeling language
    ↓
M2  UML · BMM · CWM · BPMN      Existing OMG metamodels
M2  AAEI v1.2 (proposed)        Evidence interchange metamodel (this standard)
    ↓
M1  AAEI accountability contracts  Specific evidence commitments
    ↓
M0  Runtime evidence records       Actual measured outcomes
```

AAEI is a peer M2 standard — not subordinate to any existing metamodel,
and not a replacement for any existing metamodel.

---

## Relationship to BMM

BMM (M2) defines business motivation.
AAEI (M2) defines business evidence.
Two fields bridge them: `motivation_ref` and `desired_result`.

```
BMM  →  Why the organization acts
AAEI →  Whether the action delivered
```

---

## Relationship to CWM

CWM (formal/03-03-02, 2003) established the OMG precedent for an
interchange format standard submitted by a private organization.

```
CWM pattern:   Define the warehouse metadata interchange schema (public)
               Leave warehouse engine implementation proprietary (vendor)

AAEI pattern:  Define the value evidence interchange schema (public)
               Leave value contract execution proprietary (ValueLogics)
```

---

## Relationship to MDA

MDA defines: PIM → PSM → Code

AAEI introduces a pre-model layer — a value-independent contract that
defines what the system must prove before a platform-independent model
is built.

```
MDA:   PIM → PSM → Code
AAEI:  Value Contract → PIM → PSM → Code → Evidence → Proof
```

MDA starts with a platform-independent model.
AAEI starts one level higher — with a value-independent contract
that defines what the system must prove.

---

## References

- CWM v1.1: formal/03-03-02, OMG, March 2003
- MDA: omg/03-06-01, OMG, 2003
- MOF 2.5.1: formal/16-11-01, OMG, 2016
- BMM v1.3: formal/08-09-02, OMG, 2015
- AAEI v1.2: github.com/ValueLogicsAI/AAEI, Apache 2.0
