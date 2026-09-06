# Recovery and sessions

The installed Grok plugin owns result fields, stop reasons, permission modes, recovery handles, and budgets. Read its current skill/schema. Use structured results and warnings; a terse text copy, process exit, or partial answer is not finality.

## Submission, completion, and recovery

- Keep the job and session identifiers. Distinguish a failed submission from a submitted job before retrying, and use the plugin's own lifecycle tools after a restart.
- Read the terminal state and completion predicate separately. Stop polling a terminal record. A partial answer remains useful evidence but cannot pass a review gate.
- When the plugin returns a recovery/finalization suggestion for an existing partial answer, use that supported same-session route within the original authority. Do not restart investigation, narrow away required content, or raise the budget merely to obtain the answer already gathered.
- Verify the resulting completion evidence and then the claims themselves. Recovering text does not turn missing file access into a completed inspection.
- Route authentication, quota, provider, permission, and budget failures according to the current typed error. Do not repeat unchanged non-retryable requests, expose sign-in codes, or change an explicit model/effort preference without authorization.

Use waits appropriate to the host and plugin, with progress updates for the user. No output during a long-running tool is not proof of a stall. Confirm cancellation before handing off a writer.

## Read-only sessions and scope

Reviews, adversarial reviews, and rescue may use enforced read-only modes that refuse shell execution. Supply only the necessary sanitized diff, command result, or source excerpt in the target. Label it as supplied evidence. Do not ask the reviewer to execute a command its mode forbids, widen approval to recover a read-only session, or bypass the plugin via a raw CLI call.

Continue an explicit known session whenever possible. A latest-session shortcut may select a different conversation; verify identity and inherited mode through the current plugin contract. A continuation is not authorization to upgrade a read-only task to implementation. Start a separately authorized implementation with a new packet if needed.

Use only advertised listing/export capabilities to recover handles; do not invent transfer/import functionality or copy hidden host context. Keep exported material local unless the user authorized its destination.

## Evidence decision

Read denied-tool and inspected-file evidence. A zero-evidence review is no signal, not GO. A thin result needs the missing source or independent verification. Record accepted/rejected/narrowed claims and OPEN/CLOSED/REJECTED findings against a pinned artifact. Follow-up work confirms repairs and directly affected behavior rather than opening unrelated review scope.
