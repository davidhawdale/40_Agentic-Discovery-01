# Synthesise Archetypes

> **Directive workflow** — triggered by user request. See `01-directives/synthesise-archetypes.md` for goal, inputs, and acceptance criteria.

## Approach

Read per-participant quote extracts produced by the `extract-and-tag-quotes` workflow and cluster all participants into exactly five named core archetypes. Each archetype captures a distinct pattern of attitudes and behaviours grounded in transcript evidence.

## Prerequisites

The following outputs from `extract-and-tag-quotes` must exist before running this workflow:

- `04-process/build-dynamic-personas/p0-prepare/manifest.json`
- `04-process/build-dynamic-personas/p4-consolidate-tags/consolidated-quotes.csv`

## Process

### Phase 5: Synthesize Archetypes

- Goal: Produce exactly five named core archetypes with participant assignments, plus optional outlier entries for weak-fit participants.
- Input:
  - `04-process/build-dynamic-personas/p4-consolidate-tags/consolidated-quotes.csv`
  - `04-process/build-dynamic-personas/p0-prepare/manifest.json`
- Sequence:
  1. Run `python3 02-workflows/synthesise-archetypes/prepare-archetype-extracts.py`.
  2. Run `archetype-writer` sub-agent.
  3. Run `python3 02-workflows/synthesise-archetypes/extract-archetype-assignments.py`.
  4. Run `python3 02-workflows/synthesise-archetypes/verify-archetype-assignments.py`.
  5. Run the Phase 5 Human Review Gate summary and stop for user confirmation.
- For archetype synthesis, spawn the `archetype-writer` sub-agent from:
  - `.claude/agents/archetype-writer/archetype-writer.md`
- Pass these values in the task prompt:
  - `extracts_folder` — `04-process/build-dynamic-personas/p5-synthesize-archetypes/extracts/`
  - `output_file` — `04-process/build-dynamic-personas/p5-synthesize-archetypes/archetypes.md`
  - `expected_participants` — from `04-process/build-dynamic-personas/p5-synthesize-archetypes/expected-participants.json`
- In Codex/OpenAI, "spawn sub-agent" means: read `.claude/agents/archetype-writer/archetype-writer.md` and execute those instructions inline.
- Output:
  - `04-process/build-dynamic-personas/p5-synthesize-archetypes/archetypes.md`
  - `04-process/build-dynamic-personas/p5-synthesize-archetypes/participant-archetype-assignments.csv`
- Constraints:
  - Exactly 5 core archetypes
  - Every expected participant appears exactly once across core archetypes and optional outliers
  - Evidence quotes must remain verbatim
- If fail: Re-run the failed agent/script once with a specific correction instruction; if second fail, skip and log WARN

### Phase 5 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 5 completes, read:

- `04-process/build-dynamic-personas/p5-synthesize-archetypes/archetypes.md`
- `04-process/build-dynamic-personas/p5-synthesize-archetypes/participant-archetype-assignments.csv`

Present a summary:

```
Phase 5 complete — Archetype Synthesis Summary
──────────────────────────────────────────────
Core archetypes produced:   5
Participants expected:      N
Participants assigned:      N
Outliers:                   N

Detailed results:
  04-process/build-dynamic-personas/p5-synthesize-archetypes/archetypes.md
  04-process/build-dynamic-personas/p5-synthesize-archetypes/participant-archetype-assignments.csv
```

Then ask:

- **If validation passes:** "Phase 5 passed. Please review archetypes and assignments. Ready to copy outputs and complete this workflow?"
- **If validation fails:** "Phase 5 has validation failures. Would you like to re-run archetype synthesis with correction instructions?"

Do not proceed until the user explicitly says yes.

### Final Step: Copy Outputs

After the user confirms Phase 5 is complete and satisfactory, copy the final deliverables to `05-outputs/synthesise-archetypes/`:

```bash
mkdir -p 05-outputs/synthesise-archetypes
cp 04-process/build-dynamic-personas/p5-synthesize-archetypes/archetypes.md 05-outputs/synthesise-archetypes/archetypes.md
cp 04-process/build-dynamic-personas/p5-synthesize-archetypes/participant-archetype-assignments.csv 05-outputs/synthesise-archetypes/participant-archetype-assignments.csv
```

Confirm files are present, then report workflow complete.

---

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
