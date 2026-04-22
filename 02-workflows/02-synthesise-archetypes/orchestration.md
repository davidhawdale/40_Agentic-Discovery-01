# Synthesise Archetypes

> **Directive workflow** — triggered by user request. See `01-directives/synthesise-archetypes.md` for goal, inputs, and acceptance criteria.

## Approach

Read consolidated participant quote evidence from `extract-and-tag-quotes` and synthesize exactly five named core archetypes. Each archetype should represent a distinct behavioral pattern grounded in verbatim participant evidence and suitable for downstream persona creation.

## Preconditions

- Required inputs:
  - `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv`
- Expected counts/shape:
  - Manifest includes expected participant list and transcript metadata
  - Consolidated quotes include rows for all expected participants
- Stop conditions:
  - Missing manifest or consolidated quotes file
  - `prepare-archetype-extracts.py` fails to generate participant extracts
  - `prepare-archetype-extracts.py` fails to generate `expected-participants.json`

## Process

### Phase 1: Synthesize Archetypes

- Goal: Produce exactly five named core archetypes with participant assignments, plus optional outlier entries for weak-fit participants.
- Run:
  1. `python3 02-workflows/synthesise-archetypes/prepare-archetype-extracts.py`
  2. Run `archetype-writer` sub-agent
  3. `python3 02-workflows/synthesise-archetypes/extract-archetype-assignments.py`
  4. `python3 02-workflows/synthesise-archetypes/verify-archetype-assignments.py`
- Input:
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv`
  - `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
- Output:
  - `04-process/synthesise-archetypes/extracts/*.md`
  - `04-process/synthesise-archetypes/expected-participants.json`
  - `04-process/synthesise-archetypes/archetypes.md`
  - `04-process/synthesise-archetypes/participant-archetype-assignments.csv`
- Constraints:
  - Exactly 5 core archetypes
  - Every expected participant appears exactly once across core archetypes and optional outliers
  - Evidence quotes must remain verbatim
- PASS when:
  - `verify-archetype-assignments.py` passes
  - `archetypes.md` contains 5 core archetypes
  - Assignments CSV covers all expected participants exactly once
  - Outlier count is no more than 2 in cohorts of approximately 50 participants
- WARN when:
  - Non-blocking quality concerns are logged for review
- FAIL when:
  - Any required phase script fails
  - Verification fails for coverage, schema, or structural constraints
- If fail:
  - Apply retry policy with specific correction instructions

### Phase 1 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger:
  - Phase 1 completes and archetype/assignment outputs are generated
- Read:
  - `04-process/synthesise-archetypes/archetypes.md`
  - `04-process/synthesise-archetypes/participant-archetype-assignments.csv`
- Summarise:
  - Core archetypes produced
  - Participants expected vs assigned
  - Outlier count
- Ask user:
  - If validation passes: "Phase 1 passed. Please review archetypes and assignments. Ready to copy outputs and complete this workflow?"
  - If validation fails: "Phase 1 has validation failures. Would you like to re-run archetype synthesis with correction instructions?"
- Stop rule:
  - Do not proceed until user explicitly confirms.

## Acceptance Criteria Traceability (Directive -> Checks)

Use this section for directive workflows to map each directive acceptance criterion to concrete workflow checks.

| Directive Acceptance Criterion | Where Enforced in Workflow | Enforcement Mechanism |
|---|---|---|
| Exactly five core archetypes are produced. | Phase 1 (`verify-archetype-assignments.py`) + Phase 1 Human Review Gate | Verifies core archetype structure/numbering and confirms 5 core archetypes in review summary. |
| Every participant is assigned exactly once (to a core archetype or outlier). | Phase 1 (`verify-archetype-assignments.py`) | Validates assignment coverage, uniqueness, and expected-vs-assigned parity. |
| Outlier cap: no more than 2 outliers in a cohort of approximately 50 participants. | Phase 1 Human Review Gate | Outlier count is summarized and checked before approval to promote outputs. |
| Each archetype includes three verbatim evidence quotes from three different participants in that archetype. | Phase 1 (`verify-archetype-assignments.py`) | Validates quote count per archetype, distinct quote participants, and participant membership consistency. |
| Archetype names and descriptions are clearly differentiated and interpretable by downstream teams. | Phase 1 Human Review Gate | Reviewer confirms naming clarity and differentiation quality before final approval. |
| Outputs are usable as the direct foundation for the `build-personas` workflow. | Final Step: Copy Outputs | Promotes archetype artifacts to `05-outputs/synthesise-archetypes/` for downstream workflow consumption. |

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/synthesise-archetypes/prepare-archetype-extracts.py` — generates per-participant extracts and expected participant IDs.
- `archetype-writer` sub-agent (`.claude/agents/archetype-writer/archetype-writer.md`) — synthesizes archetypes from prepared extracts.
- `02-workflows/synthesise-archetypes/extract-archetype-assignments.py` — extracts assignment rows from archetypes output.
- `02-workflows/synthesise-archetypes/verify-archetype-assignments.py` — verifies archetype structure, quote evidence constraints, and assignment integrity.

## Manifest Format

Primary consumed manifest:
- `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
  - `transcript_count`
  - `transcripts[]` including `id`, `participant_id`, `path`, `language`, `source_language`, `translated`, `size_bytes`

Phase-local expected-participant contract:
- `04-process/synthesise-archetypes/expected-participants.json`
  - `expected_participants` (array of participant IDs)

## Sub-agent Parameters

### `archetype-writer`

- `extracts_folder` — `04-process/synthesise-archetypes/extracts/`
- `output_file` — `04-process/synthesise-archetypes/archetypes.md`
- `expected_participants` — from `04-process/synthesise-archetypes/expected-participants.json`

## Output Promotion

- Process artifacts remain in `04-process/synthesise-archetypes/`.
- Final deliverables are promoted to `05-outputs/synthesise-archetypes/`.
- Do not overwrite existing `05-outputs/synthesise-archetypes/` files without explicit user confirmation.

### Final Step: Copy Outputs

After the user confirms Phase 1 is complete and satisfactory, copy the final deliverables to `05-outputs/synthesise-archetypes/`:

```bash
mkdir -p 05-outputs/synthesise-archetypes
cp 04-process/synthesise-archetypes/archetypes.md 05-outputs/synthesise-archetypes/archetypes.md
cp 04-process/synthesise-archetypes/participant-archetype-assignments.csv 05-outputs/synthesise-archetypes/participant-archetype-assignments.csv
```

Confirm files are present, then report workflow complete.

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Preconditions satisfied (or explicitly resolved)
- [ ] All directive acceptance criteria are mapped in traceability table
- [ ] All mapped checks reached required PASS/WARN state
- [ ] Final deliverables exist at expected `05-outputs/synthesise-archetypes/` paths
- [ ] User-facing summary includes counts, issues, and final status
- [ ] Run log entry appended (if enabled)

---

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
