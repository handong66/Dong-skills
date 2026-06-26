# Dong-skills

Personal collection of Claude Code skills.

## Skills

- **[claude-codex-collaboration](skills/claude-codex-collaboration/SKILL.md)** — the two-phase Claude↔Codex mutual-review (互评) workflow: Claude designs + verifies, Codex implements. Covers invoking Codex via the `codex:codex-rescue` agent (visible in Background Tasks, auto-notified), the per-milestone review gate, and the operational gotchas (service_tier, fresh threads, verify-don't-fix-phantom).

## Using a skill

Drop a skill directory into a project's or your user-level skills location (e.g. `.claude/skills/<name>/SKILL.md`), or wire this repo as a plugin marketplace. Each skill is self-contained in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`).
