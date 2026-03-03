# Directive: Roleplay Personas

## Goal

Create a role-play persona pack from the Dynamic Personas so teams can run grounded multi-persona sessions that surface realistic reactions, objections, and priorities for product decisions.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

With personas created, this workflow makes them interactive and usable in collaborative decision-making contexts. Teams use these sessions to pressure-test ideas, explore trade-offs, and identify likely user responses while staying anchored to interview evidence.

## Strategic Success Criteria

This workflow should help teams evaluate concepts against realistic user perspectives, not abstract assumptions. Outputs should make persona evidence easy to apply in live discussion and support better product choices aligned with the project vision.

## Inputs

| Input | Location |
|-------|----------|
| Persona files | `05-outputs/build-personas/personas/*.md` |
| Archetype input packs | `04-process/build-personas/persona-inputs/archetype-*.json` |
| Consolidated quotes | `04-process/extract-and-tag-quotes/p4-consolidate-tags/consolidated-quotes.csv` |
| Contradictions | `04-process/extract-and-tag-quotes/p3-check-contradictions/contradictions.csv` |
| Product vision | `00-brief/product-vision.md` |
| Research brief | `03-inputs/research-brief.md` |

> Persona files are produced by the `build-personas` workflow. Quotes and contradictions come from `extract-and-tag-quotes`. Run those workflows first.

## Outputs

| Output | Location |
|--------|----------|
| Role-play session pack | `05-outputs/roleplay-personas/session-pack.json` |
| Session runbook | `05-outputs/roleplay-personas/session-runbook.md` |

## Out of Scope

- Creating new personas or redefining archetypes
- Re-running quote extraction or contradiction analysis
- Producing product-roadmap decisions or prioritisation outputs directly
- Replacing human judgement with automated recommendations

## Acceptance Criteria

1. A complete session pack is produced for the five-persona panel.
2. Persona responses are grounded in the underlying research evidence base.
3. Persona voices are meaningfully differentiated and suitable for panel-style discussion.
4. The runbook provides clear guidance for teams to run repeatable role-play sessions.
5. Outputs are usable for downstream concept evaluation and product conversation.

## Workflow

See `02-workflows/roleplay-personas/` for the detailed process.
