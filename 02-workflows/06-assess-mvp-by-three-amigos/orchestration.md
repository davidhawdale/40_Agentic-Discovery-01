# Assess MVP by Three Amigos

> **Directive workflow** — triggered by user request. See `01-directives/06-assess-mvp-by-three-amigos.md` for goal, inputs, and acceptance criteria.

## Approach

Create a Claude Code team of three specialist reviewers. Each independently assesses the MVP brief through their own lens (Desirability, Feasibility, Viability). The orchestrator then facilitates a live discussion round — broadcasting all three reviews and recording every SendMessage response into a discussion transcript. A synthesiser agent assembles the final assessment from all reviews and the transcript.

## Preconditions

- Required inputs:
  - `05-outputs/04-generate-mvp-document/mvp-brief.md`
  - `00-brief/strategic-research-brief.md`
  - `10-resources/templates/three-amigos-output-template.md`
- Stop conditions:
  - Any required input missing

## Process

### Phase 0: Prepare

- Goal: Validate prerequisites, create working directories, write manifest.
- Run: `python3 02-workflows/assess-mvp-by-three-amigos/prepare-three-amigos-inputs.py`
- Paths:
  - Creates `04-process/06-assess-mvp-by-three-amigos/phase1-reviews/`
  - Creates `04-process/06-assess-mvp-by-three-amigos/phase2-discussion/`
  - Writes `04-process/06-assess-mvp-by-three-amigos/manifest.json`
- PASS when: Manifest written, all inputs validated, directories created
- WARN when: N/A
- FAIL when: Script exits non-zero or manifest not written
- If fail: Identify the missing input, resolve it, rerun once

### Phase 1: Create Team and Independent Reviews

- Goal: Create the Three Amigos team. Each specialist independently reviews the MVP brief from their lens without seeing the others' work.
- Run:
  1. `TeamCreate` with team name `three-amigos`
  2. Spawn all three reviewers IN PARALLEL using the Agent tool with `team_name: three-amigos`:
     - `ux-three-amigos-reviewer` → `04-process/06-assess-mvp-by-three-amigos/phase1-reviews/desirability-review.md`
     - `engineer-three-amigos-reviewer` → `04-process/06-assess-mvp-by-three-amigos/phase1-reviews/feasibility-review.md`
     - `pm-three-amigos-reviewer` → `04-process/06-assess-mvp-by-three-amigos/phase1-reviews/viability-review.md`
- Input for all three agents:
  - `manifest_file` — `04-process/06-assess-mvp-by-three-amigos/manifest.json`
  - `mode` — `independent`
- Output: 3 review files in `phase1-reviews/`
- PASS when: All 3 files exist and are non-empty
- WARN when: N/A
- FAIL when: Any review file missing or empty
- If fail: Re-run the failed agent once with a specific correction instruction

### Phase 2: Discussion Round

- Goal: Facilitate genuine inter-agent discussion. Each specialist responds to the other two reviews via SendMessage. Orchestrator records all messages into the discussion transcript.
- Run:

  **Step 1 — Read and broadcast Phase 1 reviews:**
  - Read all 3 Phase 1 review files
  - Broadcast to all three teammates (SendMessage, type: broadcast):
    ```
    Phase 1 reviews are complete. Here are all three assessments:

    --- DESIRABILITY REVIEW ---
    [contents of desirability-review.md]

    --- FEASIBILITY REVIEW ---
    [contents of feasibility-review.md]

    --- VIABILITY REVIEW ---
    [contents of viability-review.md]

    Please review all three and send your Discussion Round 1 response. Address specific points
    from the other two lenses — challenge, agree, or identify tensions. Be direct and specific.
    ```

  **Step 2 — Collect Round 1 responses:**
  - Each specialist sends a SendMessage response to the orchestrator
  - Record each message into `discussion-transcript.md` under `## Round 1` (see Transcript Format below)
  - Wait until all 3 Round 1 responses received before proceeding

  **Step 3 — Re-broadcast Round 1 responses:**
  - Broadcast Round 1 responses to all teammates:
    ```
    Round 1 responses received. Here is what your colleagues said:

    [UX Researcher's Round 1 response]
    [Engineer's Round 1 response]
    [Product Manager's Round 1 response]

    Please send your Round 2 follow-up. Focus on the most important disagreement or
    unresolved tension. 3–5 bullets maximum.
    ```

  **Step 4 — Collect Round 2 responses:**
  - Record Round 2 messages into `discussion-transcript.md` under `## Round 2`
  - After Round 2, close the discussion: send shutdown_request to all three reviewers

