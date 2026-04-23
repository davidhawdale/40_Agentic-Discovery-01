# Analyse by VC Pitch

> **Directive workflow** — triggered by user request. See `01-directives/04-generate-vc-pitch.md` for goal, inputs, and acceptance criteria.

## Approach

Build a VC-oriented one-pager from existing participant extracts: prepare deterministic inputs, run one synthesis agent, then apply deterministic validation before human review.

## Preconditions

- Required inputs:
  - `00-brief/strategic-research-brief.md`
  - `04-process/synthesise-archetypes/extracts/*.md`
  - `10-resources/templates/vc-pitch-output-template.md`
- Expected counts/shape:
  - Non-empty participant extract set
  - Brief and template files readable
- Stop conditions:
  - Missing strategic brief
  - Missing template file
  - Extract folder missing or empty

## Process

### Phase 1: Prepare Inputs

- Goal: Validate source inputs and build a manifest for synthesis.
- Run:
  1. `python3 02-workflows/generate-vc-pitch/prepare-vc-pitch-inputs.py`
- Input:
  - `00-brief/strategic-research-brief.md`
  - `04-process/synthesise-archetypes/extracts/*.md`
  - `10-resources/templates/vc-pitch-output-template.md`
- Output:
  - `04-process/04-generate-vc-pitch/manifest.json`
- PASS when:
  - Manifest is written with non-zero extract count
- WARN when:
  - No warnings defined for this phase
- FAIL when:
  - Script exits non-zero or manifest is not written
- If fail:
  - Correct the missing/bad input and rerun once

### Phase 2: Generate VC One-Pager

- Goal: Produce the one-page VC pitch narrative from prepared extracts.
- Run:
  1. `vc-pitch-writer`
- Input:
  - `04-process/04-generate-vc-pitch/manifest.json`
- Output:
  - `05-outputs/04-generate-vc-pitch/vc-pitch-one-pager.md`
- PASS when:
  - Output file exists and is non-empty
- WARN when:
  - Output exists but needs qualitative tightening (handled at human gate)
- FAIL when:
  - Output missing or empty
- If fail:
  - Re-run once with explicit correction instruction

### Phase 3: Verify Output

- Goal: Deterministically verify structural and constraint compliance.
- Run:
  1. `python3 02-workflows/generate-vc-pitch/verify-vc-pitch-output.py --file 05-outputs/04-generate-vc-pitch/vc-pitch-one-pager.md --extracts-dir 04-process/synthesise-archetypes/extracts --max-words 600`
- Input:
  - `05-outputs/04-generate-vc-pitch/vc-pitch-one-pager.md`
  - `04-process/synthesise-archetypes/extracts/*.md`
- Output:
  - Verification report in console (PASS/FAIL + checks)
- PASS when:
  - Verifier returns PASS
- WARN when:
  - No warnings defined for this phase
- FAIL when:
  - Verifier returns FAIL
- If fail:
  - Re-run Phase 2 once with specific correction, then rerun verification

### Human Review Gate (Use when required)

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger: Phase 3 returns PASS
- Read:
  - `05-outputs/04-generate-vc-pitch/vc-pitch-one-pager.md`
  - Phase 3 verifier output summary
- Summarise:
  - Word count result
  - Required-section and interview-count parity result
- Ask user:
  - `Verification passed. Review the one-pager quality. Proceed to completion?`
- Stop rule:
  - `Do not proceed until user explicitly confirms.`

## Acceptance Criteria Traceability (Directive -> Checks)

Use this section for directive workflows to map each directive acceptance criterion to concrete workflow checks.

| Directive Acceptance Criterion | Where Enforced in Workflow | Enforcement Mechanism |
|---|---|---|
| The deliverable is a concise one-page narrative suitable for rapid VC review. | Phase 3 (`verify-vc-pitch-output.py`) + Human Review Gate | Hard max word count check (`<=600`) and final reviewer approval. |
| It identifies clear opportunity areas grounded in participant evidence. | Phase 2 (`vc-pitch-writer`) + Human Review Gate | Writer prompt requires evidence-grounded opportunity framing; reviewer confirms adequacy. |
| It defines trust and user expectations in concrete, evidence-backed terms. | Phase 3 (`verify-vc-pitch-output.py`) + Human Review Gate | Required heading `## What "Trustworthy" Means` plus qualitative human check. |
| It articulates differentiated positioning versus existing AI assistants. | Phase 3 (`verify-vc-pitch-output.py`) + Human Review Gate | Required heading `## Our Positioning` plus qualitative human check. |
| It presents a coherent user-centered story linking pain, product value, and business opportunity. | Phase 3 (`verify-vc-pitch-output.py`) + Human Review Gate | Required section coverage plus human review for narrative coherence. |
| Core claims are evidence-grounded and traceable to participant patterns. | Phase 2 (`vc-pitch-writer`) + Human Review Gate | Writer instructions enforce participant-referenced evidence; reviewer validates traceability quality. |
| It directly answers why users would choose this assistant over alternatives. | Phase 3 (`verify-vc-pitch-output.py`) + Human Review Gate | Positioning section required and final user review confirms question is answered. |

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/generate-vc-pitch/prepare-vc-pitch-inputs.py` — validates prerequisites and writes synthesis manifest.
- `02-workflows/generate-vc-pitch/verify-vc-pitch-output.py` — validates word count, required sections, output existence, and interview-count parity.
- `vc-pitch-writer` sub-agent — generates the one-page VC pitch from extract evidence.

## Manifest Format

`04-process/04-generate-vc-pitch/manifest.json`:

- `workflow` — `generate-vc-pitch`
- `created_at` — UTC ISO timestamp
- `extracts_dir` — source extracts directory
- `brief_file` — strategic brief path
- `template_file` — output template path
- `output_file` — target one-pager path
- `files[]` — extract file paths (sorted)
- `summary.total_extracts` — number of extract files

## Sub-agent Parameters

`vc-pitch-writer`:

- `manifest_file` — `04-process/04-generate-vc-pitch/manifest.json`

## Output Promotion

- Process artifacts stay in `04-process/04-generate-vc-pitch/`.
- Final deliverables are copied/promoted to `05-outputs/04-generate-vc-pitch/`.
- Do not overwrite existing `05-outputs` deliverables without explicit user confirmation.

### Final Step: Copy Outputs

After the user confirms the final workflow phase is complete and satisfactory, copy final deliverables to `05-outputs/04-generate-vc-pitch/` and confirm files are present before reporting completion.

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Preconditions satisfied (or explicitly resolved)
- [ ] All directive acceptance criteria are mapped in traceability table
- [ ] All mapped checks reached required PASS/WARN state
- [ ] Final deliverable exists at `05-outputs/04-generate-vc-pitch/vc-pitch-one-pager.md`
- [ ] User-facing summary includes counts, issues, and final status
- [ ] Run log entry appended (if workflow logging is enabled)

## Learnings

**Footer bracket format (2026-03-03):** The verifier requires `Based on [N] interview transcripts` with the count in square brackets. The agent wrote `Based on 53 interview transcripts` (no brackets) on first run. Fixed by targeted retry. The agent's Step 5 instructions should explicitly note the `[N]` bracket format — consider adding it to the Writing Rules hard constraints.
