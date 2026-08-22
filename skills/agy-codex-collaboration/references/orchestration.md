# Orchestration and review

## Work packet

Use this shape before an agy call:

```text
Goal: <one observable outcome>
Acceptance: <binary checks>
Scope: <1-5 files, one narrow directory, or one explicit diff>
Isolation: isolated review | write-capable run | rescue in the real tree
Authority: read-only via isolation | edit only named files
Forbidden: commit, push, deploy, clean, destructive commands, secrets, Codex private paths
Verification: <commands Codex will rerun>
Return: findings or changed files, exact evidence, tests attempted, assumptions, remaining risks
```

`Isolation` is the line this workflow adds. agy has no read-only mode, so read-only is never a setting to request — it is a consequence of choosing the isolated review role, and it is unavailable to implementation and rescue. Decide it before writing the rest of the packet.

Narrow the packet when it contains more than one role. A timeout during broad exploration is evidence that scope is too wide; narrow before increasing the limit.

One shape of the prompt itself is load-bearing: a task description that opens with a slash can be taken as a command rather than as text, so do not begin a packet with a path or a slash. Separately, do not ask for a machine-readable return by describing a format in the prompt and then parsing the answer — the answer text carries trailing metadata that is not part of the answer. Ask for prose, and do the parsing in Codex.

## Bounded implementation

Delegate edits only when the user authorized implementation and the packet names exact files. Every agy run that is not an isolated review is write-capable in the workspace it was given, so the packet's scope is a stated boundary, not an enforced one. agy must not modify unrelated files or publish git state. Afterward Codex:

1. inspects the complete workspace diff;
2. rejects or reverts only changes attributable to the delegation when necessary;
3. checks behavior against acceptance criteria;
4. runs the real project verification;
5. performs any commit, push, or release action itself.

## Review sequence

1. Codex reads the target and runs local checks first when possible.
2. agy reviews only the named target and returns findings first with exact file references.
3. Codex verifies reachability, line references, runtime assumptions, and severity against current files.
4. Codex patches only validated issues and reruns regression checks.
5. Re-review only when the risk surface changed or the prior result was incomplete.

A bounded review is not a full security scan. Create a separately approved task for repo-wide discovery, threat modeling, or multi-agent security work.

## Reading an isolated review

An isolated review is answered against a disposable copy of the working tree, which changes how its findings must be read. The plugin's own skill documents how that copy is built and which warnings it raises; the orchestration consequences are:

- The role needs a real repository and refuses before a job exists when it cannot build the copy. That refusal arrives on the submitting call, not later as a failed job.
- Whatever the repository ignores is absent from the copy. A finding that amounts to "this import does not resolve" or "this file is missing" is an artifact of the copy, not a defect. Verify against the real tree before accepting it.
- A review that reports it fixed something did not. Any write landed in the copy, which is then deleted. Re-run the change as an authorized implementation if it is wanted.
- Read the isolation warnings the plugin returns. One of them reports that the real tree or HEAD moved while an isolated run was in flight, which an isolated run should not have been able to cause — treat that verdict with suspicion and check the repository's status yourself.

## Judging evidence

Weigh a verdict by what the run actually inspected, not by how it is worded. A run that completed no tool call is an opinion; a run that was denied the access it needed cannot support a conclusion that nothing is wrong. Take the counts from the plugin's summary rather than deriving them from the event stream, which reports a single tool call more than once. Prefer a re-run with a narrower target over accepting a confident verdict with no evidence behind it.

## Acceptance ledger

```text
agy claim:
Isolation of the run that produced it:
Current file/runtime evidence:
Codex verdict: accepted | rejected | narrowed
Action and regression test:
```

## Multiple conversations

Start multiple conversations or parallel agy work only after explicit user approval. State one independent role and scope for each. Parallel work defaults to isolated review; never run multiple writers in one working tree, and never run a rescue beside an implementation in the same tree. Concurrency beyond a small number of simultaneous runs, and any concurrency sharing one workspace, is unmeasured — treat it as unsupported rather than as permitted.
