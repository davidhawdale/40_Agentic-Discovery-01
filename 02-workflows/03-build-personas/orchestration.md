# Build Personas

> **Directive workflow** — triggered by user request. See `01-directives/build-personas.md` for goal, inputs, and acceptance criteria.

## Approach

Using the archetypes and participant extracts produced by the `synthesise-archetypes` workflow, write one fully-formed Dynamic Persona profile per archetype. Each persona is grounded in transcript evidence, follows the standard template, and the set as a whole meets diversity requirements.

## Preconditions

- Required inputs:
  - `04-process/synthesise-archetypes/archetypes.md`
  - `04-process/synthesise-archetypes/extracts/*.md`
  - `04-process/synthesise-archetypes/participant-archetype-assignments.csv`
- Expected counts/shape:
  - 5 archetypes expected in `archetypes.md`
  - participant assignments present in `participant-archetype-assignments.csv`
- Stop conditions:
  - Missing required inputs
  - Missing archetype definitions or participant assignments

## Process

### Phase 1: Create Personas from Archetypes

- Goal: Produce five persona files, one per archetype.
- Run:
  1. `python3 02-workflows/build-personas/prepare-persona-inputs.py`
  2. `persona-writer` sub-agent for each archetype input pack (run all in parallel)
  3. `python3 02-workflows/build-personas/sync-persona-filenames.py`
  4. `python3 02-workflows/build-personas/verify-personas.py`
  5. `python3 02-workflows/build-personas/verify-persona-diversity.py`
  6. `python3 02-workflows/build-personas/summarize-personas.py`
- Input:
  - `04-process/synthesise-archetypes/archetypes.md`
  - `04-process/synthesise-archetypes/extracts/*.md`
  - `10-resources/templates/persona-template.md`
  - `.claude/rules/persona-diversity-guidance.md`
- For persona writing, spawn the `persona-writer` sub-agent from:
  - `.claude/agents/persona-writer/persona-writer.md`
- In Codex/OpenAI, "spawn sub-agent" means: read `.claude/agents/persona-writer/persona-writer.md` and execute those instructions inline.
- Output:
  - `04-process/build-personas/personas/*.md` (filename = slugified persona H1)
- Constraints:
  - Keep quote evidence verbatim
  - Include exactly 2 quotes in each persona `## Key Quotes` section
  - Persona markdown filename must be the slugified H1 persona name (for example, `# Maya Patel` -> `maya-patel.md`)
  - Enforce set-level diversity using `.claude/rules/persona-diversity-guidance.md`
  - Write personas to `04-process/` first; do not write to `05-outputs/` in this phase
- PASS when:
  - `verify-personas.py` passes
  - `verify-persona-diversity.py` passes
  - `04-process/build-personas/personas/` contains 5 persona files
- WARN when:
  - Non-blocking validation concerns are identified and logged for human review
- FAIL when:
  - Required verification script fails
  - Persona count is not 5 after retry
  - Any blocking structural schema requirement fails
- If fail:
  - Apply retry policy below with specific correction instructions

### Phase 1 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 1 completes, read:

- `04-process/build-personas/personas/`
- `04-process/build-personas/`

Present a summary:

```
Phase 1 complete — Persona Creation Summary
───────────────────────────────────────────
Persona files produced:   N/5
Structural validation:    PASS|FAIL
Diversity validation:     PASS|FAIL

Detailed results:
  04-process/build-personas/personas/
```

Then ask:

- **If validation passes:** "Phase 1 passed. Please review persona files. Ready to copy outputs and complete this workflow?"
- **If validation fails:** "Phase 1 has validation failures. Would you like to re-run persona generation with correction instructions?"

Do not proceed until user explicitly confirms.

## Acceptance Criteria Traceability (Directive -> Checks)

Use this section for directive workflows to map each directive acceptance criterion to concrete workflow checks.

| Directive Acceptance Criterion | Where Enforced in Workflow | Enforcement Mechanism |
|---|---|---|
| Five persona profiles are produced, one per archetype. | Phase 1 (`verify-personas.py`) | Verifies persona structure and count, including expected persona files. |
| Each persona is clearly grounded in source evidence and reflects its assigned archetype. | Phase 1 (`verify-personas.py`) + Phase 1 Human Review Gate | Structural verification plus reviewer spot-check of evidence grounding and archetype fidelity. |
| The persona set is diverse enough to represent materially different user profiles and needs. | Phase 1 (`verify-persona-diversity.py`) | Applies set-level diversity validation against project diversity guidance. |
| Outputs are suitable for downstream product discussion and decision-making. | Phase 1 (`summarize-personas.py`) + Phase 1 Human Review Gate | Summarized outputs and human review confirm readability and practical discussion utility. |
| The deliverables are saved to the expected final output location for this workflow. | Final Step: Copy Outputs | Copies persona files to `05-outputs/03-build-personas/personas/` and confirms file presence. |

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/build-personas/prepare-persona-inputs.py` — prepares per-archetype input packs for persona generation.
- `persona-writer` sub-agent (`.claude/agents/persona-writer/persona-writer.md`) — writes one persona per archetype input pack.
- `02-workflows/build-personas/sync-persona-filenames.py` — enforces filename conventions from persona H1 titles.
- `02-workflows/build-personas/verify-personas.py` — validates structure, count, and required persona content.
- `02-workflows/build-personas/verify-persona-diversity.py` — validates set-level diversity coverage.
- `02-workflows/build-personas/summarize-personas.py` — produces summary context for human review.

## Manifest Format

No workflow manifest used.

## Sub-agent Parameters

### `persona-writer`

- `input_pack_path` — each file in `04-process/build-personas/persona-inputs/`
- `output_path` — `04-process/build-personas/personas/{persona-name-slug}.md`

## Output Promotion

- Process artifacts stay in `04-process/build-personas/`, including `04-process/build-personas/personas/*.md`.
- Final deliverables are copied to `05-outputs/03-build-personas/personas/*.md`.
- Do not overwrite existing `05-outputs/03-build-personas/` deliverables without explicit user confirmation.

### Final Step: Copy Outputs

After the user confirms Phase 1 is complete and satisfactory, copy the final deliverables to `05-outputs/03-build-personas/`:

```bash
mkdir -p 05-outputs/03-build-personas/personas
cp 04-process/build-personas/personas/*.md 05-outputs/03-build-personas/personas/
```

Confirm files are present, then report workflow complete.

---

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Preconditions satisfied (or explicitly resolved)
- [ ] All directive acceptance criteria are mapped in traceability table
- [ ] All mapped checks reached required PASS/WARN state
- [ ] Final deliverables exist at expected `05-outputs/03-build-personas/` paths
- [ ] User-facing summary includes counts, issues, and final status
- [ ] Run log entry appended (if workflow logging is enabled)

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
