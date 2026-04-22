# Directive: Synthesise Archetypes

## Goal

Cluster interview participants into five named core archetypes based on attitudes, behaviours, and evidence patterns, creating a clear participant segmentation that will anchor downstream persona development. Participants who do not fit strongly into any core archetype should be treated as outliers.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

With quotes extracted and tagged, this workflow identifies the recurring participant patterns that matter for product understanding. The resulting archetypes provide the structural bridge between quote-level evidence and persona-level synthesis.

## Strategic Success Criteria

This workflow should produce a segmentation that is evidence-grounded, decision-useful, and meaningfully differentiated, so teams can reason about distinct user types rather than aggregate averages. Archetypes should support stronger downstream persona quality and clearer product trade-off discussions.

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

## Out of Scope

- Creating persona profiles or persona narratives
- Re-running quote extraction, quote validation, or tag consolidation
- Producing product recommendations or prioritisation decisions directly
- Rewriting source transcript evidence

## Acceptance Criteria

1. Exactly five core archetypes are produced.
2. Every participant is assigned exactly once (to a core archetype or outlier).
3. Outlier cap: no more than 2 outliers in a cohort of approximately 50 participants.
4. Each archetype includes three verbatim evidence quotes from three different participants in that archetype.
5. Archetype names and descriptions are clearly differentiated and interpretable by downstream teams.
6. Outputs are usable as the direct foundation for the `build-personas` workflow.

## Workflow

See `02-workflows/synthesise-archetypes/` for the detailed process.
