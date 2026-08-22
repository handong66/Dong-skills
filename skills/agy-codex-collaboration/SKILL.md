---
name: agy-codex-collaboration
description: Use when Codex needs the Antigravity CLI (agy) as a bounded second agent for repository implementation, isolated review, adversarial review, or rescue diagnosis.
---

# Codex ↔ agy Collaboration

Codex owns scope, workspace state, verification, git, privacy, and final judgment. agy receives one bounded role through `agy-plugin-codex`.

agy is not interchangeable with the other second agents. It has no read-only mode, it cannot see a directory it was not given, and a run that reached nothing still reports success. A workflow written by analogy to opencode or Grok will misread its results.

## Required workflow

1. Confirm the plugin's `agy` skill and `agy_*` tools are loaded. The installed plugin schema is authoritative; never reconstruct a missing tool or parameter from this skill. **Never reach the `agy` CLI through a shell tool.** Everything this workflow relies on — the workspace being checked before a run, a review being isolated, the prompt boundary, the record that makes a run auditable — exists in the plugin, not in the CLI. A shell call has none of it, and it does not fail loudly when it is aimed at nothing.
2. Check capability once per batch when the binary, sign-in, model access, or workspace roots are uncertain. A listed model identifier is not proof of a successful call, and a successful capability check is not proof of a usable workspace.
3. Write one work packet: observable goal, binary acceptance, exact scope, isolation, read/write authority, prohibited actions, Codex verification, and required return shape.
4. Choose one role per call, and decide isolation before choosing — see the table. Read [orchestration.md](references/orchestration.md) for packet width, implementation delegation, review gates, and the acceptance ledger.
5. For background work, keep the returned job identifier and use the plugin's own status, result, and cancel tools. For timeout, restart, partial output, continuation, or conversation evidence, read [recovery-conversations.md](references/recovery-conversations.md).
6. Treat agy as finished only when the plugin's completion predicate is true. Then reread every cited file, inspect every diff, and rerun acceptance checks in Codex. Mark each agy claim `accepted`, `rejected`, or `narrowed`.

## Role selection

| Need | Role | Reaches your repository? |
| --- | --- | --- |
| One authorized, narrow code change | Bounded implementation | **Yes** — write-capable in the workspace; agy has no other mode |
| Findings-first check of the working tree | Isolated review | No — a disposable copy, repository path never disclosed |
| Hidden failure paths in a risk-sensitive target | Isolated adversarial review | No — same isolation; state the threat model when the user has given one |
| A stuck task with evidence already gathered | Rescue diagnosis | **Yes** — deliberately not isolated, because a rescue needs the real tree |

An adversarial review labels each finding against the threat model it was given. A finding outside that model is advisory: never a blocker, never a stop-work, never a reason to hold a merge. Where no threat model was stated, treat context-dependent findings the same way.

Isolation belongs to the run, not to the conversation. Continuing a conversation is a write-capable run wherever it is pointed, so an isolated review is never resumed — if it runs out of budget, run a fresh isolated review with a narrower target.

Do not combine design, implementation, broad discovery, review, and security scanning in one agy call. Rescue is the row most often chosen by mistake: when the goal is an opinion that cannot touch anything, choose isolated review instead. Only a delegated run can be authorized to mention Codex private paths at all; a review or a rescue whose task text names one is refused outright. Restate the task instead of trying to widen the boundary.

## Hard boundaries

- Never send hidden Codex context, system/developer messages, reasoning, credentials, arbitrary tool output, or private runtime paths.
- Do not let agy commit, push, deploy, clean the worktree, rewrite history, or run destructive commands.
- One working tree has one writer. Multiple agy conversations, parallel work, or a rescue running beside an implementation require explicit user approval and independent scopes.
- A partial log, process success, or agy assertion is a lead, not a conclusion. Reject phantom findings explicitly.
- **Success is not evidence that anything was reached.** A run whose workspace never resolved reports success and says nothing on stderr, having inspected none of your files. A run can equally report failure while carrying a substantial answer. Outcome, exit status, and answer are three separate signals, and none of them is the verdict on its own — read the plugin's output summary rather than any single field.
- **Nothing here is a sandbox.** Every agy run has its permission prompts skipped, so no role is confined to the directory it was given — agy is told about that directory, not restricted to it. Isolated review is a filesystem boundary around your repository and nothing wider; describe it that way, and never as proof that agy could not reach anything else.
- **A review that completed no tool call is an opinion, not a review.** It does not count as a passing vote, and absence of findings from a run that was denied access is not evidence of correctness. Take the tool-call count from the plugin's summary rather than counting events yourself; a single call surfaces more than once in the stream.
- Do not claim transfer, import, session-export, read-only-mode, or background capabilities unless the installed plugin advertises them. agy publishes no conversation listing of its own, so a listing of past work can only ever be the plugin's own record of what it started.

## Handoff record

Record the role, whether the run was isolated, the job or conversation identifier when present, the exact target, terminal and completion evidence, the observed model, agy claims, Codex verification, rejected claims, commands actually run, and remaining risks.
