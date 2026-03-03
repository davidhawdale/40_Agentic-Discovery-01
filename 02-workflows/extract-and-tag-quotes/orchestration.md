# Extract and Tag Quotes

> **Directive workflow** — triggered by user request. See `01-directives/extract-and-tag-quotes.md` for goal, inputs, and acceptance criteria.

## Approach

Extract verbatim quotes from every interview transcript, tag each with a memorable label, severity rating, sentiment, and question reference. Identify where participants contradict themselves. Consolidate the raw tags to a canonical set of around 40 labels.

The outputs of this workflow are the evidential foundation for all downstream persona and roleplay workflows.

## Preconditions

- Required inputs:
  - `03-inputs/interview-transcripts/`
  - `03-inputs/research-brief.md`
- Expected counts/shape:
  - Non-empty transcript set
  - Transcript filenames follow recognized patterns for manifest generation (`en_participant_####.txt` and `en_translated_from_{lang}_participant_####.txt`)
- Stop conditions:
  - Missing or empty transcript directory
  - Missing research brief
  - `prepare.py` fails to generate `p0-prepare/manifest.json`

## Process

### Phase 0: Prepare

- Goal: Validate inputs and build a manifest of all transcripts to process.
- Run:
  1. `python3 02-workflows/extract-and-tag-quotes/prepare.py`
- Input:
  - Files in `03-inputs/interview-transcripts/`
  - `03-inputs/research-brief.md`
- Output:
  - `04-process/extract-and-tag-quotes/p0-prepare/manifest.json` (transcript count, transcript metadata, brief path, warnings)
- PASS when:
  - Manifest file is written successfully
- WARN when:
  - Input count/shape warnings are emitted but manifest is still written
- FAIL when:
  - Required inputs are missing
  - Manifest is not written
- If fail:
  - Check `03-inputs/` structure and filenames, correct inputs, then apply retry policy

### Phase 1: Extract Quotes

- Goal: Extract notable quotes from each transcript and tag each with label, severity, sentiment, and question reference.
- Run:
  1. Run `transcript-quote-extractor` for each transcript in manifest (run all participants in parallel)
  2. `python3 02-workflows/extract-and-tag-quotes/merge-quotes.py`
  3. `python3 02-workflows/extract-and-tag-quotes/verify-quote-extracts-completion.py`
- Input:
  - `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
- Output:
  - `04-process/extract-and-tag-quotes/p1-quote-extraction/quote-parts/{participant_id}.csv`
  - `04-process/extract-and-tag-quotes/p1-quote-extraction/quotes.csv`
- PASS when:
  - `quotes.csv` is produced
  - Completion verification passes for all manifest participants
- WARN when:
  - Non-blocking row-level issues are logged but participant coverage remains complete
- FAIL when:
  - Quote extraction or merge fails
  - Completion verification reports missing participants
- If fail:
  - Apply retry policy with specific correction instructions to failed participant(s)/step

### Phase 2: Validate Quotes

- Goal: Confirm every extracted quote is verbatim (no paraphrasing).
- Run:
  1. `python3 02-workflows/extract-and-tag-quotes/validate-quotes.py`
- Input:
  - `04-process/extract-and-tag-quotes/p1-quote-extraction/quotes.csv`
  - `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
- Output:
  - `04-process/extract-and-tag-quotes/p2-validate-quotes/quote-validation-report.csv`
- PASS when:
  - Validation report is generated and all rows pass
- WARN when:
  - Validation report is generated with limited failures that user chooses to defer after gate review
- FAIL when:
  - Validation script fails to run
  - Report cannot be produced
- If fail:
  - Apply retry policy; for paraphrase failures, re-run affected participant extractor(s) with explicit verbatim instruction

### Phase 2 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger:
  - Phase 2 completes and validation report exists
- Read:
  - `04-process/extract-and-tag-quotes/p2-validate-quotes/quote-validation-report.csv`
- Summarise:
  - Total quotes
  - PASS/FAIL counts
  - Failed rows with participant/tag/reason (if any)
- Ask user:
  - If failures > 0: "There are [N] failed quotes. Would you like to go back and re-run the affected participant(s) before continuing, or continue to the next phase anyway?"
  - If failures = 0: "All quotes passed. Ready to continue to the next phase?"
- Stop rule:
  - Do not proceed until user explicitly confirms.

