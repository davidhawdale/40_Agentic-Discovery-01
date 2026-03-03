# Roleplay Personas

> **Directive workflow** — triggered by user request. See `01-directives/roleplay-personas.md` for goal, inputs, and acceptance criteria.

## Approach

Using persona files and evidence from upstream workflows, build a deterministic role-play pack for grounded five-persona panel discussions, then run a local FastAPI + HTMX app for interactive persona questioning.

## Preconditions

- Required inputs:
  - `04-process/build-personas/persona-inputs/archetype-*.json`
  - `04-process/build-personas/personas/*.md`
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv`
  - `04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv`
  - `00-brief/product-vision.md`
  - `03-inputs/research-brief.md`
- Expected counts/shape:
  - Exactly 5 persona markdown files expected for panel generation
  - Phase 7 pack outputs must include `session-pack.json`, `panel-system-prompt.md`, and `session-runbook.md`
- Stop conditions:
  - Missing upstream artifacts required for pack generation
  - Missing required env var `OPENAI_API_KEY` when live app phase is requested

## Process

### Phase 7: Persona Role Play and Discussion

- Goal: Build deterministic role-play assets so teams can run grounded persona-panel discussions.
- Run:
  1. `python3 02-workflows/roleplay-personas/prepare-roleplay-pack.py`
  2. `python3 02-workflows/roleplay-personas/verify-roleplay-pack.py`
  3. Optional smoke test: `python3 02-workflows/roleplay-personas/run-roleplay-session.py --question "What should the first MVP focus on?"`
  4. If smoke output exists: `python3 02-workflows/roleplay-personas/verify-roleplay-response.py --file <smoke-output-path>`
- Input:
  - `04-process/build-personas/persona-inputs/archetype-*.json`
  - `04-process/build-personas/personas/*.md`
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv`
  - `04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv`
  - `00-brief/product-vision.md`
  - `03-inputs/research-brief.md`
- Output:
  - `04-process/roleplay-personas/roleplay/session-pack.json`
  - `04-process/roleplay-personas/roleplay/panel-system-prompt.md`
  - `04-process/roleplay-personas/roleplay/session-runbook.md`
  - `04-process/roleplay-personas/roleplay/question-template.md`
  - Optional smoke output in `04-process/roleplay-personas/roleplay-app/sessions/*.md`
- Constraints:
  - Session pack must include exactly 5 personas
  - Persona evidence refs must be present and non-empty
  - Contradictions field must exist for each persona (empty list allowed)
  - Response schema must match verifier contract before any result is treated as valid
- PASS when:
  - `verify-roleplay-pack.py` passes
  - `session-pack.json` is present with 5 personas
- WARN when:
  - Optional smoke test is skipped
  - Non-blocking quality notes are logged for review
- FAIL when:
  - Pack generation or verification fails
  - Required pack artifacts are missing
- If fail:
  - Apply retry policy with specific correction instructions

### Phase 7 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger:
  - Phase 7 completes and pack artifacts are generated
- Read:
  - `04-process/roleplay-personas/roleplay/session-pack.json`
  - `04-process/roleplay-personas/roleplay/panel-system-prompt.md`
  - Optional smoke output in `04-process/roleplay-personas/roleplay-app/sessions/`
- Summarise:
  - Session pack created (YES/NO)
  - Personas in pack (`N/5`)
  - Pack verification status (`PASS/FAIL`)
  - Smoke response check (`PASS/FAIL/SKIPPED`)
- Ask user:
  - If validation passes: "Phase 7 passed. Please review the role-play pack. Ready to continue to the app phase?"
  - If validation fails: "Phase 7 has validation failures. Would you like to re-run pack generation with correction instructions?"
- Stop rule:
  - Do not proceed until user explicitly confirms.

### Phase 8: Run Persona Role-Play App

- Goal: Run a local FastAPI + HTMX app that executes grounded five-persona panel responses with moderator synthesis.
- Run:
  1. `python3 02-workflows/roleplay-personas/verify-roleplay-pack.py`
  2. `python3 02-workflows/roleplay-personas/run-roleplay-app.py`
  3. Optional API smoke test:
     - `POST /api/session`
     - `POST /api/session/{session_id}/ask`
  4. If smoke output is captured to file: `python3 02-workflows/roleplay-personas/verify-roleplay-response.py --file <response-file>`
- Input:
  - `04-process/roleplay-personas/roleplay/session-pack.json`
  - `04-process/roleplay-personas/roleplay/panel-system-prompt.md`
  - Runtime env: `OPENAI_API_KEY` (required for live answers), `OPENAI_MODEL` (optional, default `gpt-4o`)
- Output:
  - `04-process/roleplay-personas/roleplay-app/app-config.json`
  - `04-process/roleplay-personas/roleplay-app/latest-session.json`
  - `04-process/roleplay-personas/roleplay-app/sessions/*.json`
  - `04-process/roleplay-personas/roleplay-app/logs/app.log`
- Constraints:
  - App URL default: `http://127.0.0.1:8016`
  - Every model response is checked with `verify-roleplay-response` rules
  - One targeted retry is allowed on verifier failure; second fail rejects turn and logs `VERIFICATION_FAIL`
  - Error categories: `VERIFICATION_FAIL`, `OPENAI_CALL_FAIL`, `PACK_MISSING_OR_INVALID`, `PARSING_FAIL`
- PASS when:
  - App starts successfully with valid pack
  - Smoke turn verification passes (or smoke test is intentionally skipped)
- WARN when:
  - Smoke test is skipped
  - Recoverable runtime errors occur but app remains operational
- FAIL when:
  - App startup fails
  - Pack invalid/missing at runtime
  - Response verification fails without recovery
- If fail:
  - Apply retry policy with specific correction instructions

### Phase 8 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger:
  - Phase 8 completes and app/session artifacts are available
- Read:
  - `04-process/roleplay-personas/roleplay-app/app-config.json`
  - `04-process/roleplay-personas/roleplay-app/sessions/`
  - `04-process/roleplay-personas/roleplay-app/logs/app.log`
- Summarise:
  - App startup status (`PASS/FAIL`)
  - Session pack status (`PASS/FAIL`)
  - Smoke turn verification (`PASS/FAIL/SKIPPED`)
  - Session artifact path
- Ask user:
  - If validation passes: "Phase 8 passed. Please review app outputs and session artifacts. Ready to copy outputs and complete this workflow?"
  - If validation fails: "Phase 8 has validation failures. Would you like to re-run with correction instructions?"
- Stop rule:
  - Do not proceed until user explicitly confirms.

## Acceptance Criteria Traceability (Directive -> Checks)

Use this section for directive workflows to map each directive acceptance criterion to concrete workflow checks.

| Directive Acceptance Criterion | Where Enforced in Workflow | Enforcement Mechanism |
|---|---|---|
| A complete session pack is produced for the five-persona panel. | Phase 7 (`verify-roleplay-pack.py`) | Verifies pack artifacts and persona count (`5`). |
| Persona responses are grounded in the underlying research evidence base. | Phase 7/8 (`verify-roleplay-pack.py` + `verify-roleplay-response.py`) + Human Review Gates | Enforces evidence references in pack and validates response schema/grounding expectations before acceptance. |
| Persona voices are meaningfully differentiated and suitable for panel-style discussion. | Phase 7 optional smoke + Phase 8 smoke (`verify-roleplay-response.py`) + Human Review Gates | Checks response validity and supports reviewer assessment of differentiated persona behavior. |
| The runbook provides clear guidance for teams to run repeatable role-play sessions. | Phase 7 outputs + Phase 7 Human Review Gate | Confirms `session-runbook.md` is produced and reviewed as usable guidance. |
| Outputs are usable for downstream concept evaluation and product conversation. | Phase 8 Human Review Gate + Final Step: Copy Outputs | Confirms operational artifacts and final output promotion to `05-outputs/roleplay-personas/`. |

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/roleplay-personas/prepare-roleplay-pack.py` — builds deterministic role-play pack artifacts.
- `02-workflows/roleplay-personas/verify-roleplay-pack.py` — validates session pack structure and required fields.
- `02-workflows/roleplay-personas/run-roleplay-session.py` — runs optional smoke panel turn for pack-level validation.
- `02-workflows/roleplay-personas/verify-roleplay-response.py` — validates response schema/contract for smoke or app outputs.
- `02-workflows/roleplay-personas/run-roleplay-app.py` — starts local FastAPI + HTMX role-play application.

## Manifest Format

No workflow manifest; Phase 7 outputs act as runtime contract for Phase 8.

## Sub-agent Parameters

No dedicated sub-agent calls in this workflow.

## Output Promotion

- Process artifacts remain under:
  - `04-process/roleplay-personas/roleplay/`
  - `04-process/roleplay-personas/roleplay-app/`
- Final deliverables are promoted to:
  - `05-outputs/roleplay-personas/session-pack.json`
  - `05-outputs/roleplay-personas/session-runbook.md`
- Do not overwrite existing `05-outputs/roleplay-personas/` deliverables without explicit user confirmation.

### Final Step: Copy Outputs

After the user confirms Phase 8 is complete and satisfactory, copy the final deliverables to `05-outputs/roleplay-personas/`:

```bash
mkdir -p 05-outputs/roleplay-personas
cp 04-process/roleplay-personas/roleplay/session-pack.json 05-outputs/roleplay-personas/session-pack.json
cp 04-process/roleplay-personas/roleplay/session-runbook.md 05-outputs/roleplay-personas/session-runbook.md
```

Confirm files are present, then report workflow complete.

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Preconditions satisfied (or explicitly resolved)
- [ ] All directive acceptance criteria are mapped in traceability table
- [ ] All mapped checks reached required PASS/WARN state
- [ ] Final deliverables exist at expected `05-outputs/roleplay-personas/` paths
- [ ] User-facing summary includes counts, issues, and final status
- [ ] Run log entry appended (if workflow logging is enabled)

---

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
