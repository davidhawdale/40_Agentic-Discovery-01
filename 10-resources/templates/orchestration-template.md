# {Workflow Name}

> **{Directive workflow | Utility workflow}** — {For directive: "triggered by user request. See `01-directives/{name}.md` for goal, inputs, and acceptance criteria." | For utility: "called as a prerequisite by other workflows. Can also be run standalone if needed."}

## Approach

{One or two sentences describing the method — how this workflow accomplishes its goal. For utility workflows that have no directive, also state the goal here.}

## Process

Use phase blocks in this format:

### Phase {N}: {Name}

- Goal: {What this phase must achieve}
- Run: `{command}` or `{agent-name}`
- Paths: {Optional but recommended for Phase 0. List the key folders/files used in this phase.}
- Input: {Key inputs or manifest fields}
- Output: {Expected artifact/report}
- If fail: {Recovery action}

For the final phase, include output-deliverable details inline:
- Output artifact: `{path-to-final-output}`
- Output format: {Template or structure used}
- Output constraints: {Length/quality constraints, if any}

If a phase has branching outcomes, include a compact decision table:
- `{check} PASS` -> {next step}
- `{check} FAIL` -> {retry/fallback}

{Optional: ## Output Naming — include only if patterns are not obvious; prefer one pattern line over multiple examples.}

{Optional: workflow-specific context sections (e.g., "Language Detection") — include only if the process steps need reference material to make sense.}

## Acceptance Criteria Traceability (Directive -> Checks)

Use this section for directive workflows to map each directive acceptance criterion to concrete workflow checks.

| Directive Acceptance Criterion | Where Enforced in Workflow | Enforcement Mechanism |
|---|---|---|
| {Criterion from `01-directives/{name}.md`} | {Phase N + command/agent} | {How PASS/FAIL is determined} |
| {Criterion from `01-directives/{name}.md`} | {Phase N + command/agent} | {How PASS/FAIL is determined} |

Rules:
- Include one row per directive acceptance criterion.
- Reference exact phase labels and exact script/agent names.
- Keep mechanism text concrete and testable (what causes FAIL/WARN/PASS).
- Do not restate directive wording only; show enforcement linkage.

## Tools

- `02-workflows/{name}/{script}.py` — {what it does}
- `{agent-name}` sub-agent — {what it does}

{Group by category if there are prerequisite tools from other workflows.}

{Avoid a separate "Prerequisites" section if Phase 0 already contains prerequisite checks and fallback actions.}

## Manifest Format

{What the prep script outputs. List JSON keys and structure only; avoid repeating concrete path values already defined in phase path bullets or final-phase output details.}

## Sub-agent Parameters

{For each sub-agent, list the parameters and where each value comes from in the manifest. Group by agent name.}

## Completion Checklist (Run-End Acceptance Gate)

- [ ] {Prepare phase succeeded}
- [ ] {Primary verify step is PASS}
- [ ] {Final output file exists at expected path}
- [ ] {User-facing report includes counts and issues}

## Learnings

{Starts empty. Updated as the workflow is used. Record API constraints, edge cases, translation quirks, timing expectations, or anything that would help next time. Date each entry.}