- Output: `04-process/06-assess-mvp-by-three-amigos/discussion-transcript.md`
- PASS when: Transcript exists, ≥6 messages recorded (≥2 per specialist)
- WARN when: Fewer than 6 messages — note in transcript header, continue to Phase 3
- FAIL when: Transcript missing or fewer than 3 messages total
- If fail: Re-broadcast Phase 1 reviews with a more specific prompt, collect responses again

### Phase 3: Synthesis

- Goal: Combine all specialist reviews and the discussion transcript into the final assessment document.
- Run: `three-amigos-synthesizer` (spawned as a standalone agent, outside the team)
- Input (passed as parameters):
  - `manifest_file` — `04-process/06-assess-mvp-by-three-amigos/manifest.json`
  - Agent reads `phase1_dir`, `phase2_dir`, `transcript_file`, `template_file`, `output_file` from manifest
- Output: `05-outputs/06-assess-mvp-by-three-amigos/mvp-three-amigos-assessment.md`
- PASS when: Output file exists and is non-empty
- WARN when: N/A
- FAIL when: Output missing or empty
- If fail: Re-run once with correction (e.g. "word count exceeded — cut Executive Summary first")

### Phase 4: Verify and Shutdown

- Goal: Deterministically verify structural and constraint compliance. Clean up the team.
- Run:
  1. `python3 02-workflows/assess-mvp-by-three-amigos/verify-three-amigos-output.py --file 05-outputs/06-assess-mvp-by-three-amigos/mvp-three-amigos-assessment.md --max-words 2500`
  2. `TeamDelete` (team should already be empty after Phase 2 shutdown; this cleans up the team record)
- PASS when: All 6 required headings present, word count ≤ 2500, footer present, ≥5 recommendations present, ≤5 recommendations present
- FAIL when: Verifier returns FAIL
- If fail: Re-run Phase 3 once with the specific failure as a correction instruction, then re-verify

### Human Review Gate

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger: Phase 4 returns PASS
- Summarise:
  - Word count
  - Number of Cross-Cutting Tensions identified
  - Number of Consensus Recommendations
  - Any WARN conditions during the run
- Ask user:
  - `Verification passed. Review the Three Amigos assessment quality. Proceed to completion?`

## Acceptance Criteria Traceability (Directive → Checks)

| Directive Acceptance Criterion | Where Enforced | Mechanism |
|---|---|---|
| Three independent specialist reviews exist | Phase 1 (3 files) + Phase 4 verify | Verifier checks 3 review files exist |
| Discussion transcript captures full Phase 2 exchange | Phase 2 (transcript) + Phase 4 verify | Verifier checks transcript exists and message count |
| Transcript contains genuine back-and-forth | Phase 2 (2 rounds) + Human Gate | Orchestrator enforces 2 rounds; human confirms quality |
| Final doc follows output template | Phase 3 (synthesizer) + Phase 4 (headings) | Verifier checks all 6 required headings |
| Maximum 2,500 words | Phase 4 verify | Verifier word count check |
| Bullet points and short sentences | Phase 3 (synthesizer instructions) + Human Gate | Human confirms format |
| Cross-Cutting Tensions identifies genuine disagreements | Phase 3 + Human Gate | Verifier checks heading present; human confirms content |
| Consensus Recommendations ≤ 5 | Phase 4 verify | Verifier counts recommendations |
| Team cleanly shut down | Phase 4 shutdown + TeamDelete | TeamDelete confirms no orphaned teammates |

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/assess-mvp-by-three-amigos/prepare-three-amigos-inputs.py` — validates prerequisites, creates dirs, writes manifest
- `02-workflows/assess-mvp-by-three-amigos/verify-three-amigos-output.py` — validates headings, word count, footer, recommendation count
- `ux-three-amigos-reviewer` — Desirability lens (independent review + SendMessage discussion)
- `engineer-three-amigos-reviewer` — Feasibility lens (independent review + SendMessage discussion)
- `pm-three-amigos-reviewer` — Viability lens (independent review + SendMessage discussion)
- `three-amigos-synthesizer` — assembles final assessment from all reviews + transcript

## Manifest Format

`04-process/06-assess-mvp-by-three-amigos/manifest.json`:

- `workflow` — `assess-mvp-by-three-amigos`
- `created_at` — UTC ISO timestamp
- `mvp_brief_file` — `05-outputs/04-generate-mvp-document/mvp-brief.md`
- `strategic_brief_file` — `00-brief/strategic-research-brief.md`
- `template_file` — `10-resources/templates/three-amigos-output-template.md`
- `phase1_dir` — `04-process/06-assess-mvp-by-three-amigos/phase1-reviews/`
- `phase2_dir` — `04-process/06-assess-mvp-by-three-amigos/phase2-discussion/`
- `transcript_file` — `04-process/06-assess-mvp-by-three-amigos/discussion-transcript.md`
- `output_file` — `05-outputs/06-assess-mvp-by-three-amigos/mvp-three-amigos-assessment.md`

## Sub-agent Parameters

**Phase 1 reviewers (all three):**
- `manifest_file` — `04-process/06-assess-mvp-by-three-amigos/manifest.json`
- `mode` — `independent`

**Phase 3 synthesizer:**
- `manifest_file` — `04-process/06-assess-mvp-by-three-amigos/manifest.json`

## Discussion Transcript Format

`04-process/06-assess-mvp-by-three-amigos/discussion-transcript.md`:

```markdown
# Discussion Transcript

