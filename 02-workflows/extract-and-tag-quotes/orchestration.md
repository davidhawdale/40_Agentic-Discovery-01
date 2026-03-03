# Extract and Tag Quotes

> **Directive workflow** — triggered by user request. See `01-directives/extract-and-tag-quotes.md` for goal, inputs, and acceptance criteria.

## Approach

Extract verbatim quotes from every interview transcript, tag each with a memorable label, severity rating, sentiment, and question reference. Identify where participants contradict themselves. Consolidate the raw tags to a canonical set of around 40 labels.

The outputs of this workflow are the evidential foundation for all downstream persona and roleplay workflows.

## Process

### Phase 0: Prepare

- Goal: Validate inputs and build a manifest of all transcripts to process.
- Run: `python3 02-workflows/extract-and-tag-quotes/prepare.py`
- Paths:
  - Transcripts in: `03-inputs/interview-transcripts/`
  - Research brief in: `03-inputs/research-brief.md`
  - Manifest out: `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
- Input: Files in `03-inputs/interview-transcripts/`, research brief
- Output: `p0-prepare/manifest.json` with transcript count, file paths, and language flags
- If fail: Check `03-inputs/` structure; ensure transcripts are in expected format

### Phase 1: Extract Quotes

- Goal: Extract notable quotes from each transcript; tag each with a memorable label, severity rating, sentiment, and question reference
- Input: Each transcript entry from `p0-prepare/manifest.json`
- Spawn all `transcript-quote-extractor` sub-agents in parallel — one per transcript — each with these values in the task prompt:
  - `participant_id` — from manifest
  - `transcript_id` — from manifest (`id` field)
  - `transcript_path` — full path to the transcript file (from manifest `path` field, resolved from project root)
  - `output_path` — `04-process/extract-and-tag-quotes/p1-quote-extraction/quote-parts/{participant_id}.csv`
- Output: One CSV part file per transcript in `04-process/extract-and-tag-quotes/p1-quote-extraction/quote-parts/`
- Merge: `python3 02-workflows/extract-and-tag-quotes/merge-quotes.py`
- Validate completeness: `python3 02-workflows/extract-and-tag-quotes/verify-quote-extracts-completion.py`
- If fail: Re-run the failed agent with a specific correction instruction; if second fail, skip and log WARN

### Phase 2: Validate Quotes

- Goal: Confirm every extracted quote is verbatim — no paraphrasing.
- Run: `python3 02-workflows/extract-and-tag-quotes/validate-quotes.py`
- Input: `p1-quote-extraction/quotes.csv` + `p0-prepare/manifest.json` (for transcript paths)
- Output: `p2-validate-quotes/quote-validation-report.csv` (status, reason, transcript_match, transcript_lines per quote)
- If FAIL: quote was paraphrased — re-run that participant's extractor with explicit instruction to copy text verbatim; if second fail, flag for human review

### Phase 2 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 2 completes, read `p2-validate-quotes/quote-validation-report.csv` and present a summary:

```
Phase 2 complete — Quote Validation Summary
───────────────────────────────────────────
Total quotes:   N
Passed:         N
Failed:         N

[If failures > 0, list each:]
  FAIL  [tag]  participant: [id]  reason: [reason]

[If failures = 0:]
  All quotes passed verbatim check.
```

Then ask:

- **If failures > 0:** "There are [N] failed quotes. Would you like to go back and re-run the affected participant(s) before continuing, or continue to the next phase anyway?"
- **If failures = 0:** "All quotes passed. Ready to continue to the next phase?"

Do not proceed to the next phase until the user explicitly says yes.

### Phase 3: Check for Contradictions

- Goal: For each participant, identify where their quotes contradict each other. Apply the rules in `.claude/rules/contradiction-rules.md`.
- Input: `p1-quote-extraction/quotes.csv` (all validated quotes) + `p0-prepare/manifest.json` (for participant list)
- Sequence:
  1. Run `participant-contradiction-checker` per participant.
  2. Run `python3 02-workflows/extract-and-tag-quotes/verify-contradictions-completion.py`.
  3. Run `python3 02-workflows/extract-and-tag-quotes/merge-contradictions.py`.
  4. Run the Phase 3 Human Review Gate summary and stop for user confirmation.
- Spawn all `participant-contradiction-checker` sub-agents in parallel — one per participant — each with:
  - `participant_id` — from manifest
  - `transcript_id` — from manifest (`id` field)
  - `quotes_path` — full path to `p1-quote-extraction/quotes.csv`
  - `output_path` — `04-process/extract-and-tag-quotes/p3-check-contradictions/contradiction-parts/{participant_id}.csv`
- In Codex/OpenAI, "spawn sub-agent" means: read `.claude/agents/participant-contradiction-checker.md` and execute those instructions inline for each participant.
- Output: One CSV part file per participant in `04-process/extract-and-tag-quotes/p3-check-contradictions/contradiction-parts/` (empty CSV with header if no contradictions)
- Verify completion: `python3 02-workflows/extract-and-tag-quotes/verify-contradictions-completion.py`
- Merge: `python3 02-workflows/extract-and-tag-quotes/merge-contradictions.py`
- If fail: Re-run the failed agent once with a specific correction instruction; if second fail, skip and log WARN

### Phase 3 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 3 completes, read:

- `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
- `04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv`

