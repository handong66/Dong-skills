---
name: grok-codex-collaboration
description: "Use when Codex needs to collaborate with Grok through grok-plugin-codex: calling Grok CLI, delegating bounded repo work, requesting review/rescue/adversarial analysis, inspecting Grok sessions, exporting sessions, or managing Grok background jobs while Codex keeps scope, verification, git, and final judgment."
---

# Codex ↔ Grok Collaboration

Use Grok as an independent second-agent surface from inside Codex. Codex remains the owner of the workspace, tests, git state, privacy boundary, and final decision; Grok supplies bounded implementation attempts, review, adversarial review, rescue analysis, or session evidence through the `grok-plugin-codex` MCP tools.

> Prerequisite: the `grok-plugin-codex` Codex plugin is installed and exposes the `grok_*` MCP tools. The current v1 tool surface is `grok_check`, `grok_models`, `grok_run`, `grok_continue`, `grok_rescue`, `grok_review`, `grok_adversarial_review`, `grok_sessions`, `grok_export`, `grok_status`, `grok_result`, and `grok_cancel`. There is no `grok_transfer` tool in v1.

## Start With A Capability Check

1. If the `grok_*` tools are not available in the current Codex session, report that `grok-plugin-codex` is not installed or not loaded. Do not invent Grok results.
2. Run `grok_check` before live delegation, review, or rescue when Grok CLI, login, model availability, or binary discovery may be uncertain.
3. Interpret `grok_check.ok: true` as CLI discovery plus `grok models` success when `includeModels` is not false. Use `includeModels: false` only for a fast CLI/version probe.
4. If Grok is installed outside `PATH`, pass `grokBin` or rely on the plugin discovery order: tool argument, `GROK_BIN`, common Grok install paths, Homebrew paths, then `PATH`.

## Roles

| Responsibility | Codex | Grok |
| --- | --- | --- |
| Scope and packet | Owns task boundaries, file limits, constraints, and acceptance criteria | Challenges gaps and risky assumptions |
| Implementation | May delegate a narrow change, then reads and verifies every diff | Can attempt bounded repo work through `grok_run` |
| Tests and git | Runs local checks, reviews workspace state, commits, pushes, opens PRs | Reports attempts; never gets final say |
| Review | Verifies each finding against actual files before editing | Supplies findings-first review or failure-mode analysis |
| Sessions | Decides when session history is useful and safe | Lists, continues, or exports Grok sessions when explicitly targeted |

## Collaboration Workflow

### 1. Align The Work Packet

Before calling Grok, write a narrow packet:

- Goal and acceptance criteria.
- Exact files, directories, or diff target in scope.
- Constraints: no commits, no pushes, no destructive commands, no secret disclosure, no Codex private runtime paths.
- Whether Grok may edit or must stay read-only.
- Verification commands Codex will run afterward.
- Expected output format: changed files or findings, verification attempted, risks, and assumptions.

Task packet width budget:

- File scope: prefer 1-5 files, one focused directory, or one explicit diff target.
- Role scope: implementation, normal review, adversarial review, rescue diagnosis, session inspection, or export; do not combine all of them.
- Behavior scope: one visible outcome, not "inspect the repo and decide what to do."
- Time scope: if broad discovery is needed, Codex should explore first and pass Grok a narrowed target.

Avoid prompts like:

- "Fix everything."
- "Review the whole repo and tell me what matters."
- "Continue the latest Grok session" without an explicit `sessionId` or `continueLatest: true`.

### 2. Choose The Right Grok Entry

