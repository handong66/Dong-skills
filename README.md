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

- **[claude-codex-collaboration](skills/claude-codex-collaboration/SKILL.md)** — the two-phase Claude↔Codex mutual-review (互评) workflow: Claude designs + verifies, Codex implements. Covers invoking Codex via the `codex:codex-rescue` agent (visible in Background Tasks, auto-notified), the per-milestone review gate, and the operational gotchas (service_tier, fresh threads, verify-don't-fix-phantom).
- **[codex-opencode-collaboration](skills/codex-opencode-collaboration/SKILL.md)** — the source-of-truth Codex↔OpenCode orchestration workflow. The core Skill stays concise; one-level references cover bounded packets, user-approved multi-session work, restart/timeout recovery, result finality, permission boundaries, and privacy-safe transfer. Installed personal copies must be synchronized from this directory after validation and must not evolve independently.
- **[grok-codex-collaboration](skills/grok-codex-collaboration/SKILL.md)** — the source-of-truth Codex↔Grok orchestration policy for bounded implementation, review, adversarial review, rescue, recovery, and verification. Current tool schemas remain owned by `grok-plugin-codex`; installed copies of this skill must be synchronized from this directory and must not evolve independently.
- **[agy-codex-collaboration](skills/agy-codex-collaboration/SKILL.md)** — the source-of-truth Codex↔agy orchestration policy for the Antigravity CLI. agy has no read-only mode, cannot see a directory it was not given, and reports its own outcome independently of its exit code, so this skill makes isolation an explicit line in the work packet and separates the roles that reach the real tree from the ones that cannot. Current tool schemas remain owned by `agy-plugin-codex`; installed copies of this skill must be synchronized from this directory and must not evolve independently.

## Using a skill

Copy the complete skill directory into a project's or user-level skills location — for example `.claude/skills/<name>/` or `~/.codex/skills/<name>/`. Preserve `SKILL.md` plus any `agents/` and `references/` files; do not copy only the entrypoint or edit an installed copy independently.
