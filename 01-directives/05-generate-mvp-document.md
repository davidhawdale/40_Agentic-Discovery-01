# Directive: Generate MVP Document

## Goal

Synthesize research findings and market context into a concise MVP brief for a personal AI assistant product, so the product team can decide what to build first, what to test, and whether the opportunity justifies investment.

## Context

> From `00-brief/strategic-research-brief.md`: Build an AI assistant that people choose to use daily for their personal needs, and develop a compelling product story backed by user insights to secure Series A funding.

This workflow draws on existing participant evidence, archetypes, and personas generated upstream, combines them with external market data, and frames the result as a practical MVP brief: not a feature spec, but a learning plan with a defined user, testable hypotheses, and a credible revenue case.

## Strategic Success Criteria

The deliverable should give a product team enough to act: a clear problem to solve, a defined target user, testable experiments, known risks, and a credible revenue opportunity. It should be readable in under ten minutes and decision-ready on first pass.

## Inputs

| Input | Location |
|-------|----------|
| VC pitch one-pager | `05-outputs/04-generate-vc-pitch/vc-pitch-one-pager.md` |
| Participant archetypes | `05-outputs/synthesise-archetypes/archetypes.md` |
| Personas | `05-outputs/03-build-personas/personas/*.md` |
| Strategic research brief | `00-brief/strategic-research-brief.md` |
| External market research | Web (competitor pricing, market size, identified gaps) |

> The VC pitch, archetypes, and personas must exist before running this workflow. Run `generate-vc-pitch`, `synthesise-archetypes`, and `build-personas` first.

## Outputs

| Output | Location |
|--------|----------|
| MVP brief | `05-outputs/05-generate-mvp-document/mvp-brief.md` |

## Out of Scope

- Feature specifications or technical architecture
- Implementation roadmaps or sprint planning
- Financial models or investor-ready decks
- Re-running any upstream research workflows

## Acceptance Criteria

1. Includes a problem statement grounded in participant evidence from the VC pitch.
2. Defines scope: what the MVP does and explicitly what it does not do.
3. Identifies the primary target user, drawn from archetypes and personas.
4. Proposes 1–3 experiments, each with a clear learning goal and a measurable signal for success or failure.
5. Lists risks and constraints relevant to building and launching the MVP.
6. Includes a market review covering competitor pricing, market size, and identified gaps in the current landscape.
7. Closes with an opportunity statement: revenue model options, a realistic pricing range, and an order-of-magnitude revenue estimate.

## Workflow

See `02-workflows/generate-mvp-document/` for the detailed process.
