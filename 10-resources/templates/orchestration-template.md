# {Workflow Name}

> **{Directive workflow | Utility workflow}** — {For directive: "triggered by user request. See `01-directives/{name}.md` for goal, inputs, and acceptance criteria." | For utility: "called as a prerequisite by other workflows. Can also be run standalone if needed."}
>
> This template is normative. Orchestration files should follow it exactly unless a workflow-specific exception is documented inline.

## Section Requirements

| Section | Requirement |
|---|---|
| `## Approach` | Required |
| `## Preconditions` | Required |
| `## Process` | Required |
| `## Acceptance Criteria Traceability (Directive -> Checks)` | Required for directive workflows |
| `## Retry Policy` | Required |
| `## Tools` | Required |
| `## Manifest Format` | Conditional: include content, or explicit line `No workflow manifest used.` |
| `## Sub-agent Parameters` | Conditional: include content, or explicit line `No dedicated sub-agent calls.` |
| `## Output Promotion` | Required |
| `## Completion Checklist (Run-End Acceptance Gate)` | Required |
| `## Learnings` | Required |

## Approach

{One or two sentences describing the method — how this workflow accomplishes its goal. For utility workflows that have no directive, also state the goal here.}

## Preconditions

- Required inputs:
  - `{path}` — {what must exist}
- Expected counts/shape:
  - `{e.g., N transcripts, one manifest row per transcript}`
- Stop conditions:
  - `{what causes immediate stop before Phase 0}`

## Process

Use phase blocks in this format:

### Phase {N}: {Name}

- Goal: {What this phase must achieve}
- Run: `{command}` or `{agent-name}`
- Paths: {Optional but recommended for Phase 0. List the key folders/files used in this phase.}
- Input: {Key inputs or manifest fields}
- Output: {Expected artifact/report}
- PASS when: {Concrete success condition}
- WARN when: {Condition that allows continue}
- FAIL when: {Condition that blocks or requires retry}
- If fail: {Recovery action}

Rules:
- Every phase must include `PASS when`, `WARN when`, `FAIL when`, and `If fail`.
- Keep command flow in one canonical place (`Run`) and avoid duplicating the same sequence elsewhere.

If a phase has branching outcomes, include a compact decision table:
- `{check} PASS` -> {next step}
- `{check} WARN` -> {log + continue}
- `{check} FAIL` -> {retry/fallback}

{Optional: ## Output Naming — include only if patterns are not obvious; prefer one pattern line over multiple examples.}

{Optional: workflow-specific context sections (e.g., "Language Detection") — include only if the process steps need reference material to make sense.}

### Human Review Gate (Use when required)

**Always stop here. Do not continue without explicit user confirmation.**

- Trigger: {When this gate runs}
- Read: `{path(s)}`
- Summarise:
  - `{count/status field 1}`
  - `{count/status field 2}`
- Ask user:
  - `{proceed/re-run prompt text}`
- Stop rule:
  - `Do not proceed until user explicitly confirms.`

## Acceptance Criteria Traceability (Directive -> Checks)

Use this section for directive workflows to map each directive acceptance criterion to concrete workflow checks.

| Directive Acceptance Criterion | Where Enforced in Workflow | Enforcement Mechanism |
|---|---|---|
| {Criterion from `01-directives/{name}.md`} | {Phase N + command/agent} | {How PASS/FAIL is determined} |
| {Criterion from `01-directives/{name}.md`} | {Phase N + command/agent} | {How PASS/FAIL is determined} |

Rules:
- Include one row per directive acceptance criterion.
- Reference exact phase labels and exact script/agent names.
- Keep mechanism text concrete and testable.
- Do not restate directive wording only; show enforcement linkage.

## Retry Policy

- `WARN`: Log and continue.
- `FAIL` (first): Re-run once with specific correction.
- `FAIL` (second): Stop and report failure context for human decision.

## Tools

- `02-workflows/{name}/{script}.py` — {what it does}
- `{agent-name}` sub-agent — {what it does}

{Group by category if there are prerequisite tools from other workflows.}

{Avoid a separate "Prerequisites" section if Phase 0 already contains prerequisite checks and fallback actions.}

## Manifest Format

{What the prep script outputs. List JSON keys and structure only; avoid repeating concrete path values already defined in phase path bullets or final-phase output details.}

Or, if not applicable:
- `No workflow manifest used.`

## Sub-agent Parameters

{For each sub-agent, list the parameters and where each value comes from in the manifest. Group by agent name.}

Or, if not applicable:
- `No dedicated sub-agent calls.`

## Output Promotion

- Process artifacts stay in `04-process/{name}/`.
- Final deliverables are copied/promoted to `05-outputs/{name}/`.
- Do not overwrite existing `05-outputs` deliverables without explicit user confirmation.

### Final Step: Copy Outputs

After the user confirms the final workflow phase is complete and satisfactory, copy final deliverables to `05-outputs/{name}/` and confirm files are present before reporting completion.

## Completion Checklist (Run-End Acceptance Gate)

- [ ] Preconditions satisfied (or explicitly resolved)
- [ ] All directive acceptance criteria are mapped in traceability table
- [ ] All mapped checks reached required PASS/WARN state
- [ ] Final deliverables exist at expected `05-outputs/{name}/` paths
- [ ] User-facing summary includes counts, issues, and final status
- [ ] Run log entry appended (if workflow logging is enabled)

## Learnings

{Starts empty. Updated as the workflow is used. Record API constraints, edge cases, translation quirks, timing expectations, or anything that would help next time. Date each entry.}