Present a summary:

```
Phase 3 complete — Contradiction Check Summary
──────────────────────────────────────────────
Participants checked:             N
Participants with contradictions: N
Total contradictions found:       N

[If contradictions found:]
  Detailed results: 04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv
  Use this file for participant-level contradiction details and quote pairs.

[If none:]
  No contradictions found across all participants.
```

Then ask:

- **If contradictions found:** "There are [N] contradictions across [N] participants. Please review 04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv. Would you like to re-run any participants before continuing?"
- **If none:** "No contradictions found. Ready to continue to the next phase?"

Do not proceed to the next phase until the user explicitly says yes.

### Phase 4: Consolidate the Quote Tags

- Goal: Consolidate `p1` quote tags to a canonical set of around 40 tags (hard range 35-45) without changing quote text.
- Input:
  - `04-process/extract-and-tag-quotes/p1-quote-extraction/quotes.csv`
- Sequence:
  1. Build tag mapping with `tag-consolidator`.
  2. Run `python3 02-workflows/extract-and-tag-quotes/run-tag-consolidation.py`.
  3. Run `python3 02-workflows/extract-and-tag-quotes/verify-tag-consolidation.py`.
  4. Run the Phase 4 Human Review Gate summary and stop for user confirmation.
- For consolidation mapping, spawn a `tag-consolidator` sub-agent with:
  - `quotes_path` — full path to `p1-quote-extraction/quotes.csv`
  - `output_mapping_path` — `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-mapping.json`
- In Codex/OpenAI, "spawn sub-agent" means: read `.claude/agents/tag-consolidator.md` and execute those instructions inline.
- Output:
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv` (all original quote rows + `consolidated_tag`)
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-crosswalk.csv` (original tag to consolidated tag mapping)
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-consolidation-report.md` (summary and distribution)
- Constraints:
  - Do not overwrite `p1-quote-extraction/quotes.csv`
  - Do not alter any `quote` text in output rows
  - Enforce semantic quality first (no over-broad catch-all buckets, avoid pass-through mapping, avoid dominant mega-buckets)
  - Only after semantic quality passes, enforce consolidated unique tag count between 35 and 45
- If fail: Re-run the failed agent/script once with a specific correction instruction; if second fail, skip and log WARN

### Phase 4 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

After Phase 4 completes, read:

- `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv`
- `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-consolidation-report.md`

Present a summary:

```
Phase 4 complete — Tag Consolidation Summary
────────────────────────────────────────────
Total quotes:              N
Original unique tags:      N
Consolidated unique tags:  N

Detailed results:
  04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-consolidation-report.md
  04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv
```

Then ask:

- **If validation passes:** "Phase 4 passed. Please review the report and consolidated quotes output. Ready to copy outputs and complete this workflow?"
- **If validation fails:** "Phase 4 has validation failures. Would you like to re-run consolidation with correction instructions?"

Do not proceed until the user explicitly says yes.

### Final Step: Copy Outputs

After the user confirms Phase 4 is complete and satisfactory, copy the final deliverables to `05-outputs/extract-and-tag-quotes/`:

```bash
mkdir -p 05-outputs/extract-and-tag-quotes
cp 04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv 05-outputs/extract-and-tag-quotes/quotes.csv
cp 04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv 05-outputs/extract-and-tag-quotes/contradictions.csv
cp 04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-consolidation-report.md 05-outputs/extract-and-tag-quotes/tag-consolidation-report.md
```

Confirm files are present, then report workflow complete.

---

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