*Three Amigos panel — [Date]*
*Participants: UX Researcher (Desirability), Engineer (Feasibility), Product Manager (Viability)*

## Phase 1 Review Summaries

### Desirability Review
[1–2 sentence summary of key points from desirability-review.md]

### Feasibility Review
[1–2 sentence summary of key points from feasibility-review.md]

### Viability Review
[1–2 sentence summary of key points from viability-review.md]

---

## Round 1

**[UX Researcher]**
[Message content verbatim]

**[Engineer]**
[Message content verbatim]

**[Product Manager]**
[Message content verbatim]

---

## Round 2

**[UX Researcher]**
[Message content verbatim]

**[Engineer]**
[Message content verbatim]

**[Product Manager]**
[Message content verbatim]
```

## Output Promotion

- Phase 1 and Phase 2 review files stay in `04-process/06-assess-mvp-by-three-amigos/`.
- Discussion transcript stays in `04-process/06-assess-mvp-by-three-amigos/`.
- Final assessment is written directly to `05-outputs/06-assess-mvp-by-three-amigos/mvp-three-amigos-assessment.md`.
- Do not overwrite an existing `05-outputs` deliverable without explicit user confirmation.

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Preconditions satisfied
- [ ] All directive acceptance criteria mapped in traceability table
- [ ] All mapped checks reached PASS/WARN state
- [ ] 3 Phase 1 review files exist in `04-process/06-assess-mvp-by-three-amigos/phase1-reviews/`
- [ ] Discussion transcript exists with ≥6 messages
- [ ] Final deliverable exists at `05-outputs/06-assess-mvp-by-three-amigos/mvp-three-amigos-assessment.md`
- [ ] Team cleanly shut down (TeamDelete confirmed)
- [ ] User-facing summary includes word count, tensions count, recommendation count, final status
- [ ] Run log entry appended

## Learnings

### Run 1 — March 2026

**SendMessage broadcast delivery to idle spawned agents does not work.**
After Phase 1 agents complete and go idle, broadcasting Phase 1 reviews to them produces no responses. Spawned agents via the Agent tool appear to terminate after completing their initial task rather than remaining genuinely idle for follow-up messages.

**Workaround: respawn agents in discussion mode, writing responses to files.**
For Phase 2, spawn each specialist fresh with all Phase 1 review content embedded directly in the prompt. Have them WRITE their response to a specific file in `phase2-discussion/` rather than using SendMessage. The orchestrator reads all files and assembles the transcript manually.

**Updated Phase 2 pattern:**
1. Read all 3 Phase 1 review files
2. Spawn 3 new discussion agents in parallel, each receiving all 3 reviews in their prompt and a specific output file path
3. Spawn 3 more agents for Round 2, each receiving all Round 1 responses in their prompt
4. Orchestrator reads all 6 files and writes the transcript manually

**TeamDelete requires manual cleanup.**
Shutdown requests sent via SendMessage to idle spawned agents are not processed. TeamDelete therefore cannot confirm shutdown. Workaround: `rm -rf ~/.claude/teams/{team-name} ~/.claude/tasks/{team-name}`.

**`three-amigos-synthesizer` subagent_type now available.**
The agent folder has been renamed from `3-amigos-synthesizer` to `three-amigos-synthesizer`, enabling registration as a named subagent type. The synthesizer can now be invoked directly via `subagent_type: "three-amigos-synthesizer"`.

**Discussion quality was high despite file-based workaround.**
Two rounds × 3 specialists produced substantive cross-lens engagement. File-writing pattern does not compromise discussion quality.
