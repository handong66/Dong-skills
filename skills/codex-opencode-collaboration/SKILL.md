---
name: codex-opencode-collaboration
description: Use when Codex needs to collaborate with OpenCode on coding work, review a diff, delegate a bounded task, coordinate multiple OpenCode sessions, rescue a stuck task, or transfer a visible Codex thread into OpenCode.
---

# Codex ↔ OpenCode Collaboration

Use OpenCode as an independent second agent from inside Codex. Codex remains the owner of the workspace, tests, git state, and final judgment; OpenCode supplies implementation attempts, rescue analysis, review, adversarial review, or a continued session when a handoff is useful.

Multiple OpenCode sessions can be treated as pseudo-subagents, but they are independent collaboration sessions, not managed subagents. Codex must orchestrate their roles, keep task packets narrow, and verify every accepted result.

> Prerequisite: the `opencode-plugin-codex` Codex plugin is installed and exposes the `opencode_*` MCP tools. The current tool surface is `opencode_check`, `opencode_run`, `opencode_continue`, `opencode_rescue`, `opencode_review`, `opencode_adversarial_review`, `opencode_transfer`, `opencode_status`, `opencode_result`, and `opencode_cancel`.

## Start With A Capability Check

1. If the `opencode_*` tools are not available in the current Codex session, report that the plugin is not installed or not loaded. Do not invent tool results.
2. Run `opencode_check` before live delegation, review, or transfer when the OpenCode CLI, provider, or model may be missing.
3. Treat model listing as a weak signal: a provider can list a model while the local API key is still unauthorized for real runs.
4. If OpenCode is installed outside `PATH`, pass `opencodeBin` or rely on the plugin discovery order: tool argument, `OPENCODE_BIN`, `~/.opencode/bin/opencode`, Homebrew paths, then `PATH`.

## Roles

| Responsibility | Codex | OpenCode |
| --- | --- | --- |
| Plan and scope | Owns task boundaries, constraints, and acceptance criteria | Challenges gaps or risky assumptions |
| Implementation | May delegate bounded tasks, but verifies every file | Can implement with `opencode_run` |
| Tests and git | Runs tests, typecheck, lint, diff review, commits, pushes | Reports what it attempted; does not get final say |
| Review | Verifies findings against real files before acting | Reviews or adversarially reviews diffs |
| Handoff | Decides when transfer is worth the privacy/context cost | Continues from imported visible transcript |

## Collaboration Workflow

### 1. Align The Work Packet

Write a small, explicit packet before calling OpenCode:

- Goal and acceptance criteria.
- Exact files or directories in scope.
- Constraints: no commits, no pushes, no destructive commands, no secret disclosure.
- Verification commands Codex will run afterward.
- Expected output format: changed files, reasoning summary, test attempts, risks.

#### Task Packet Width Budget

Before `opencode_run`, reduce the packet until it fits:

- File scope: prefer 1-5 files, or one tightly named directory.
- Role scope: implementation, design review, copy review, risk review, or rescue diagnosis; do not combine them.
- Behavior scope: one visible outcome, not "redesign, implement, test, and audit everything."
- Time scope: if it may require broad repository discovery, Codex should explore first and pass OpenCode the narrowed context.

Avoid prompts like:

- "Fix everything."
- "Redesign the page and update tests and check the whole site."
- "Inspect the repo and decide what to do."

If an OpenCode run times out while exploring, first assume the packet was too wide. Narrow scope before increasing timeout.

#### Advisory-First Collaboration

Use advisory sessions before implementation for strategic, visual, UX, copy, or architecture questions. Ask OpenCode to review and recommend only, then let Codex convert accepted advice into a bounded implementation packet.

### 2. Choose The Right OpenCode Entry

