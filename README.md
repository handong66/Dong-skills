# Dong-skills

Personal collection of agent collaboration skills.

## Working with other coding agents

[Turnweft](https://github.com/handong66/turnweft) lets Claude Code and Codex hand work to Dim, Droid, Grok, OpenCode, and agy in the real project, with sessions you can come back to later.

**Turnweft connects the agents; these skills organize the collaboration.** Dong-skills defines task scope, file ownership, cross-review, and acceptance checks. Its two workflows cover Claude–Codex mutual review and delegation to other coding agents through Turnweft. The Claude–Codex workflow uses a separate third-party plugin.

## Skills

- **[claude-codex-collaboration](skills/claude-codex-collaboration/SKILL.md)** — Claude–Codex mutual review: assign roles for the task, hand off edits explicitly, check each other's work, and pick up an interrupted task. Either host can implement or verify when assigned.
- **[turnweft-collaboration](skills/turnweft-collaboration/SKILL.md)** — hand bounded implementation, review, or diagnosis from Claude Code or Codex to Dim, Droid, Grok, OpenCode, or agy through Turnweft, continue the same agent session, and verify the result before accepting it.

## How collaboration works

1. **Assign the task.** Name the coordinator, implementer, reviewer, and integrator; pin the worktree, change, allowed files, and acceptance criteria. Current user assignments take precedence over defaults.
2. **Hand off writes.** Confirm the previous writer stopped, reconcile the diff, and pass on verified and unverified work before another agent edits. Parallel work needs authorization and independent scopes.
3. **Close the review.** Verify each finding against source or behavior, track open and closed issues, and recheck repairs and affected behavior. Review budgets prevent repeated unchanged rounds; they never turn an unresolved blocker into approval.
4. **Check the evidence.** Distinguish source inspection, static checks, runtime tests, and production observations. For generated or visual artifacts, pin the output and state which page, region, or view was actually inspected.
5. **Pick up and deliver.** Continue an interrupted task through the tool that started it. The integrator handles authorized Git and release steps and checks what users actually see.

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