### Phase 3: Check for Contradictions

- Goal: Identify where each participant's quotes contradict each other using contradiction rules.
- Run:
  1. Run `participant-contradiction-checker` for each participant in manifest (run all participants in parallel)
  2. `python3 02-workflows/extract-and-tag-quotes/verify-contradictions-completion.py`
  3. `python3 02-workflows/extract-and-tag-quotes/merge-contradictions.py`
- Input:
  - `04-process/extract-and-tag-quotes/p1-quote-extraction/quotes.csv`
  - `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
- Output:
  - `04-process/extract-and-tag-quotes/p3-check-contradictions/contradiction-parts/{participant_id}.csv`
  - `04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv`
- PASS when:
  - Completion verification passes for all participants
  - Merged contradictions file is produced
- WARN when:
  - No contradictions found for all participants (valid outcome)
  - Non-blocking issues are logged and reviewed
- FAIL when:
  - Completion verification fails
  - Merge step fails
- If fail:
  - Apply retry policy with specific correction instructions

### Phase 3 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger:
  - Phase 3 completes and contradictions output is available
- Read:
  - `04-process/extract-and-tag-quotes/p0-prepare/manifest.json`
  - `04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv`
- Summarise:
  - Participants checked
  - Participants with contradictions
  - Total contradictions found
- Ask user:
  - If contradictions found: "There are [N] contradictions across [N] participants. Please review 04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv. Would you like to re-run any participants before continuing?"
  - If none: "No contradictions found. Ready to continue to the next phase?"
- Stop rule:
  - Do not proceed until user explicitly confirms.

### Phase 4: Consolidate the Quote Tags

- Goal: Consolidate Phase 1 quote tags to a canonical set around 40 tags (hard range 35-45) without changing quote text.
- Run:
  1. Run `tag-consolidator` to produce mapping
  2. `python3 02-workflows/extract-and-tag-quotes/run-tag-consolidation.py`
  3. `python3 02-workflows/extract-and-tag-quotes/verify-tag-consolidation.py`
- Input:
  - `04-process/extract-and-tag-quotes/p1-quote-extraction/quotes.csv`
- Output:
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-mapping.json`
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv`
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-crosswalk.csv`
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-consolidation-report.md`
- PASS when:
  - Consolidation and verification steps pass
  - Unique consolidated tag count is between 35 and 45
- WARN when:
  - Non-blocking quality notes are logged and reviewed
- FAIL when:
  - Verification fails on tag-count bounds or semantic quality constraints
  - Consolidation outputs are missing or malformed
- If fail:
  - Apply retry policy with specific correction instructions

### Phase 4 Gate: Human Review — HARD STOP

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger:
  - Phase 4 completes with consolidated outputs and report
- Read:
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv`
  - `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-consolidation-report.md`
- Summarise:
  - Total quotes
  - Original unique tags
  - Consolidated unique tags
- Ask user:
  - If validation passes: "Phase 4 passed. Please review the report and consolidated quotes output. Ready to copy outputs and complete this workflow?"
  - If validation fails: "Phase 4 has validation failures. Would you like to re-run consolidation with correction instructions?"
- Stop rule:
  - Do not proceed until user explicitly confirms.

## Acceptance Criteria Traceability (Directive -> Checks)

Use this section for directive workflows to map each directive acceptance criterion to concrete workflow checks.

