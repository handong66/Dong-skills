# Orchestration and review

## Work packet

Use this shape before a Grok call:

```text
Goal: <one observable outcome>
Acceptance: <binary checks>
Scope: <1-5 files, one narrow directory, or one explicit diff>
Authority: read-only | edit only named files
Forbidden: commit, push, deploy, clean, destructive commands, secrets, Codex private paths
Verification: <commands Codex will rerun>
Return: findings or changed files, exact evidence, tests attempted, assumptions, remaining risks
```

Narrow the packet when it contains more than one role. A timeout during broad exploration is evidence that scope is too wide; narrow before increasing the limit.

## Bounded implementation

Delegate edits only when the user authorized implementation and the packet names exact files. Grok must not modify unrelated files or publish git state. Afterward Codex:

1. inspects the complete workspace diff;
2. rejects or reverts only changes attributable to the delegation when necessary;
3. checks behavior against acceptance criteria;
4. runs the real project verification;
5. performs any commit, push, or release action itself.

## Review sequence

1. Codex reads the target and runs local checks first when possible.
2. Grok reviews only the named target and returns findings first with exact file references.
3. Codex verifies reachability, line references, runtime assumptions, and severity against current files.
4. Codex patches only validated issues and reruns regression checks.
5. Re-review only when the risk surface changed or the prior result was incomplete.

A bounded review is not a full security scan. Create a separately approved task for repo-wide discovery, threat modeling, or multi-agent security work.

## Acceptance ledger

```text
Grok claim:
Current file/runtime evidence:
Codex verdict: accepted | rejected | narrowed
Action and regression test:
```

## Multiple sessions

Start multiple sessions or Grok-native subagents only after explicit user approval. State one independent role and scope for each. Parallel sessions default to read-only; never run multiple writers in one working tree.
