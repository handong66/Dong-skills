---
name: claude-codex-collaboration
description: Use when collaborating with the Codex CLI on a coding milestone — the two-phase Claude↔Codex mutual-review (互评) workflow where Claude designs + verifies and Codex implements. Covers invoking Codex via the codex:codex-rescue agent (visible, auto-notified), the per-milestone review gate, and the operational gotchas that bite.
---

# Claude ↔ Codex Collaboration (互评 / mutual review)

A division of labor between Claude Code and the Codex CLI on real coding work. **Codex writes the code; Claude designs, runs the tests Codex can't, critically reviews, and commits.** It is bidirectional: each side reviews the other until *both models + the test suite* agree. **Green tests ≠ Done** — a review round is mandatory.

> Prerequisite: the `openai-codex` plugin is installed (provides the `codex:codex-rescue` agent and `codex-companion.mjs` — for direct calls the script lives at `~/.claude/plugins/cache/openai-codex/codex/<version>/scripts/codex-companion.mjs`). Codex must be authed (`/codex:setup`).

## The Two Phases — design first, code second

**Phase 1 — Design (Claude authors, Codex reviews, iterate to agreement):**
1. Claude writes the spec, then the implementation plan (complete, concrete, TDD-shaped).
2. Codex reviews it in a **fresh thread** (read-only).
3. Claude reconciles: **verify each finding by reading the code/plan**, fix the real ones, re-review in a new fresh thread.
4. Repeat until Codex returns GO (no substantive findings). **Only then start coding.**

