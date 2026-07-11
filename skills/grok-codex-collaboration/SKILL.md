---
name: grok-codex-collaboration
description: Use when Codex needs Grok as a bounded second agent for repository implementation, independent review, adversarial review, or rescue analysis.
---

# Codex ↔ Grok Collaboration

Codex owns scope, workspace state, verification, git, privacy, and final judgment. Grok receives one bounded role through `grok-plugin-codex`.

## Required workflow

1. Confirm the plugin's `grok` skill and `grok_*` tools are loaded. The installed plugin schema is authoritative; never reconstruct a missing tool or parameter from this skill.
2. Check capability when CLI discovery, authentication, model access, or installed-version compatibility is uncertain. A listed model is not proof of a successful call.
3. Write one work packet: observable goal, binary acceptance, exact scope, read/write authority, prohibited actions, Codex verification, and required return shape.
4. Choose one role per call. Read [orchestration.md](references/orchestration.md) for packet width, implementation delegation, review gates, and the acceptance ledger.
5. For timeout, restart, partial output, continuation, or session evidence, read [recovery-sessions.md](references/recovery-sessions.md) and follow the current plugin completion contract.
6. Reread every cited file, inspect every diff, and rerun acceptance checks in Codex. Mark each Grok claim `accepted`, `rejected`, or `narrowed`.

## Role selection

| Need | Role |
| --- | --- |
| One authorized, narrow code change | Bounded implementation |
| Findings-first check of named files or diff | Independent review |
| Hidden failure paths in a risk-sensitive target | Adversarial review |
| A stuck task with evidence already gathered | Rescue diagnosis |

Do not combine design, implementation, broad discovery, review, and security scanning in one Grok call.

## Hard boundaries

- Never send hidden Codex context, system/developer messages, reasoning, credentials, arbitrary tool output, or private runtime paths.
- Do not let Grok commit, push, deploy, clean the worktree, rewrite history, or run destructive commands.
- One working tree has one writer. Multiple Grok sessions, Grok-native subagents, or parallel work require explicit user approval and independent scopes.
- A partial log, process success, or Grok assertion is a lead, not a conclusion. Reject phantom findings explicitly.
- Do not claim transfer, import, model, permission, or background capabilities unless the installed plugin advertises them.

## Handoff record

Record the role, exact target, job/session identifier when present, terminal and completion evidence, Grok claims, Codex verification, rejected claims, commands actually run, and remaining risks.