| Need | Use | Notes |
| --- | --- | --- |
| Check environment | `opencode_check` | Use before blaming transfer, model, or provider failures. |
| New bounded task | `opencode_run` | Constrain scope; default background jobs should be followed with status/result. |
| Continue known session | `opencode_continue` | Use only when a previous OpenCode session is the right continuity anchor. |
| Stuck Codex task | `opencode_rescue` | Ask for diagnosis, minimal path forward, commands to verify, and risks. |
| Normal diff review | `opencode_review` | Findings first; Codex verifies every finding before editing. |
| High-risk review | `opencode_adversarial_review` | Use for hidden breakage paths, platform assumptions, and edge cases. |
| Full handoff | `opencode_transfer` | Imports visible Codex user/assistant transcript into an OpenCode session. |
| Background job management | `opencode_status`, `opencode_result`, `opencode_cancel` | Use `result` before summarizing OpenCode output; require `outputSummary.resultComplete === true` before treating it as final. |

### 3. Coordinate Multiple OpenCode Sessions

OpenCode sessions may be used as pseudo-subagents when the work benefits from independent perspectives. Give each session one role and a read-only default unless isolated implementation is explicitly needed.

Recommended roles:

- Design reviewer: visual hierarchy, layout, spacing, responsiveness, style fit.
- Copy reviewer: audience fit, clarity, ambiguity, tone, repeated phrases.
- Risk reviewer: hidden breakage paths, accessibility, state management, tests.
- Implementation helper: one bounded code change in exact files.

Single Writer Rule:

- Do not let multiple OpenCode sessions mutate the same working tree at the same time.
- Parallel OpenCode sessions should normally be review-only.
- If multiple sessions must implement in parallel, isolate them in separate git worktrees and merge through Codex.
- Codex is the final integrator and must read diffs before accepting changes.

### 4. Delegate Implementation Narrowly

Use `opencode_run` for a focused implementation task. Keep the prompt bounded:

```text
Implement Task N from the agreed plan.
Scope: <files/directories>.
Do not commit, push, or run destructive commands.
Return changed files, verification attempted, remaining risks, and any assumptions.
```

After it returns, Codex must read the diff, verify against the plan, and run the real project checks before claiming progress.

### 5. Recover From Timeout Or Stalls

When an OpenCode run times out or appears stuck:

1. Read `opencode_result` before summarizing or retrying, and check `outputSummary` first.
2. Classify the stall: exploration too broad, implementation blocked, model/API failure, permission prompt, or long-running command.
3. If `outputSummary.state` is `queued_partial`, `running_partial`, `cancelled_partial`, `failed_partial`, or `succeeded_without_text`, treat stdout/stderr as partial process evidence, not an OpenCode result.
4. If exploration was too broad, cancel or abandon the run and resend a narrower packet with exact files and one role.
5. If implementation partially changed files, inspect the diff before deciding whether to continue, revert your own changes, or take over.
6. If model/API failed, check capability or provider state; do not retry the same prompt blindly.

Timeout retry template:

```text
Previous run timed out during exploration. Retry with no broad repository search.
Use only these files: <files>.
Role: <implementation/design/copy/risk>.
Goal: <one sentence>.
Stop after this single change or review.
Return changed files or findings, verification attempted, and remaining risks.
```

### 6. Review Before Completion

For any non-trivial change:

1. Run local verification in Codex first when possible.
2. Ask OpenCode for `opencode_review` on the current diff.
3. For risky work, add `opencode_adversarial_review`.
4. Verify every OpenCode finding by reading the actual code. Reject phantom findings explicitly.
5. Patch only validated issues, re-run verification, and re-review if the patch changed behavior.

Green tests are not enough for high-risk work; a second-agent review is a review gate, not a replacement for Codex ownership.

### 7. Handle Background Results Conservatively

`opencode_result` can contain OpenCode JSONL tool logs even when no final answer exists. Check `outputSummary` before quoting or acting on OpenCode output:

