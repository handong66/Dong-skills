# Dong-skills

Personal collection of agent collaboration skills.

## Skills

- **[claude-codex-collaboration](skills/claude-codex-collaboration/SKILL.md)** — the two-phase Claude↔Codex mutual-review (互评) workflow: Claude designs + verifies, Codex implements. Covers invoking Codex via the `codex:codex-rescue` agent (visible in Background Tasks, auto-notified), the per-milestone review gate, and the operational gotchas (service_tier, fresh threads, verify-don't-fix-phantom).
- **[codex-opencode-collaboration](skills/codex-opencode-collaboration/SKILL.md)** — the source-of-truth Codex↔OpenCode orchestration workflow. The core Skill stays concise; one-level references cover bounded packets, user-approved multi-session work, restart/timeout recovery, result finality, permission boundaries, and privacy-safe transfer. Installed personal copies must be synchronized from this directory after validation and must not evolve independently.
- **[grok-codex-collaboration](skills/grok-codex-collaboration/SKILL.md)** — the source-of-truth Codex↔Grok orchestration policy for bounded implementation, review, adversarial review, rescue, recovery, and verification. Current tool schemas remain owned by `grok-plugin-codex`; installed copies of this skill must be synchronized from this directory and must not evolve independently.

## Using a skill

Copy the complete skill directory into a project's or user-level skills location — for example `.claude/skills/<name>/` or `~/.codex/skills/<name>/`. Preserve `SKILL.md` plus any `agents/` and `references/` files; do not copy only the entrypoint or edit an installed copy independently.
