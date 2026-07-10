# Orchestration and review

## Work packet

Use this shape before any OpenCode call:

```text
Goal: <one observable outcome>
Acceptance: <binary checks>
Scope: <1-5 files or one narrow directory>
Authority: read-only | edit only named files
Forbidden: commit, push, deploy, clean, destructive commands, secrets, Codex private paths
Verification: <commands Codex will rerun>
Return: findings/changed files, evidence, tests attempted, assumptions, remaining risks
```

Narrow again if the packet combines implementation, design, copy, risk review, and broad discovery. A timeout during exploration is evidence that the packet is too wide; do not increase timeout before narrowing.

## Review sequence

1. Codex reads the real scope and runs local checks first when possible.
2. OpenCode reviews only named files/diff and returns findings first with exact references.
3. Codex verifies each claim against current files and runtime behavior.
4. Patch only validated findings. Codex runs the regression suite again.
5. Re-review only when the patch changed the risk surface or the first result was incomplete.

`opencode_review` and `opencode_adversarial_review` are bounded reviews, not full security scans. Do not ask them to invoke security-scan skills, threat models, attack-path analysis, validation skills, or subagents. Create a separate user-approved task if that broader work is actually required.

## Multiple sessions

Start more than one OpenCode session only after explicit user approval and only when roles are independent. State each role and scope before dispatch.

- Parallel sessions are read-only by default.
- One working tree has one writer.
- If the user authorizes isolated implementation, use separate worktrees and let Codex integrate.
- OpenCode-native `task`/subagent calls require the same explicit approval; seeing `sawSubagentTask=true` in an unapproved bounded review means the packet widened.
- Do not quote a session whose `outputSummary.resultComplete` is false.

## Bounded implementation

OpenCode may edit only when the user authorized delegation and the packet names exact files. Codex must inspect the diff, reject unrelated changes, and rerun all acceptance checks. OpenCode never performs git publication or deployment.

## Acceptance ledger

For every accepted finding, record:

```text
OpenCode claim:
Current file/runtime evidence:
Codex verdict: accepted | rejected | narrowed
Action and regression test:
```