> Spec reviews converge on the gap between **intent and acceptance gate**: expect NO-GO rounds whose findings are "the gate passes while the intent fails" (a keyword grep that only covers one language; a keyword check that doesn't bind the content to the field that actually renders). Write gates that bind required content to its **location and shape**, not to keyword presence — in one field session 3 of 5 spec findings were exactly this class.

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
- Put routing flags (`--fresh`, `--resume`) in the prompt text; the agent strips them and applies the routing. Do **not** rely on prompt text for `--model`/`--effort` — forwarding them is not guaranteed (see Operational gotchas).
- **Do NOT** call `node codex-companion.mjs task --write --background` directly as the default path — that detaches from the harness (invisible in Background Tasks, no auto-notify, forces you to hand-roll status-poll watchers). The only exceptions are the two documented fallbacks in Operational gotchas (wrapper died mid-forward; `--model`/`--effort` must land).

## Red lines / rules that prevent disasters

- **Green tests ≠ Done.** Every milestone passes a Codex review gate before merge.
- **Rechecks use FRESH threads (`--fresh`).** Resumed Codex threads drift and *confabulate* bugs that don't exist.
- **Verify every Codex finding (grep/read the actual code) before adopting it. Never "fix" a phantom bug.** Codex will sometimes prescribe a change that references a non-existent variable or breaks a real invariant — read the code, and if the finding is wrong, **reject it** (and say why). A clarifying comment often closes the reviewer's confusion without the wrong change.
- **Codex can't run `npm`/`vitest`** (sandbox EPERM). So Claude runs all tests/typecheck/lint and does the commits-after-green. Codex may run `npx tsc --noEmit` only.
- **Codex implements per the *agreed* plan.** Don't let Codex start coding before Phase 1 reaches agreement.
- **Calibrate external APIs against the installed version**, don't write from memory — tell Codex to confirm the API in `node_modules/<pkg>/docs` before using it (e.g. an AI SDK major version bump).

## Operational gotchas

- **`service_tier` must be `fast` or `flex`.** If something resets `~/.codex/config.toml` `service_tier = "default"`, Codex **dies at startup** with no useful error (3-line log, status `failed`). Symptom: a task "starts thread" then nothing. Fix: set it back to `fast` and re-check `codex-companion.mjs setup --json` shows `ready: true`. Then retry.
- **Reading a background job's result:** `codex-companion.mjs result <job-id> --json` returns a terse `job.summary`; the **full review text is the final assistant message in the job log** (`~/.claude/plugins/data/codex-inline/state/<ws>/jobs/<job-id>.log`). (The Agent tool returns Codex's output directly only when the job finishes inside the wrapper's foreground window — see the next gotcha; `result <job-id>` without `--json` also prints the full text.)
- **The wrapper regularly hands back only a job id — that is a normal outcome, not a failure.** The wrapper self-reports a "120s foreground window": a run that outlives it gets auto-moved to background and the wrapper returns "started as `<job-id>`" — sometimes phrased as if it will report back later. **It won't**: the wrapper exits, and no later notification carries the result. Poll `status <job-id> --json` until `completed`/`failed`/`cancelled`, then `result <job-id>`. In one field session 3 of 5 wrapper calls behaved this way (and the inline-result cases included runs over 2 minutes, so the cutoff is not strict wall-time) — treat the inline result as a convenience you cannot rely on, and always capture the job id.
- **Manage tasks** with `codex-companion.mjs status [job-id] --json` / `result <job-id>` / `cancel <job-id>`. (Slash commands: `/codex:status`, `/codex:result`, `/codex:cancel`, `/codex:review`, `/codex:adversarial-review`.)
- **`--model` / `--effort` are not reliably forwarded by the `codex:codex-rescue` wrapper.** The wrapper's contract is to convert an explicit model/effort request into companion arguments, but it is an LLM forwarder — it can strip the flags from the prompt text **without** converting them, and the job then silently runs on the `~/.codex/config.toml` defaults. When a specific model matters, call the companion directly: `codex-companion.mjs task "<prompt>" --background --model <m> --effort <e>`, then **verify it took effect**. The companion does **not** persist model/effort (`status <job-id> --json` has no such fields) — read it back from the Codex session rollout instead: take the thread id from the job log's "Thread ready (<id>)" line, then check `session_meta` in `~/.codex/sessions/<Y>/<M>/<D>/rollout-*-<thread-id>.jsonl` (`model`/`effort`; `null` = config default — a dropped flag shows up as `model: null`). Never assume a flag landed without reading it back.
- **The wrapper agent can die before submitting the job** (e.g. it hits the host Claude session limit mid-forward). Symptom: the wrapper reports failure or success-with-no-job, and `status --json` shows `running: []` with no new job id. That means nothing was submitted — don't wait; submit directly via the companion and poll yourself (a background loop over `status <job-id> --json` until `completed`/`failed`/`cancelled`, then `result <job-id>`).
- **A red Codex-written guard can be wrong in *shape* while the content is right.** Field case: the spec required a sentence at the end of an existing trilingual `summary` value; Codex's new guard asserted the sentence as the entire line (`toContain('en: "<sentence>"')`) and failed against spec-correct content. When a guard Codex just wrote goes red, diagnose against the spec's *placement* before touching content — fix the assertion's shape (`toMatch(/en: ".*<sentence>"/)`) rather than moving the content, and have the milestone review explicitly confirm the edit did not loosen the guard (Phase 2 rule 3: Codex reviews Claude's edit).
- **Files outside the companion's `workspaceRoot` are Claude's to implement.** Codex writes only inside the workspace it was launched for; a task touching another repo (e.g. a GitHub profile README) inverts no roles when Claude implements it — hand the resulting diff to the milestone review as pasted text. And verify findings on pasted-diff text against the real file like any other: a GO verdict once carried a LOW claiming a missing apostrophe ("Googles") that existed correctly in both the pasted diff and the file. Phantom findings occur at every severity and in every input mode.
- **Upgrading the Codex CLI via npm does not fix a running session.** The companion uses a shared runtime (`app-server-broker.mjs serve` + a resident `codex app-server` child); after `npm i -g @openai/codex@latest` those processes still run the **old binary from memory**, so the original error reproduces byte-for-byte (e.g. "model X requires a newer version of Codex"). Fix: kill the broker and its app-server children (match `app-server-broker|<npm-prefix>.*codex` — carefully avoid ChatGPT.app's own Codex processes), let the next companion call respawn them, then smoke-test with `codex exec --sandbox read-only "Reply with exactly: OK"`.

## Anti-patterns (learned the hard way)

- ❌ Claude implementing when Codex should (roles inverted).
- ❌ Raw `codex-companion task --background` as the default path → invisible, needs hand-rolled watchers. (It becomes the legitimate fallback when the wrapper can't be used — wrapper hit the host session limit, or the run needs `--model`/`--effort` forwarded; see Operational gotchas.)
- ❌ Blindly applying a Codex-suggested fix without reading the code (phantom bugs).
- ❌ Coding before the plan reached Claude↔Codex agreement.
- ❌ Calling green tests "Done" without a review round.
