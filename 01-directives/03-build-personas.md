# Directive: Build Personas

## Goal

Produce five fully formed Dynamic Persona profiles, one per archetype, grounded in transcript evidence and suitable for product and experience teams to evaluate ideas against realistic user needs and behaviours.

## Context

> From `00-brief/product-vision.md`: An AI assistant that people choose to use daily for their personal needs — not because they have to, but because it consistently delivers value, earns their trust, and fits seamlessly into their lives.

With archetypes defined, this workflow turns each archetype into a human-centered persona with a clear identity, motivations, behaviours, pain points, and evidence-backed voice. The persona set is used to pressure-test concepts, messaging, and prioritisation decisions.

## Strategic Success Criteria

The persona set should help teams make better product decisions by representing a meaningful spread of user realities and linking those realities to the project vision in `00-brief/`. Personas should be usable as decision-making tools, not just descriptive profiles.

## Inputs

| Input | Location |
|-------|----------|
| Archetype profiles | `04-process/synthesise-archetypes/archetypes.md` |
| Per-participant extracts | `04-process/synthesise-archetypes/extracts/*.md` |
| Participant assignments | `04-process/synthesise-archetypes/participant-archetype-assignments.csv` |
| Persona template | `10-resources/templates/persona-template.md` |

> These are produced by the `synthesise-archetypes` workflow. Run that workflow first.

## Outputs

The outputs produced: five final persona documents for the archetype set (for example, files under `05-outputs/03-build-personas/personas/`).

## Out of Scope

- Redefining or re-clustering archetypes
- Translating transcripts or generating new source extracts
- Changing the core persona template structure
- Producing implementation plans, feature specs, or solution designs

## Acceptance Criteria

1. Five persona profiles are produced, one per archetype.
2. Each persona is clearly grounded in source evidence and reflects its assigned archetype.
3. The persona set is diverse enough to represent materially different user profiles and needs.
4. Outputs are suitable for downstream product discussion and decision-making.
5. The deliverables are saved to the expected final output location for this workflow.

## Workflow

See `02-workflows/build-personas/` for the detailed process.
