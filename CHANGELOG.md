# AAEI Changelog

This file records two separate things and keeps them apart:

1. **AAEI v1.2** — the proposed OMG standard.
2. **A draft extension profile** (ESG / VLH / LDR) — not part of AAEI v1.2.

---

## AAEI v1.2 — Proposed OMG standard (12 public fields, BMM-mapped)

AAEI v1.2 is a proposed OMG standard; Letters of Intent identify it for submission.
It is the twelve-field, BMM-mapped standard.
Its only governing schema is `schemas/aaei_schema_v1_2.json`.

### Public fields (12)

`role`, `problem`, `bau_measure`, `ps_measure`, `motivation_ref`,
`desired_result`, `delta`, `evidence_chain_id`, `hash`, `lifecycle_mode`,
`proof_package_ref`, `drift_status`

- Required: `role`, `problem`. The other ten fields are nullable.
- `additionalProperties: false` — no other field may appear in a
  conformant record.
- BMM bridge fields: `motivation_ref` and `desired_result`
  (see `mappings/aaei_to_bmm_mapping.md`). AAEI does not modify BMM.
- MOF M2 metamodel: `mof/aaei_mof_metamodel.md`.
- Conformance: the 18 tests in `tools/conformance/` pass 18/18 against
  `schemas/aaei_schema_v1_2.json`
  (see `tools/conformance/conformance_report.json`).
- Examples: `examples/example_01_standard_application.json`,
  `examples/example_02_ai_agent.json`,
  `examples/example_03_esg_extended.json`.
- Prior art timestamp: June 26, 2026 (see `NOTICE`).

AAEI v1.2 defines no ESG, VLH, or LDR fields.
`examples/example_03_esg_extended.json` expresses an ESG claim using the
twelve fields only.

---

## Test tooling — September 21, 2026

No change to the AAEI v1.2 schema or to the inline assertions of the 18
conformance tests. The conformance count stays 18.

- `requirements.txt` added: `jsonschema==4.26.0` (Python 3.10 or later).
- `tools/conformance/run_conformance_suite.py` and `tools/validate_aaei.py`
  no longer run `pip install`. If `jsonschema` is missing they print the
  install command and exit with code 2.
- The runner now executes each test's fixture file: the fixture's `id`,
  `category` and `name` must match the test, every `pass_fixture*` must
  validate, and a non-null `fail_fixture` must be rejected.
- Fixture names reconciled with the runner and the July 9, 2026 report:
  CT-15 "String field Unicode encoding" and CT-18 "drift_status closed
  enumeration". The two fixture files were renamed to match. Fixture
  descriptions are unchanged.
- Three supplementary checks added, counted separately from the 18:
  SC-01 `delta.direction` closed enumeration (metamodel constraint C2);
  SC-02 `mof/aaei_xmi_example.xml` is well-formed and uses only field names,
  enumeration values and the hash pattern the schema allows; SC-03 every
  record in `examples/` validates.
- `python3 tools/validate_aaei.py --examples` validates all example records
  in one command. `--record` accepts more than one path.
- The runner writes no file unless `--report PATH` is given, so a run no
  longer modifies the tracked `conformance_report.json`.
- `datetime.utcnow()` replaced with a timezone-aware UTC timestamp.
- `.github/workflows/conformance.yml` added: installs `requirements.txt`,
  runs the suite and the example validation, and fails if a tracked file
  changed.

Not tested, because the repository defines no rule to test against:
XMI-to-JSON value mapping, XMI schema validation, and whether a
`drift_status` value is derivable from the measures.

---

## Repository reconciliation — September 21, 2026

A merge on July 27, 2026 (`110780e`) added a second, 14-field schema that was
also labelled v1.2, replaced the README, and added this changelog with the
14-field lineage narrated as AAEI v1.0 → v1.1 → v1.2. This reconciliation
restores the repository to the twelve-field standard without deleting that work.

- `README.md` restored to the 12-field / BMM version from commit `ef27444`,
  with four corrections: the OMG status sentence added; trailing-space line
  breaks rewritten as backslash line breaks; the repository tree updated to
  match the repository; and the submission paper marked NOT INCLUDED (the
  previously referenced
  `docs/AAEI_OMG_Submission_v1.2.docx` is not in this repository).
- `schemas/aaei_v1_2.json` moved unchanged to
  `drafts/ldr_vlh_extended_profile_draft.json`, then relabelled as a draft:
  `_NOTE` added; `title`, `$id`, `description`, `version`, `status`, section
  comments and per-field group labels changed; `omg_submission_target` and
  `prior_art_date` removed. Field names, types, patterns, enums and
  `required` are unchanged.
- `examples/ibm_cobol_sam1_v1_2.json` and
  `examples/event_concierge_hq_v1_2.json` moved to `drafts/examples/`; their
  `_comment` lines now identify them as draft-profile examples, and the
  unsubstantiated `vlh_status` and `vlh_last_verified` values were removed.
- `docs/vlh_spec_v1_0.md` and `docs/homepage_portable_logic_copy.md`
  relabelled as draft portable-logic / LDR / VLH work, separate from
  AAEI v1.2.
- `NOTICE`: "Submitted to: …" replaced with "Letters of Intent identify
  AAEI v1.2 for submission to: …".
- `drafts/README.md` added.
- This changelog rewritten.
- No change to the governing schema, the conformance tests, the validator,
  the BMM mapping, or the MOF metamodel.

---

## Draft extension profile — ESG / VLH / LDR (not part of AAEI v1.2)

The material below is a **separate draft extension profile**. It is
unsubmitted, it is not covered by the AAEI v1.2 conformance suite, and a
record written to it does not validate against the AAEI v1.2 schema.
See `drafts/README.md`.

Files:

- `drafts/ldr_vlh_extended_profile_draft.json` — 14-field draft schema
- `drafts/examples/ibm_cobol_sam1_v1_2.json`
- `drafts/examples/event_concierge_hq_v1_2.json`
- `docs/vlh_spec_v1_0.md` — VLH specification. It is kept in the repository,
  but VLH is not part of AAEI v1.2.
- `docs/homepage_portable_logic_copy.md` — draft portable-logic copy.

### Field groups in the draft profile

An earlier version of this changelog listed these groups as AAEI v1.0.0
(dated June 26, 2026), v1.1.0 (dated June 29, 2026) and v1.2.0 (dated
July 2, 2026). They are field groups of the draft profile, not versions of
AAEI.

- Core (8): `role`, `problem_statement`, `bau_measure`, `ps_measure`,
  `delta`, `fib_id`, `sha256_hash`, `lifecycle_mode`
- ESG (3): `energy_proxy_pct`, `token_reduction_pct`,
  `network_reduction_pct`
- Portable logic (3): `vlh` (Value Logic Hash), `ldr_ratio` (Logic Density
  Ratio), `source_snapshot_hash`

### LDR figures

The LDR values 0.15 (Event Concierge HQ: 1,211 ÷ 8,071) and 0.13 (IBM COBOL
SAM1/SAM2: 120 ÷ 922) are published example calculations on stated line
counts. The source snapshots are not in this repository. They are not
audited results and they are not AAEI v1.2 proof.
