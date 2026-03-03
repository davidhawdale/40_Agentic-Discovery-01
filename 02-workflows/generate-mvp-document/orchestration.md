# Generate MVP Document

> **Directive workflow** — triggered by user request. See `01-directives/generate-mvp-document.md` for goal, inputs, and acceptance criteria.

## Approach

Run four specialist agents in two parallel phases to produce structured sections, then synthesise into a single MVP brief using a dedicated writer agent, followed by deterministic verification.

## Preconditions

- Required inputs:
  - `05-outputs/generate-vc-pitch/vc-pitch-one-pager.md`
  - `05-outputs/synthesise-archetypes/archetypes.md`
  - `05-outputs/build-personas/personas/*.md` (at least one file)
  - `00-brief/strategic-research-brief.md`
  - `10-resources/templates/mvp-brief-template.md`
- Stop conditions:
  - Any required input missing
  - Personas directory empty

## Process

### Phase 1: Prepare Inputs

- Goal: Validate prerequisites and write the manifest.
- Run:
  1. `python3 02-workflows/generate-mvp-document/prepare-mvp-inputs.py`
- Output:
  - `04-process/generate-mvp-document/manifest.json`
- PASS when:
  - Manifest written, all inputs validated
- FAIL when:
  - Script exits non-zero or manifest not written
- If fail:
  - Identify the missing input, resolve it, rerun once

### Phase 2: Specialist Agents (run in parallel)

- Goal: Produce three independent sections concurrently.
- Run simultaneously:
  1. `market-reviewer` → `04-process/generate-mvp-document/market-review.md`
  2. `ux-architect` → `04-process/generate-mvp-document/target-user.md`
  3. `staff-engineer` → `04-process/generate-mvp-document/risks-constraints.md`
- Input for all three:
  - `04-process/generate-mvp-document/manifest.json`
- PASS when:
  - All three output files exist and are non-empty
- FAIL when:
  - Any output file missing or empty
- If fail:
  - Re-run the failed agent once with a specific correction instruction

### Phase 3: Business Opportunity Agent

- Goal: Assess revenue opportunity, using the market review from Phase 2.
- Run:
  1. `business-opportunity` → `04-process/generate-mvp-document/business-opportunity.md`
- Input:
  - `04-process/generate-mvp-document/manifest.json`
  - Reads `market-review.md` internally (path from manifest)
- PASS when:
  - Output file exists and is non-empty
- FAIL when:
  - Output missing or empty, or market-review.md not yet present
- If fail:
  - Confirm Phase 2 completed first; re-run once with correction

### Phase 4: Synthesise MVP Brief

- Goal: Assemble all sections into the final document.
- Run:
  1. `mvp-writer` → `05-outputs/generate-mvp-document/mvp-brief.md`
- Input:
  - `04-process/generate-mvp-document/manifest.json`
  - Reads all four section files and the template internally
- PASS when:
  - Output file exists and is non-empty
- FAIL when:
  - Output missing or empty
- If fail:
  - Re-run once with specific correction (e.g. "word count exceeded — cut from Market Review first")

### Phase 5: Verify Output

- Goal: Deterministically verify structural and constraint compliance.
- Run:
  1. `python3 02-workflows/generate-mvp-document/verify-mvp-output.py --file 05-outputs/generate-mvp-document/mvp-brief.md --max-words 2500`
- PASS when:
  - All 7 headings present, word count ≤ 2500, footer present
- FAIL when:
  - Verifier returns FAIL
- If fail:
  - Re-run Phase 4 once with the specific failure as a correction instruction, then re-verify

### Human Review Gate

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger: Phase 5 returns PASS
- Summarise:
  - Word count
  - Experiments selected (names)
  - Any thin sections or gaps flagged by agents
- Ask user:
  - `Verification passed. Review the MVP brief quality. Proceed to completion?`

## Acceptance Criteria Traceability (Directive → Checks)

| Directive Acceptance Criterion | Where Enforced | Mechanism |
|---|---|---|
| Problem statement grounded in participant evidence | Phase 4 (`mvp-writer`) + Human Gate | Writer reads VC pitch; reviewer confirms quotes present |
| Scope defined (in and out) | Phase 2 (`ux-architect`) + Phase 5 | Required heading `## Scope`; human review for specificity |
| Primary target user identified | Phase 2 (`ux-architect`) + Phase 5 | Required heading `## Target User`; human review for evidence grounding |
| 1–3 experiments with learning goals and signals | Phase 4 (`mvp-writer`) + Phase 5 | Required heading `## Experiments`; writer selects from 3 agent proposals |
| Risks and constraints listed | Phase 2 (`staff-engineer`) + Phase 5 | Required heading `## Risks and Constraints` |
| Market review with competitor pricing, size, gaps | Phase 2 (`market-reviewer`) + Phase 5 | Required heading `## Market Review` |
| Opportunity statement with revenue model and estimate | Phase 3 (`business-opportunity`) + Phase 5 | Required heading `## Opportunity Statement` |

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/generate-mvp-document/prepare-mvp-inputs.py` — validates prerequisites, writes manifest
- `02-workflows/generate-mvp-document/verify-mvp-output.py` — validates headings, word count, footer
- `market-reviewer` — market research and competitor analysis section
- `ux-architect` — target user, scope, and user validation experiment
- `staff-engineer` — technical risks, constraints, and technical experiment
- `business-opportunity` — opportunity statement, pricing, revenue estimate, pricing experiment
- `mvp-writer` — synthesis agent; assembles final MVP brief

## Manifest Format

`04-process/generate-mvp-document/manifest.json`:

- `workflow` — `generate-mvp-document`
- `created_at` — UTC ISO timestamp
- `vc_pitch_file` — VC pitch one-pager path
- `archetypes_file` — archetypes output path
- `personas_dir` — personas directory path
- `brief_file` — strategic research brief path
- `template_file` — MVP brief template path
- `output_file` — final output path
- `market_review_file` — market-reviewer section output
- `target_user_file` — ux-architect section output
- `risks_file` — staff-engineer section output
- `opportunity_file` — business-opportunity section output

## Sub-agent Parameters

All agents receive:
- `manifest_file` — `04-process/generate-mvp-document/manifest.json`

## Output Promotion

- Section files stay in `04-process/generate-mvp-document/`.
- Final deliverable is written directly to `05-outputs/generate-mvp-document/mvp-brief.md`.
- Do not overwrite an existing `05-outputs` deliverable without explicit user confirmation.

## Completion Checklist

- [ ] Preconditions satisfied
- [ ] All directive acceptance criteria mapped in traceability table
- [ ] All mapped checks reached PASS/WARN state
- [ ] Final deliverable exists at `05-outputs/generate-mvp-document/mvp-brief.md`
- [ ] User-facing summary includes word count, experiments selected, and final status
- [ ] Run log entry appended

## Learnings

_Update this section as the workflow is used. Record constraints, edge cases, and improved checks._
