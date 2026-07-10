---
name: codex-opencode-collaboration
description: Use when Codex needs OpenCode for a bounded coding task, independent review, rescue analysis, adversarial review, session continuation, or visible-thread transfer.
---

# Codex ↔ OpenCode Collaboration

Codex owns scope, workspace state, verification, git, and final judgment. OpenCode is a bounded second agent. Plugin source and tests are authoritative for tool behavior; this Skill defines orchestration.

## Required workflow

1. Confirm the `opencode_*` tools are loaded. Run `opencode_check` when CLI/provider/model availability is uncertain. A listed model is not proof of authorization.
2. Write a bounded packet: goal, acceptance criteria, exact files, read/write authority, prohibited actions, verification, and output shape.
3. Obtain explicit user approval before starting multiple OpenCode sessions, OpenCode-native subagents, or parallel work. Parallel sessions default to read-only.
4. Choose one tool and keep one role per call. See [orchestration.md](references/orchestration.md) for packets, width limits, reviews, and multi-session rules.
5. For background work, keep the returned `jobId`; call `opencode_status`/`opencode_result`/`opencode_cancel` without `cwd`.
6. Treat OpenCode as finished only when `outputSummary.resultComplete === true`. Then reread every cited file and rerun relevant commands in Codex.

## Tool selection

| Need | Tool |
| --- | --- |
| Capability diagnosis | `opencode_check` |
| New bounded task | `opencode_run` |
| Known OpenCode session | `opencode_continue` |
| Stuck-task diagnosis | `opencode_rescue` |
| Normal second review | `opencode_review` |
| Failure-mode review | `opencode_adversarial_review` |
| Visible conversation handoff | `opencode_transfer` |
| Background lifecycle | `opencode_status`, `opencode_result`, `opencode_cancel` |

Read [recovery-transfer.md](references/recovery-transfer.md) before recovering a timeout/restart, interpreting partial or truncated output, changing permission/path boundaries, or transferring a Codex task.

## Hard boundaries

- Do not let OpenCode commit, push, deploy, clean the worktree, rewrite history, or read secrets/private Codex runtime paths.
- Do not run multiple writers against one working tree. Isolation does not remove Codex's review obligation.
- Put instructions in `prompt`; attach only in-workspace regular files through `files`. Do not pass executable paths; configure trusted `OPENCODE_BIN` in the MCP environment.
- `autoApprovePermissions` maps to OpenCode `--auto`; it does not bypass explicit denies or the Codex-private-path guard. Private-path access requires separate explicit authorization.
- Transfer only visible user/assistant text. Never paste system/developer messages, reasoning, tool outputs, credentials, or private runtime files.
- A partial log or OpenCode claim is a lead, not a conclusion. Reject phantom findings explicitly.

## Handoff record

Record the tool, job/session ID, exact scope, terminal state, whether `resultComplete` was true, OpenCode findings, Codex verification, rejected findings, remaining risks, and commands actually run.
