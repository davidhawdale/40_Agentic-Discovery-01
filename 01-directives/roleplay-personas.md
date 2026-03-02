# Directive: Roleplay Personas

## Goal

Build a deterministic role-play pack from the five Dynamic Personas, then launch a local web app so teams can ask questions and receive grounded in-character responses from all five personas simultaneously.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

With personas created, this workflow makes them interactive. Teams can use the role-play app to pressure-test ideas, explore reactions, and surface realistic objections — all grounded in real transcript evidence.

## Inputs

| Input | Location |
|-------|----------|
| Persona files | `04-process/build-dynamic-personas/p6-create-personas/personas/*.md` |
| Archetype input packs | `04-process/build-dynamic-personas/p6-create-personas/persona-inputs/archetype-*.json` |
| Consolidated quotes | `04-process/build-dynamic-personas/p4-consolidate-tags/consolidated-quotes.csv` |
| Contradictions | `04-process/build-dynamic-personas/p3-check-contradictions/contradictions.csv` |
| Product vision | `00-brief/product-vision.md` |
| Research brief | `03-inputs/research-brief.md` |

> Persona files are produced by the `build-personas` workflow. Quotes and contradictions come from `extract-and-tag-quotes`. Run those workflows first.

## Outputs

| Output | Location |
|--------|----------|
| Role-play session pack | `05-outputs/roleplay-personas/session-pack.json` |
| Session runbook | `05-outputs/roleplay-personas/session-runbook.md` |

## Workflow

`02-workflows/roleplay-personas/`

## Success Criteria

- Session pack contains exactly 5 personas with evidence references and contradiction metadata
- App starts successfully and responds to panel questions
- Every model response passes verifier validation before being returned to the user
- Teams can run grounded panel sessions with realistic, differentiated persona voices
