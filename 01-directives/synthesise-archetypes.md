# Directive: Synthesise Archetypes

## Goal

Cluster all interview participants into exactly five named core archetypes based on their attitudes, behaviours, and quote patterns. Each archetype captures a distinct participant type grounded in transcript evidence.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

With quotes extracted and tagged, this workflow identifies the underlying participant patterns that will shape the five Dynamic Personas. Every participant must be assigned to exactly one archetype (or flagged as an outlier).

## Inputs

| Input | Location |
|-------|----------|
| Consolidated quotes | `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv` |
| Transcript manifest | `04-process/extract-and-tag-quotes/p0-prepare/manifest.json` |

> These are produced by the `extract-and-tag-quotes` workflow. Run that workflow first.

## Outputs

| Output | Location |
|--------|----------|
| Five archetype profiles | `05-outputs/synthesise-archetypes/archetypes.md` |
| Participant archetype assignments | `05-outputs/synthesise-archetypes/participant-archetype-assignments.csv` |

## Workflow

`02-workflows/synthesise-archetypes/`

## Success Criteria

- Exactly 5 core archetypes produced
- Every participant assigned exactly once (core or outlier)
- Each archetype includes 3 verbatim evidence quotes from 3 different participants in that archetype
- Archetype names and descriptions are meaningfully differentiated
