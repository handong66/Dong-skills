# Dong-skills

Personal collection of agent collaboration skills.

## Agent collaboration plugins

Use OpenCode, Grok, or Antigravity from Claude Code and Codex for scoped tasks, code review, troubleshooting, and session handoff.

| Target CLI | From Claude Code | From Codex |
| --- | --- | --- |
| OpenCode | [opencode-plugin-cc](https://github.com/handong66/opencode-plugin-cc) | [opencode-plugin-codex](https://github.com/handong66/opencode-plugin-codex) |
| Grok | [grok-plugin-cc](https://github.com/handong66/grok-plugin-cc) | [grok-plugin-codex](https://github.com/handong66/grok-plugin-codex) |
| Antigravity (`agy`) | [agy-plugin-cc](https://github.com/handong66/agy-plugin-cc) | [agy-plugin-codex](https://github.com/handong66/agy-plugin-codex) |

**Plugins connect the tools; skills organize the collaboration.** Dong-skills defines task scope, file ownership, cross-review, and acceptance checks. Its four named workflows cover Claude–Codex mutual review and Codex delegation to OpenCode, Grok, and Antigravity. The six plugins provide three auxiliary tools across two hosts; they are not six separate workflows. The Claude–Codex mutual-review workflow uses a separate third-party plugin.

The Claude Code family traces back to OpenAI's Apache-2.0 [codex-plugin-cc](https://github.com/openai/codex-plugin-cc): the OpenCode port adapts its command surface, the Grok port applies the same approach, and the Antigravity port builds on the OpenCode port. The Codex family uses MCP servers and collaboration skills. The Antigravity plugins run reviews against disposable workspace copies; this separates review work from the source repository, but is not an OS-level sandbox. See each plugin's README and notices for its current behavior, installation, and attribution.

## Skills

- **[claude-codex-collaboration](skills/claude-codex-collaboration/SKILL.md)** — Claude–Codex mutual review with task-assigned roles, explicit writer handoffs, proportionate design gates, and runtime recovery. Either host can implement or verify when assigned and supported.
- **[codex-opencode-collaboration](skills/codex-opencode-collaboration/SKILL.md)** — bounded OpenCode implementation, review, rescue, recoverable sessions, and privacy-safe visible-conversation transfer through the installed plugin.
- **[grok-codex-collaboration](skills/grok-codex-collaboration/SKILL.md)** — bounded Grok work, evidence-backed review, same-session answer recovery, and explicit read-only session boundaries.
- **[agy-codex-collaboration](skills/agy-codex-collaboration/SKILL.md)** — Antigravity collaboration with an explicit choice between disposable-copy reviews and write-capable implementation, rescue, or continuation.

## How collaboration works

1. **Assign the task.** Name the coordinator, implementer, reviewer, and integrator; pin the worktree, change, allowed files, and acceptance criteria. Current user assignments take precedence over defaults.
2. **Hand off writes.** Confirm the previous writer stopped, reconcile the diff, and pass on verified and unverified work before another agent edits. Parallel work needs authorization and independent scopes.
3. **Close the review.** Verify each finding against source or behavior, track open and closed issues, and recheck repairs and affected behavior. Review budgets prevent repeated unchanged rounds; they never turn an unresolved blocker into approval.
4. **Check the evidence.** Distinguish source inspection, static checks, runtime tests, and production observations. For generated or visual artifacts, pin the output and state which page, region, or view was actually inspected.
5. **Recover and deliver.** Use the installed plugin's current completion and recovery contract. The integrator performs authorized Git/release actions and verifies the actual user entry point.

These workflows capture reusable practices from local use. They do not publish private sessions, prescribe fixed model settings, or treat past host limitations as permanent rules. Tool schemas, failure-code tables, and runtime defaults stay with the plugins that implement them.

## Using and maintaining a skill

Copy the complete skill directory into a project's or user-level skills location — for example `.claude/skills/<name>/` or `~/.codex/skills/<name>/`. Preserve `SKILL.md`, `agents/`, and `references/`; each directory is portable without dependencies on sibling skills. The common orchestration and evidence references are intentionally included in each package and should be maintained together.

This repository is the source of truth. Before updating an existing installation, inspect and reconcile its unique changes, preserve a backup, then copy the validated complete directory. Do not overwrite unknown local edits or install missing skills implicitly.

The read-only checker (Python 3.11+) reports SHA-256 hashes and matching, missing, stale, extra, or unsupported entries. It does not follow symlinks, modify files, or synchronize automatically. Pass physical root paths without symlink components:

```sh
python3 scripts/check-installed.py --source skills --installed ~/.codex/skills
python3 scripts/check-installed.py --source skills --installed ~/.claude/skills --skill claude-codex-collaboration
python3 -m unittest discover -s tests
```

Exit status is `0` for an exact match, `1` for differences, and `2` for invalid input or an unreadable tree. Missing installations are informational until you choose to install them; a nonzero check does not authorize changes.
