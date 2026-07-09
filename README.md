# Dong-skills

Personal collection of agent collaboration skills.

## Skills

- **[claude-codex-collaboration](skills/claude-codex-collaboration/SKILL.md)** — the two-phase Claude↔Codex mutual-review (互评) workflow: Claude designs + verifies, Codex implements. Covers invoking Codex via the `codex:codex-rescue` agent (visible in Background Tasks, auto-notified), the per-milestone review gate, and the operational gotchas (service_tier, fresh threads, verify-don't-fix-phantom).
- **[codex-opencode-collaboration](skills/codex-opencode-collaboration/SKILL.md)** — the Codex↔OpenCode workflow for using `opencode-plugin-codex`: check capability with `opencode_check`, delegate bounded tasks with `opencode_run`, transfer visible Codex threads with `opencode_transfer`, and use OpenCode review/adversarial review as a second-agent gate while Codex keeps tests, git, and final verification.
- **[grok-codex-collaboration](skills/grok-codex-collaboration/SKILL.md)** — the Codex↔Grok workflow for using `grok-plugin-codex`: check capability with `grok_check`, delegate bounded work with `grok_run`, use Grok review/rescue/adversarial review as a second-agent surface, and manage Grok sessions/background jobs while Codex keeps scope, privacy, tests, git, and final judgment.

## Using a skill

Copy a skill directory into a project's or your user-level skills location — for example `.claude/skills/<name>/` or the Codex skills directory (`~/.codex/skills/<name>/`). Each skill is self-contained in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`).
