# Build Personas

> **Directive workflow** — triggered by user request. See `01-directives/build-personas.md` for goal, inputs, and acceptance criteria.

## Approach

Using the archetypes and participant extracts produced by the `synthesise-archetypes` workflow, write one fully-formed Dynamic Persona profile per archetype. Each persona is grounded in transcript evidence, follows the standard template, and the set as a whole meets diversity requirements.

## Prerequisites

The following outputs from `synthesise-archetypes` must exist before running this workflow:

- `04-process/synthesise-archetypes/archetypes.md`
- `04-process/synthesise-archetypes/extracts/*.md`
- `04-process/synthesise-archetypes/participant-archetype-assignments.csv`

## Process

### Phase 6: Create Personas from Archetypes

- Goal: Produce five persona files, one per archetype.
- Input:
  - `04-process/synthesise-archetypes/archetypes.md`
  - `04-process/synthesise-archetypes/extracts/*.md`
  - `10-resources/templates/persona-template.md`
  - `.claude/rules/persona-diversity-guidance.md`
- Sequence:
  1. Run `python3 02-workflows/build-personas/prepare-persona-inputs.py`.
  2. For each archetype input pack, run `persona-writer` sub-agent.
  3. Run `python3 02-workflows/build-personas/sync-persona-filenames.py`.
  4. Run `python3 02-workflows/build-personas/verify-personas.py`.
  5. Run `python3 02-workflows/build-personas/verify-persona-diversity.py`.
  6. Run `python3 02-workflows/build-personas/summarize-personas.py`.
  7. Run Phase 6 Human Review Gate summary and stop for user confirmation.
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
- If fail: Re-run the failed agent/script once with a specific correction instruction; if second fail, skip and log WARN

### Phase 6 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 6 completes, read:

- `04-process/build-personas/personas/`
- `04-process/build-personas/`

Present a summary:

```
Phase 6 complete — Persona Creation Summary
───────────────────────────────────────────
Persona files produced:   N/5
Structural validation:    PASS|FAIL
Diversity validation:     PASS|FAIL

Detailed results:
  04-process/build-personas/personas/
```

Then ask:

- **If validation passes:** "Phase 6 passed. Please review persona files. Ready to copy outputs and complete this workflow?"
- **If validation fails:** "Phase 6 has validation failures. Would you like to re-run persona generation with correction instructions?"

Do not proceed until the user explicitly says yes.

### Final Step: Copy Outputs

After the user confirms Phase 6 is complete and satisfactory, copy the final deliverables to `05-outputs/build-personas/`:

```bash
mkdir -p 05-outputs/build-personas/personas
cp 04-process/build-personas/personas/*.md 05-outputs/build-personas/personas/
```

Confirm files are present, then report workflow complete.

---

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
