# Sessions, waiting, and recovery

The installed Turnweft skill and tool schemas own result fields, job states, permission tiers, and error codes. Read them for current behavior. Use structured results and warnings; a short text summary is not the result.

## Sessions

- Create one session per agent and stream of work, in the project directory, and keep its session ID for every follow-up in this conversation. Never guess "the latest session". If the ID is lost, list sessions for this project and ask the user when more than one fits.
- A session resumes the agent's own native session after it was stopped for being idle. If resuming fails, Turnweft reports an error instead of starting a fresh agent that has forgotten the work; report it rather than silently creating a new session.
- A session started from the other host is attached only when the user asks to continue it here.
- A continuation keeps the session, not the earlier permission. Each turn is submitted with its own intent; continuing an analysis session does not authorize an implementation turn.

## Submitting and waiting

1. Generate a fresh request ID for each new turn and keep it. If submission errors or times out, retry with the same request ID; Turnweft returns the original job instead of running the work twice.
2. Poll the job with bounded waits and pass the last event sequence to read only new events. Keep the user informed during long turns. No new output while a tool runs is not proof of a stall.
3. When the job waits for confirmation, tell the user which agent, project, and mode are requested and that a dialog is waiting. Keep polling the same job. Do not resubmit: after the user allows it, the job starts by itself. If the user denies it, the job is cancelled. After about ten minutes of waiting, stop polling and ask the user to say "continue" once they have confirmed, then query the same job. If no dialog appeared, give the user the grant command from the Turnweft skill to run themselves; never run it for them.
4. Stop polling once the job is terminal. Read the result once, with paging when it is long.

## Uncertain, failed, and cancelled jobs

- An in_doubt job may have run. Inspect the files and the agent's answer before deciding anything; never resend it automatically.
- Report permission, capability, sign-in, and missing-session failures as they are. Do not switch to another agent, widen permissions, or start a new session without the user.
- Cancellation is confirmed only when the job state becomes cancelled. Before handing writes to another writer, confirm the stop and reconcile the diff.
- A partial answer is evidence, not a completed review. Continue the known session with a narrowed question within the original authority instead of restarting discovery.

## Evidence decision

Files changed during the turn come from git snapshots taken before and after it. They show what changed, not who changed it; edits made by others in the same folder appear too. Changes outside the session directory may belong to someone else. Check attribution before accepting or reverting.

A review with no inspected evidence is no signal, not GO. A thin result needs the missing source or independent verification. Record accepted, rejected, and narrowed claims and OPEN, CLOSED, and REJECTED findings against a pinned artifact. Follow-up work confirms repairs and directly affected behavior rather than opening unrelated review scope.
