# Recovery, result handling, and transfer

## Background lifecycle

`opencode_run` defaults to background mode. `timeoutMs` is enforced by an independent worker, and central private state lets a new MCP process use the original `jobId` after restart. Status/result/cancel do not take `cwd`.

Poll by condition, not fixed optimism:

1. Call `opencode_status` with `jobId`.
2. If queued/running, call `opencode_result` only for partial evidence and poll later.
3. If scope is too wide, cancel and rerun narrowly.
4. If the worker disappeared, expect `failed` with `worker_unavailable`, not an eternal running state.

Only `outputSummary.resultComplete === true` is final. All other states are partial:

- `queued_partial`, `running_partial`: still active.
- `cancelled_partial`: cancellation won; logs may be incomplete.
- `failed_partial`: inspect `errorClass` and stderr/JSONL error evidence.
- `succeeded_without_text`: process exited zero without a terminal stop step containing assistant text.

Output is a bounded tail. `outputTruncated=true` means earlier data was discarded. Never infer absence from a truncated tail.

## Failure routing

- `model_unauthorized`: verify the exact provider/model with a harmless real call; listing is insufficient.
- `network_error`: verify connectivity/provider state before retrying.
- `timeout`: narrow scope before raising the limit.
- `worker_unavailable`: preserve the record and rerun; do not claim OpenCode concluded.
- JSONL `error` events override exit code 0.

## Permission and path boundaries

Use `autoApprovePermissions` only with explicit user approval; it maps to current `--auto` and respects explicit deny rules. `dangerouslySkipPermissions` is a deprecated alias for the same behavior. Neither permits Codex private paths.

Set `allowCodexPrivatePaths` only when the user explicitly authorizes the exact private path and understands exposure. Normal collaboration must inline task-local guidance instead. `cwd`, `files`, and explicit rollout fixtures are realpath-contained; tools do not accept a caller-controlled OpenCode executable.

## Transfer

Use `opencode_transfer` only when the user wants a handoff or the visible conversation materially improves continuity. Before calling it:

- Warn that visible conversation text will be stored in OpenCode's local session database.
- Pass an explicit model proven by a harmless authorized call.
- Prefer the default current-thread lookup; an explicit rollout must be inside the workspace or Codex sessions directory.
- Do not include system/developer messages, reasoning, tool output, credentials, or hidden context.

The parser prefers current visible `event_msg.user_message` and `event_msg.agent_message`; legacy response messages are fallback only. Import succeeds only after OpenCode returns a session ID and the plugin exports that session for readback.

If `runAfterImport` fails, retain `opencodeSessionId`, report `importSucceeded=true`, report overall `ok=false`, and route the continuation error. A background continuation reports `continuationStarted=true` and `continuationResultComplete=false`; poll its job and require `outputSummary.resultComplete=true`. Continue later with `opencode_continue` only after fixing the model/provider/scope problem.