- `succeeded_with_text`: usable as OpenCode's final answer, after Codex verifies real files.
- `queued_partial`, `running_partial`, `cancelled_partial`, `failed_partial`, `succeeded_without_text`: partial only. Do not describe it as an OpenCode review or implementation result.
- If `sawSubagentTask` is true during a bounded review, treat the prompt as too broad unless the user explicitly approved OpenCode-native subagent work.
- For repeated long-read/low-output runs, cancel and rerun with exact files/diffs plus findings-only output.

## Prompt Templates

Review only:

```text
Review only. Do not edit files.
Scope: <files/directories>.
Role: <design reviewer/copy reviewer/risk reviewer>.
Return findings ordered by severity with exact file references and suggested fix direction.
Ignore unrelated issues.
```

Narrow implementation:

```text
Implement only this bounded change.
Scope: <exact files>.
Do not commit, push, deploy, or modify unrelated files.
Do not redesign adjacent areas.
Return changed files, verification attempted, risks, and assumptions.
```

Pseudo-subagent packet:

```text
You are one advisory OpenCode session, not the final decision maker.
Role: <design/copy/risk>.
Scope: <files>.
Do not edit files.
Return only actionable findings and tradeoffs for Codex to verify.
```

## Transfer Workflow

Use `opencode_transfer` when the user wants OpenCode to continue the current Codex thread or when a fresh OpenCode session needs the visible conversation context.

Before transfer:

- Warn that visible user/assistant transcript text will be imported into OpenCode's local session database.
- Keep the default privacy boundary. The plugin excludes Codex system messages, developer messages, tool outputs, and reasoning by default.
- Do not manually paste secrets, hidden instructions, raw tool logs, or private config into the transfer prompt.
- Consider `maxMessages` when the current thread is long.

After transfer:

- Record the returned `opencodeSessionId`.
- Use `opencode_continue` for follow-up work in that session.
- If `runAfterImport` starts a background continuation, use `opencode_status` and `opencode_result` before summarizing.

## Safety Rules

- Do not use `dangerouslySkipPermissions` unless the user explicitly asks and the blast radius is understood.
- Do not let OpenCode commit, push, deploy, or clean the worktree. Codex handles git after verification.
- Do not accept OpenCode's claims without reading files and running commands yourself.
- Do not transfer hidden Codex context. Transfer is for visible user/assistant content only.
- Do not confuse stale marketplace configuration with an installed plugin. If the tools are unavailable, say so and give the install/setup blocker.
- Do not treat partial OpenCode stdout/stderr as a result. Cancelled, running, failed, or no-final-text background jobs are process evidence only; Codex must either rerun narrowly or verify any intermediate clue locally before using it.

## Install/Setup Fallback

If the plugin is missing, use the repository README as the source of truth. The expected local setup shape is:

```bash
git clone https://github.com/handong66/opencode-plugin-codex.git
cd opencode-plugin-codex
npm install
npm run build
codex plugin marketplace add /path/to/opencode-plugin-codex
```

Then install `opencode-plugin-codex` from that marketplace in Codex and start a new Codex session so the `opencode_*` tools load.

## Common Mistakes

- Treating OpenCode output as authoritative without verifying real files.
- Treating OpenCode as another full Codex instance and feeding it an oversized task packet.
- Letting multiple OpenCode sessions write to the same working tree.
- Increasing timeout after an exploration stall instead of narrowing the prompt.
- Asking one session to handle product judgment, UI design, code implementation, tests, and copy review at once.
- Starting multiple sessions without assigning distinct roles.
- Calling transfer for a small review when `opencode_review` would be cheaper and safer.
- Forgetting to retrieve background job results before reporting.
- Reporting cancelled/running tool logs as if OpenCode completed the review.
- Sending broad documentation or repository-wide prompts through `opencode_run` when a bounded `opencode_review` target would force better convergence.
- Assuming `opencode_setup` exists; current shipped tools use `opencode_check` for environment diagnostics.
- Passing broad prompts like "fix everything" instead of a bounded work packet.
