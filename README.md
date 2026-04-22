# Agentic Discovery — Personal AI Assistant

This project transforms 52 qualitative interview transcripts into interactive research artefacts for a personal AI assistant product. It runs a chain of AI workflows that progressively distil raw interview data into actionable discovery outputs.

## What it does

Starting from interview transcripts, seven workflows run in sequence:

| # | Workflow | What it produces |
|---|----------|-----------------|
| 01 | **Extract and tag quotes** | Tagged, validated quotes and contradiction flags from all transcripts |
| 02 | **Synthesise archetypes** | Five behavioural archetypes grounded in the quote data |
| 03 | **Build personas** | Five named, conversational Dynamic Personas backed by transcript evidence |
| 04 | **Generate MVP document** | A product brief for the AI assistant, built from persona and market research |
| 05 | **Generate VC pitch** | A one-page investor pitch synthesised from the research |
| 06 | **Assess MVP by Three Amigos** | A structured review of the MVP brief from UX, PM, and engineering lenses |
| 07 | **Run focus group** | A simulated focus group session where the personas respond to product concepts |

The personas are the core deliverable — they are designed to be queried conversationally so teams can "talk to the research" during ideation, rather than reading static documents.

## How to use it

Run workflows in Claude Code using `/run-workflow <workflow-name>`. To talk to a persona, ask Claude to load it from `05-outputs/03-build-personas/personas/`.

## Project structure

```
00-brief/       Project goals and research context
01-directives/  One file per workflow — what to do and why
02-workflows/   Orchestration files and Python scripts for each workflow
03-inputs/      Raw interview transcripts (read-only)
04-process/     Intermediate files generated during workflow runs
05-outputs/     Final deliverables — personas, MVP brief, VC pitch, assessments
```
