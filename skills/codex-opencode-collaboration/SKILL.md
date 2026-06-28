---
name: codex-opencode-collaboration
description: Use when Codex needs to collaborate with OpenCode on coding work, review a diff with OpenCode, delegate a bounded task to OpenCode, rescue a stuck Codex task, or transfer a visible Codex thread into an OpenCode session.
---

# Codex ↔ OpenCode Collaboration

Use OpenCode as an independent second agent from inside Codex. Codex remains the owner of the workspace, tests, git state, and final judgment; OpenCode supplies implementation attempts, rescue analysis, review, adversarial review, or a continued session when a handoff is useful.

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
| Background job management | `opencode_status`, `opencode_result`, `opencode_cancel` | Use `result` before summarizing OpenCode output. |

### 3. Delegate Implementation Narrowly

Use `opencode_run` for a focused implementation task. Keep the prompt bounded:

```text
Implement Task N from the agreed plan.
Scope: <files/directories>.
Do not commit, push, or run destructive commands.
Return changed files, verification attempted, remaining risks, and any assumptions.
```

After it returns, Codex must read the diff, verify against the plan, and run the real project checks before claiming progress.

### 4. Review Before Completion

For any non-trivial change:

1. Run local verification in Codex first when possible.
2. Ask OpenCode for `opencode_review` on the current diff.
3. For risky work, add `opencode_adversarial_review`.
4. Verify every OpenCode finding by reading the actual code. Reject phantom findings explicitly.
5. Patch only validated issues, re-run verification, and re-review if the patch changed behavior.

Green tests are not enough for high-risk work; a second-agent review is a review gate, not a replacement for Codex ownership.

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
- Calling transfer for a small review when `opencode_review` would be cheaper and safer.
- Forgetting to retrieve background job results before reporting.
- Assuming `opencode_setup` exists; current shipped tools use `opencode_check` for environment diagnostics.
- Passing broad prompts like "fix everything" instead of a bounded work packet.