| Need | Use | Notes |
| --- | --- | --- |
| Check environment | `grok_check` | Confirms CLI discovery and, by default, model/login availability. |
| List available models | `grok_models` | Useful before selecting a non-default model. |
| New bounded task | `grok_run` | Use foreground for short tasks, `background: true` for long tasks. |
| Continue known session | `grok_continue` | Use `sessionId` or explicit `continueLatest: true`; never silently continue latest. |
| Stuck Codex task | `grok_rescue` | Ask for read-only diagnosis, minimal path forward, commands to verify, and risks. |
| Normal diff/target review | `grok_review` | Always pass an explicit `target`; the plugin default is `current working tree`, which is broader than a diff. |
| Failure-mode review | `grok_adversarial_review` | Always pass an explicit `target`; at most 5 findings by prompt. |
| Session discovery | `grok_sessions` | Use for Grok session list/search. Search queries are separated from CLI flags. |
| Session export | `grok_export` | Returns Markdown unless `outputFile` is set; `outputFile` must stay inside `cwd`. |
| Background jobs | `grok_status`, `grok_result`, `grok_cancel` | Capture the returned `job.id` and pass it as `jobId` with the same `cwd`. |

### 3. Delegate Implementation Narrowly

Use `grok_run` only for a focused implementation task. Keep the prompt bounded:

```text
Implement only this bounded change.
Scope: <exact files/directories>.
Do not commit, push, deploy, run destructive commands, or modify unrelated files.
Do not read Codex private runtime paths.
Return changed files, verification attempted, risks, and assumptions.
```

After Grok returns, Codex must read the diff, verify it against the task, and run the real project checks before claiming progress. If Grok partially changed files or timed out, inspect the workspace state before deciding whether to continue, patch, or revert only changes made by this run.

### 4. Use Review Tools As Gates, Not Authority

For non-trivial local changes:

1. Run local verification in Codex first when possible.
2. Ask `grok_review` for a bounded findings-first review of an explicit `target`, such as `current diff affecting <files>` or exact named files. Do not rely on the default `current working tree` target.
3. Use `grok_adversarial_review` with an explicit `target` for risky work involving path handling, permissions, auth, cache invalidation, deployment, migrations, or platform assumptions.
4. Verify every Grok finding by reading the actual files. Reject phantom findings explicitly.
5. Patch only validated issues, re-run verification, and re-review when behavior changed materially.

Green tests plus a Grok review still are not final proof; Codex owns the final judgment.

### 5. Handle Background Jobs Conservatively

For long tasks, pass `background: true`, then poll:

```text
grok_run/grok_review/grok_rescue/grok_adversarial_review with background: true
-> capture response.job.id
-> repeat grok_status({ cwd, jobId }) and grok_result({ cwd, jobId }) while outputSummary.state is queued_partial/running_partial
-> accept only grok_result.outputSummary.resultComplete === true
-> grok_cancel({ cwd, jobId }) if the job is stuck or too broad
```

Rules:

- Always pass the same `cwd` to `grok_status`, `grok_result`, and `grok_cancel` that was used to start the job. Job records live under `<cwd>/.grok-plugin-codex/jobs`.
- Record the returned `job.id` from the background start response. Job tools require that value as `jobId`, and valid IDs look like `job_<timestamp>_<8-hex>`.
- Do not treat `grok_status.job.status === "succeeded"` as final. Always call `grok_result` and inspect `grok_result.outputSummary.resultComplete`.
- Treat `grok_result.outputSummary.resultComplete === true` as required before quoting Grok as finished.
- Treat `grok_result.outputSummary.state` values `queued_partial`, `running_partial`, `cancelled_partial`, `failed_partial`, and `succeeded_without_text` as process evidence only. `succeeded_with_text` plus `resultComplete === true` is the usable final-output path.
- Do not report only `grok_result.outputSummary.textPreview` as Grok's full answer; it is a short preview. Use `grok_result.stdout` text events for the full answer, increasing `maxChars` if the returned tail is too small.
- If a background run stalls during broad exploration, narrow the packet before increasing timeout.

### 6. Continue, List, And Export Sessions Deliberately

- Use `grok_continue` with a known `sessionId` or explicit `continueLatest: true`. The plugin intentionally rejects implicit latest-session continuation.
- Use `grok_sessions` when the user asks to inspect Grok history or when you need a session ID.
- Use `grok_export` when the user asks for a session export or when a prior Grok session is evidence. Keep `outputFile` inside `cwd`.
- Do not claim a Codex-to-Grok thread transfer path exists. `grok_transfer` is not part of v1.

