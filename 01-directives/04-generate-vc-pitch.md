# Directive: Analyse by VC Pitch

## Goal

Synthesize interview research into a one-page, evidence-backed VC pitch narrative for a personal AI assistant product, so stakeholders can evaluate fundability from real user needs and market gaps.

## Context

> From `00-brief/strategic-research-brief.md`: Build an AI assistant that people choose to use daily for their personal needs, and develop a compelling product story backed by user insights to secure Series A funding.

This workflow re-synthesizes existing participant evidence into an investor-facing narrative. It builds on extract outputs already generated upstream and frames them through a VC decision lens: market gap, user demand, strategic differentiation, and why this product can win.

## Strategic Success Criteria

The deliverable should help a VC audience quickly understand why this opportunity is investable: where current tools fail, what users concretely need, and how this assistant can earn sustained preference over alternatives. It should support strategic funding conversations, not just summarize research.

## Inputs

| Input | Location |
|-------|----------|
| Strategic research brief | `00-brief/strategic-research-brief.md` |
| Per-participant extracts | `04-process/synthesise-archetypes/extracts/*.md` |

> Participant extracts are produced by the `synthesise-archetypes` workflow. Run that workflow first.

## Outputs

| Output | Location |
|--------|----------|
| VC pitch one-pager | `05-outputs/04-generate-vc-pitch/vc-pitch-one-pager.md` |

## Out of Scope

- Re-analyzing raw transcripts directly
- Re-running quote extraction, validation, or tag consolidation
- Producing implementation plans, delivery roadmaps, or feature specifications
- Producing investor collateral beyond the one-page narrative deliverable

## Acceptance Criteria

1. The deliverable is a concise one-page narrative suitable for rapid VC review.
2. It identifies clear opportunity areas grounded in participant evidence.
3. It defines trust and user expectations in concrete, evidence-backed terms.
4. It articulates differentiated positioning versus existing AI assistants.
5. It presents a coherent user-centered story linking pain, product value, and business opportunity.
6. Core claims are evidence-grounded and traceable to participant patterns.
7. It directly answers why users would choose this assistant over alternatives.

## Workflow

See `02-workflows/generate-vc-pitch/` for the detailed process.
