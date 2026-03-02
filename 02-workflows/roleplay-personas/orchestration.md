# Roleplay Personas

> **Directive workflow** — triggered by user request. See `01-directives/roleplay-personas.md` for goal, inputs, and acceptance criteria.

## Approach

Using the persona files and evidence produced by `build-personas`, build a deterministic role-play pack that teams can use to run grounded five-persona panel discussions. Then launch a local FastAPI + HTMX app so teams can ask questions and receive in-character responses from all five personas simultaneously.

## Prerequisites

The following outputs from upstream workflows must exist before running this workflow:

- `04-process/build-dynamic-personas/p6-create-personas/persona-inputs/archetype-*.json` (from `build-personas`)
- `04-process/build-dynamic-personas/p6-create-personas/personas/*.md` (from `build-personas`)
- `04-process/build-dynamic-personas/p4-consolidate-tags/consolidated-quotes.csv` (from `extract-and-tag-quotes`)
- `04-process/build-dynamic-personas/p3-check-contradictions/contradictions.csv` (from `extract-and-tag-quotes`)
- `00-brief/product-vision.md`
- `03-inputs/research-brief.md`

## Process

### Phase 7: Persona Role Play and Discussion

- Goal: Build deterministic role-play assets so teams can run grounded persona-panel discussions about the proposed app.
- Sequence:
  1. Run `python3 02-workflows/roleplay-personas/prepare-roleplay-pack.py`.
  2. Run `python3 02-workflows/roleplay-personas/verify-roleplay-pack.py`.
  3. Optional smoke test: `python3 02-workflows/roleplay-personas/run-roleplay-session.py --question "What should the first MVP focus on?"`
  4. If smoke output exists, run `python3 02-workflows/roleplay-personas/verify-roleplay-response.py --file <smoke-output-path>`.
  5. Run Phase 7 Human Review Gate summary and stop for user confirmation.
- Inputs:
  - `04-process/build-dynamic-personas/p6-create-personas/persona-inputs/archetype-*.json`
  - `04-process/build-dynamic-personas/p6-create-personas/personas/*.md`
  - `04-process/build-dynamic-personas/p4-consolidate-tags/consolidated-quotes.csv`
  - `04-process/build-dynamic-personas/p3-check-contradictions/contradictions.csv`
  - `00-brief/product-vision.md`
  - `03-inputs/research-brief.md`
- Outputs:
  - `04-process/build-dynamic-personas/p7-role-play/session-pack.json`
  - `04-process/build-dynamic-personas/p7-role-play/panel-system-prompt.md`
  - `04-process/build-dynamic-personas/p7-role-play/session-runbook.md`
  - `04-process/build-dynamic-personas/p7-role-play/question-template.md`
  - Optional smoke output in `04-process/build-dynamic-personas/p8-roleplay-app/sessions/*.md`
- Constraints:
  - Session pack must include exactly 5 personas.
  - Persona evidence refs must be present and non-empty.
  - Contradictions field must exist for each persona (empty list allowed).
  - Response schema must match verifier contract before any result is treated as valid.
- If fail: Re-run the failed script once with specific correction instructions; if second fail, stop and report FAIL.

### Phase 7 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 7 completes, read:

- `04-process/build-dynamic-personas/p7-role-play/session-pack.json`
- `04-process/build-dynamic-personas/p7-role-play/panel-system-prompt.md`
- Optional smoke output in `04-process/build-dynamic-personas/p8-roleplay-app/sessions/`

Present a summary:

```
Phase 7 complete — Role-Play Pack Summary
─────────────────────────────────────────
Session pack created:       YES|NO
Personas in pack:           N/5
Pack verification:          PASS|FAIL
Smoke response check:       PASS|FAIL|SKIPPED

Detailed results:
  04-process/build-dynamic-personas/p7-role-play/session-pack.json
  04-process/build-dynamic-personas/p7-role-play/panel-system-prompt.md
```

Then ask:

- **If validation passes:** "Phase 7 passed. Please review the role-play pack. Ready to continue to the app phase?"
- **If validation fails:** "Phase 7 has validation failures. Would you like to re-run pack generation with correction instructions?"

Do not proceed to the next phase until the user explicitly says yes.

### Phase 8: Run Persona Role-Play App

- Goal: Run a local FastAPI + HTMX app that executes grounded five-persona panel responses with moderator synthesis.
- Sequence:
  1. Verify Phase 7 assets: `python3 02-workflows/roleplay-personas/verify-roleplay-pack.py`
  2. Start app: `python3 02-workflows/roleplay-personas/run-roleplay-app.py`
  3. Optional API smoke test:
     - Create session: `POST /api/session`
     - Ask one question: `POST /api/session/{session_id}/ask`
  4. If smoke output is captured to file, run `python3 02-workflows/roleplay-personas/verify-roleplay-response.py --file <response-file>`
  5. Run Phase 8 Human Review Gate summary and stop for user confirmation.
- Runtime:
  - App URL default: `http://127.0.0.1:8016`
  - Required env var for live answers: `OPENAI_API_KEY`
  - Optional model override: `OPENAI_MODEL` (default `gpt-4o`)
- App outputs:
  - `04-process/build-dynamic-personas/p8-roleplay-app/app-config.json`
  - `04-process/build-dynamic-personas/p8-roleplay-app/latest-session.json`
  - `04-process/build-dynamic-personas/p8-roleplay-app/sessions/*.json`
  - `04-process/build-dynamic-personas/p8-roleplay-app/logs/app.log`
- Hard validation behavior:
  - Every model response is checked with `verify-roleplay-response` rules.
  - One targeted retry is allowed on verifier failure.
  - If second fail, reject turn and log `VERIFICATION_FAIL`.
- Error categories:
  - `VERIFICATION_FAIL`
  - `OPENAI_CALL_FAIL`
  - `PACK_MISSING_OR_INVALID`
  - `PARSING_FAIL`

### Phase 8 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 8 completes, read:

- `04-process/build-dynamic-personas/p8-roleplay-app/app-config.json`
- `04-process/build-dynamic-personas/p8-roleplay-app/sessions/`
- `04-process/build-dynamic-personas/p8-roleplay-app/logs/app.log`

Present a summary:

```
Phase 8 complete — Role-Play App Summary
────────────────────────────────────────
App startup status:          PASS|FAIL
Session pack status:         PASS|FAIL
Smoke turn verification:     PASS|FAIL|SKIPPED
Session artifact path:       04-process/build-dynamic-personas/p8-roleplay-app/sessions/
```

Then ask:

- **If validation passes:** "Phase 8 passed. Please review app outputs and session artifacts. Ready to copy outputs and complete this workflow?"
- **If validation fails:** "Phase 8 has validation failures. Would you like to re-run with correction instructions?"

Do not proceed until the user explicitly says yes.

### Final Step: Copy Outputs

After the user confirms Phase 8 is complete and satisfactory, copy the final deliverables to `05-outputs/persona-roleplay/`:

```bash
mkdir -p 05-outputs/roleplay-personas
cp 04-process/build-dynamic-personas/p7-role-play/session-pack.json 05-outputs/roleplay-personas/session-pack.json
cp 04-process/build-dynamic-personas/p7-role-play/session-runbook.md 05-outputs/roleplay-personas/session-runbook.md
```

Confirm files are present, then report workflow complete.

---

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
