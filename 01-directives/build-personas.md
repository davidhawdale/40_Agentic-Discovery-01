# Directive: Build Personas

## Goal

Produce five fully-formed Dynamic Persona profiles — one per archetype — each grounded explicitly in transcript evidence, following the standard persona template, and meeting set-level diversity requirements.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

With archetypes defined, this workflow gives each archetype a human identity: a name, backstory, needs, behaviours, pain points, and verbatim quotes. The five personas are the primary deliverable for teams wanting to pressure-test product ideas.

## Inputs

| Input | Location |
|-------|----------|
| Archetype profiles | `04-process/synthesise-archetypes/archetypes.md` |
| Per-participant extracts | `04-process/synthesise-archetypes/extracts/*.md` |
| Participant assignments | `04-process/synthesise-archetypes/participant-archetype-assignments.csv` |
| Persona template | `10-resources/templates/persona-template.md` |

> These are produced by the `synthesise-archetypes` workflow. Run that workflow first.

## Outputs

| Output | Location |
|--------|----------|
| 5 Dynamic Persona profiles | `05-outputs/build-personas/personas/` |

## Workflow

`02-workflows/build-personas/`

## Success Criteria

- 5 persona files produced, one per archetype
- Each persona follows the standard template headings exactly
- Each persona includes exactly 2 verbatim quotes in the Key Quotes section
- Personas pass structural and diversity validation
- The set covers a range of ages, genders, personality types, pain point severities, and attitudes toward the product
