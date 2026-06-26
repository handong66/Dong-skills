---
name: claude-codex-collaboration
description: Use when collaborating with the Codex CLI on a coding milestone — the two-phase Claude↔Codex mutual-review (互评) workflow where Claude designs + verifies and Codex implements. Covers invoking Codex via the codex:codex-rescue agent (visible, auto-notified), the per-milestone review gate, and the operational gotchas that bite.
---

# Claude ↔ Codex Collaboration (互评 / mutual review)

A division of labor between Claude Code and the Codex CLI on real coding work. **Codex writes the code; Claude designs, runs the tests Codex can't, critically reviews, and commits.** It is bidirectional: each side reviews the other until *both models + the test suite* agree. **Green tests ≠ Done** — a review round is mandatory.

> Prerequisite: the `openai-codex` plugin is installed (provides the `codex:codex-rescue` agent and `codex-companion.mjs`). Codex must be authed (`/codex:setup`).

## The Two Phases — design first, code second

**Phase 1 — Design (Claude authors, Codex reviews, iterate to agreement):**
1. Claude writes the spec, then the implementation plan (complete, concrete, TDD-shaped).
2. Codex reviews it in a **fresh thread** (read-only).
3. Claude reconciles: **verify each finding by reading the code/plan**, fix the real ones, re-review in a new fresh thread.
4. Repeat until Codex returns GO (no substantive findings). **Only then start coding.**

**Phase 2 — Implementation (Codex codes, Claude verifies, iterate to agreement):**
1. For each task in the agreed plan, **Codex implements** it (TDD, the actual files) via the agent below.
2. **Claude verifies**: runs `npm test` / `typecheck` / `lint` (Codex's sandbox can't), reads the diff, reviews against the spec/plan + red lines, and **commits per task** when green + reviewed.
3. Findings get fed back to Codex to fix; if Claude edits, Codex reviews Claude's edit.
4. At the milestone end, a **fresh Codex review gate** over the whole diff → reconcile → merge to `main`.

## Roles (do not invert)

| | Codex | Claude |
|---|---|---|
| Phase 1 design | reviews | **authors** spec + plan |
| Phase 2 code | **implements** (writes files) | verifies + reviews + commits |
| Runs npm/vitest | ❌ sandbox can't | ✅ always Claude |
| Final commit | no (Claude commits after green) | ✅ |

## How to invoke Codex — use the agent, not the raw companion

**Always go through the `codex:codex-rescue` subagent via the Agent tool.** It is a thin forwarder to `codex-companion.mjs task` that is **harness-tracked → visible in the Background Tasks panel + auto-notifies on completion**. It **defaults to `--write`** (built for handing coding tasks to Codex).

```
Agent(
  subagent_type: "codex:codex-rescue",
  run_in_background: true,          # visible + auto-notify; no manual polling
  description: "Codex: implement Task N",
  prompt: "--fresh\n<full task: point to the agreed plan task; say what files to write;
           'do NOT run npm/vitest or git commit — Claude verifies + commits'>"
)
```

- **Implementation** → just describe the task (the agent adds `--write`). **Review** → say "read-only review, no edits" so it omits `--write`.
- Put routing flags (`--fresh`, `--resume`, `--model`) in the prompt text; the agent strips them.
- **Do NOT** call `node codex-companion.mjs task --write --background` directly — that detaches from the harness (invisible in Background Tasks, no auto-notify, forces you to hand-roll status-poll watchers). That is the wrong path.

## Red lines / rules that prevent disasters

- **Green tests ≠ Done.** Every milestone passes a Codex review gate before merge.
- **Rechecks use FRESH threads (`--fresh`).** Resumed Codex threads drift and *confabulate* bugs that don't exist.
- **Verify every Codex finding (grep/read the actual code) before adopting it. Never "fix" a phantom bug.** Codex will sometimes prescribe a change that references a non-existent variable or breaks a real invariant — read the code, and if the finding is wrong, **reject it** (and say why). A clarifying comment often closes the reviewer's confusion without the wrong change.
- **Codex can't run `npm`/`vitest`** (sandbox EPERM). So Claude runs all tests/typecheck/lint and does the commits-after-green. Codex may run `npx tsc --noEmit` only.
- **Codex implements per the *agreed* plan.** Don't let Codex start coding before Phase 1 reaches agreement.
- **Calibrate external APIs against the installed version**, don't write from memory — tell Codex to confirm the API in `node_modules/<pkg>/docs` before using it (e.g. an AI SDK major version bump).

## Operational gotchas

- **`service_tier` must be `fast` or `flex`.** If something resets `~/.codex/config.toml` `service_tier = "default"`, Codex **dies at startup** with no useful error (3-line log, status `failed`). Symptom: a task "starts thread" then nothing. Fix: set it back to `fast` and re-check `codex-companion.mjs setup --json` shows `ready: true`. Then retry.
- **Reading a background job's result:** `codex-companion.mjs result <job-id> --json` returns a terse `job.summary`; the **full review text is the final assistant message in the job log** (`~/.claude/plugins/data/codex-inline/state/<ws>/jobs/<job-id>.log`). (Using the Agent tool returns Codex's output directly, so you rarely need this.)
- **Manage tasks** with `codex-companion.mjs status [job-id] --json` / `result <job-id>` / `cancel <job-id>`. (Slash commands: `/codex:status`, `/codex:result`, `/codex:cancel`, `/codex:review`, `/codex:adversarial-review`.)

## Anti-patterns (learned the hard way)

- ❌ Claude implementing when Codex should (roles inverted).
- ❌ Raw `codex-companion task --background` → invisible, needs hand-rolled watchers.
- ❌ Blindly applying a Codex-suggested fix without reading the code (phantom bugs).
- ❌ Coding before the plan reached Claude↔Codex agreement.
- ❌ Calling green tests "Done" without a review round.
