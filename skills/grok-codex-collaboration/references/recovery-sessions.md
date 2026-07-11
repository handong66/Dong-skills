# Recovery and sessions

## Completion and restart

Read the installed plugin skill and result schema before polling. Preserve the returned job identifier across MCP restarts; do not add workspace arguments that the current job-control schema does not accept.

Treat all of these as partial evidence:

- queued or running state;
- a process exit without the plugin's completion predicate;
- preview text or raw log tails;
- cancelled, timed-out, failed, or truncated output.

Only the installed plugin's positive completion predicate and complete final-text field qualify as a Grok conclusion. Codex verification is still required.

## Recovery routing

- CLI not discovered: verify trusted plugin configuration and the real executable/version.
- Authentication or model uncertainty: separate CLI discovery, login/model listing, and a harmless real invocation.
- Timeout: narrow target, role, and requested output before increasing time.
- Worker unavailable after restart: preserve the failed record, inspect evidence, and rerun narrowly; do not claim Grok concluded.
- Partial or truncated output: do not infer absence or quote it as final.
- Cancellation: inspect workspace state before any rerun, especially after an authorized implementation attempt.

## Sessions

Continue a known session when continuity is useful and safe; use an explicit request before selecting the latest session. List or export sessions only when the user asks or prior Grok work is relevant evidence.

Session exports may contain prompts, workspace-derived text, and model output. Apply the same secret and private-context boundary as a new delegation.

Do not claim a Codex-to-Grok transfer or import path unless the installed plugin explicitly exposes and documents that capability.