| Directive Acceptance Criterion | Where Enforced in Workflow | Enforcement Mechanism |
|---|---|---|
| Every participant has at least one extracted quote | Phase 1 (`verify-quote-extracts-completion.py`) | Verifies manifest participants are present in `p1-quote-extraction/quotes.csv`; FAIL if any participant is missing. |
| All quotes pass verbatim validation (exact match in source transcript) | Phase 2 (`validate-quotes.py`) + Phase 2 Human Review Gate | Produces per-quote PASS/FAIL report; workflow pauses for user review before proceeding. |
| Contradictions are identified and documented per participant | Phase 3 (`verify-contradictions-completion.py` + `merge-contradictions.py`) | Verifies per-participant contradiction part coverage and merges into consolidated contradictions output. |
| Consolidated tag count is between 35 and 45 | Phase 4 (`run-tag-consolidation.py` + `verify-tag-consolidation.py`) | Enforces hard unique-tag bounds and fails if outside range. |
| No over-broad catch-all tags; no dominant mega-tags | Phase 4 (`run-tag-consolidation.py` + `verify-tag-consolidation.py`) | Applies semantic quality checks for catch-all markers and dominant-tag ratio limits; FAIL on violation. |

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/extract-and-tag-quotes/prepare.py` — validates inputs and writes manifest.
- `02-workflows/extract-and-tag-quotes/merge-quotes.py` — merges per-participant quote parts into `quotes.csv`.
- `02-workflows/extract-and-tag-quotes/verify-quote-extracts-completion.py` — verifies participant coverage in quote extraction.
- `02-workflows/extract-and-tag-quotes/validate-quotes.py` — checks verbatim quote matching against transcripts.
- `02-workflows/extract-and-tag-quotes/verify-contradictions-completion.py` — verifies per-participant contradiction part coverage and schema.
- `02-workflows/extract-and-tag-quotes/merge-contradictions.py` — merges contradiction parts into `contradictions.csv`.
- `02-workflows/extract-and-tag-quotes/run-tag-consolidation.py` — applies mapping to produce consolidated tag outputs.
- `02-workflows/extract-and-tag-quotes/verify-tag-consolidation.py` — validates tag consolidation integrity and semantic guardrails.
- `transcript-quote-extractor` sub-agent — extracts and tags verbatim quotes per transcript.
- `participant-contradiction-checker` sub-agent — identifies contradiction signals per participant.
- `tag-consolidator` sub-agent — generates tag mapping for consolidation.

## Manifest Format

`04-process/extract-and-tag-quotes/p0-prepare/manifest.json`:

- `transcript_count` (integer)
- `research_brief_path` (string)
- `warnings` (string list)
- `transcripts` (array), each item includes:
  - `id` (transcript id)
  - `participant_id` (participant key used across phases)
  - `path` (relative transcript file path)
  - `language` (current transcript language)
  - `source_language` (original language for translated transcripts, else `null`)
  - `translated` (boolean)
  - `size_bytes` (integer)

## Sub-agent Parameters

### `transcript-quote-extractor`

- `participant_id` — from manifest `transcripts[].participant_id`
- `transcript_id` — from manifest `transcripts[].id`
- `transcript_path` — from manifest `transcripts[].path` resolved from project root
- `output_path` — `04-process/extract-and-tag-quotes/p1-quote-extraction/quote-parts/{participant_id}.csv`

### `participant-contradiction-checker`

- `participant_id` — from manifest `transcripts[].participant_id`
- `transcript_id` — from manifest `transcripts[].id`
- `quotes_path` — `04-process/extract-and-tag-quotes/p1-quote-extraction/quotes.csv`
- `output_path` — `04-process/extract-and-tag-quotes/p3-check-contradictions/contradiction-parts/{participant_id}.csv`

### `tag-consolidator`

- `quotes_path` — `04-process/extract-and-tag-quotes/p1-quote-extraction/quotes.csv`
- `output_mapping_path` — `04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-mapping.json`

## Output Promotion

- Process artifacts remain in `04-process/extract-and-tag-quotes/`.
- Final deliverables are promoted to `05-outputs/extract-and-tag-quotes/`.
- Do not overwrite existing `05-outputs/extract-and-tag-quotes/` files without explicit user confirmation.

### Final Step: Copy Outputs

After the user confirms Phase 4 is complete and satisfactory, copy the final deliverables to `05-outputs/extract-and-tag-quotes/`:

```bash
mkdir -p 05-outputs/extract-and-tag-quotes
cp 04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv 05-outputs/extract-and-tag-quotes/quotes.csv
cp 04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv 05-outputs/extract-and-tag-quotes/contradictions.csv
cp 04-process/extract-and-tag-quotes/p4-consolidate-tags/tag-consolidation-report.md 05-outputs/extract-and-tag-quotes/tag-consolidation-report.md
```

Confirm files are present, then report workflow complete.

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Preconditions satisfied (or explicitly resolved)
- [ ] All directive acceptance criteria are mapped in traceability table
- [ ] All mapped checks reached required PASS/WARN state
- [ ] Final files exist in `05-outputs/extract-and-tag-quotes/`
- [ ] User-facing summary includes counts, issues, and final status
- [ ] Run log entry appended (if workflow logging is enabled)

---

## Learnings

_Update this section as you encounter errors, constraints, or improvements during execution._
