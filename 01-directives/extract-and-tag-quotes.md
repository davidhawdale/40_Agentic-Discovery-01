# Directive: Extract and Tag Quotes

## Goal

Extract evidence-rich interview quotes and organise them into a usable tagged dataset, including participant-level contradictions, so downstream workflows can reliably synthesise archetypes and personas.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

The raw transcripts contain high-value qualitative insight, but that insight must be structured before it can drive consistent downstream analysis. This workflow turns raw transcript material into a clear evidence base for subsequent interpretation and synthesis.

## Strategic Success Criteria

This workflow should produce a dependable evidence foundation that helps later stages represent real user motivations, friction points, and trust/value dynamics in line with the product vision. The output should improve decision quality by making source-backed signals easy to reuse.

## Inputs

| Input | Location |
|-------|----------|
| Interview transcripts | `03-inputs/interview-transcripts/` |
| Research brief | `03-inputs/research-brief.md` |

## Outputs

| Output | Location |
|--------|----------|
| Validated consolidated quotes | `05-outputs/extract-and-tag-quotes/quotes.csv` |
| Participant contradictions | `05-outputs/extract-and-tag-quotes/contradictions.csv` |
| Tag consolidation report | `05-outputs/extract-and-tag-quotes/tag-consolidation-report.md` |

## Out of Scope

- Synthesising archetypes or generating personas
- Producing product recommendations or prioritisation decisions
- Redefining downstream workflow outputs or templates
- Interpreting findings beyond evidence extraction and organisation

## Acceptance Criteria

1. A complete, reusable quote evidence set is produced from the interview corpus.
2. All quotes pass verbatim validation (exact match in source transcript).
3. Participant-level contradiction signals are captured as part of the evidence base.
4. Consolidated tag count is between 35 and 45.
5. No over-broad catch-all tags and no dominant mega-tags.

## Workflow

See `02-workflows/extract-and-tag-quotes/` for the detailed process.
