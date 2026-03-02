# Directive: Extract and Tag Quotes

## Goal

Extract verbatim quotes from every interview transcript, tag each with a memorable label, severity, sentiment, and question reference. Identify internal contradictions per participant. Consolidate the raw tags to a canonical set of around 40 labels.

These outputs are the evidential foundation for all downstream persona workflows.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

The raw transcripts contain rich qualitative insight. This workflow extracts, validates, and organises that insight so it can be reliably used for archetype synthesis and persona creation.

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

## Workflow

`02-workflows/extract-and-tag-quotes/`

## Success Criteria

- Every participant has at least one extracted quote
- All quotes pass verbatim validation (exact match in source transcript)
- Contradictions are identified and documented per participant
- Consolidated tag count is between 35 and 45
- No over-broad catch-all tags; no dominant mega-tags