## Safety Rules

- Do not expose Codex hidden context, system/developer messages, tool outputs, hidden reasoning, secrets, auth tokens, or private runtime paths.
- Do not ask Grok to read `~/.codex` or similar Codex private runtime paths unless the user explicitly authorizes that risk and `allowCodexPrivatePaths: true` is intentionally set.
- Do not paste secrets or private tool output into `prompt`, `problem`, or `target`; the plugin cannot redact arbitrary user-provided text.
- Pass `cwd` whenever Grok should inspect a workspace. Without `cwd`, Grok may run from the installed plugin directory instead of the user's active repo.
- Use `disableWebSearch: true` and `noSubagents: true` for tightly bounded smoke checks or reviews unless web/search/subagent behavior is explicitly useful.
- Do not pass `alwaysApprove` unless the user explicitly asks for that permission behavior and the blast radius is understood.
- Use very low `maxTurns` values only for sentinel checks. Repo reviews and rescue analysis need enough turns to inspect files and produce a final answer.
- Do not rely on `reasoningEffort` with the known local default `grok-composer-2.5-fast`; the plugin warns and does not pass that flag for unsupported/default cases.

## Install/Setup Fallback

If the plugin is missing, use the repository README as the source of truth. The expected local setup shape is:

```bash
git clone https://github.com/handong66/grok-plugin-codex.git
cd grok-plugin-codex
npm install
npm run check
codex plugin marketplace add .
codex plugin add grok-plugin-codex --marketplace grok-plugin-codex
```

Then start a new Codex thread so the `grok_*` tools and plugin-provided `grok` skill load.

## Tool Argument Templates

Review only with `grok_review`:

```json
{
  "cwd": "<workspace>",
  "target": "current diff affecting <files>, or exact files/directories: <scope>",
  "disableWebSearch": true,
  "noSubagents": true
}
```

Rescue diagnosis with `grok_rescue`:

```json
{
  "cwd": "<workspace>",
  "problem": "Failure: <failure or blocker>\nScope: <files/logs/commands already checked>\nReturn diagnosis, minimal path forward, commands to verify, and risks.",
  "disableWebSearch": true,
  "noSubagents": true
}
```

Adversarial review with `grok_adversarial_review`:

```json
{
  "cwd": "<workspace>",
  "target": "specific diff/files: <scope>. Focus on hidden breakage paths, bad assumptions, platform/path/permission issues, and missing verification.",
  "disableWebSearch": true,
  "noSubagents": true
}
```

Background run and polling:

```json
{
  "cwd": "<workspace>",
  "prompt": "Bounded task: <one outcome>. Scope: <exact files>. Do not commit, push, deploy, or read Codex private paths.",
  "background": true,
  "disableWebSearch": true,
  "noSubagents": true
}
```

```json
{
  "cwd": "<same workspace>",
  "jobId": "<response.job.id>"
}
```

## Common Mistakes

- Treating Grok output as authoritative without checking real files.
- Forgetting `cwd` and accidentally running Grok in the installed plugin directory.
- Reporting partial background logs as a completed Grok result.
- Trusting `grok_status.job.status` without checking `grok_result.outputSummary.resultComplete`.
- Quoting `outputSummary.textPreview` as if it were Grok's full answer.
- Increasing timeout after a broad exploration stall instead of narrowing the packet.
- Omitting `target` from `grok_review` or `grok_adversarial_review` and accidentally reviewing the whole working tree.
- Asking one Grok run to design, implement, test, review, and audit everything.
- Continuing the latest session implicitly instead of using a known `sessionId` or `continueLatest: true`.
- Claiming transfer/import support that the plugin does not ship.
- Passing `alwaysApprove`, secrets, tool logs, or Codex private paths casually.
