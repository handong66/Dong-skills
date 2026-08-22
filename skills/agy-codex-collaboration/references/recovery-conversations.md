# Recovery and conversations

## Completion and restart

Read the installed plugin skill and result schema before polling. Preserve the returned job identifier across MCP restarts; do not add arguments that the current job-control schema does not accept.

Treat all of these as partial evidence:

- queued or running state;
- a process exit without the plugin's completion predicate — including a successful exit;
- preview text or raw log tails;
- cancelled, timed-out, failed, or truncated output;
- text marked partial, which covers a run that answered and then errored as well as one still in flight.

Only the installed plugin's positive completion predicate and complete final-text field qualify as an agy conclusion. Codex verification is still required.

## Reading a result

The result envelope is the plugin's, not agy's, and a few of its properties change how a caller must read it:

- A large payload is delivered once, through the structured field only, with the text block carrying a notice in its place. A caller that reads only the text block will conclude the run returned nothing.
- A refusal carries no payload at all. Branch on the failure first, then read data.
- The answer text is prose, not a data format. It carries trailing metadata that is not part of the answer, so parsing it for a structured result will pick up fields that were never part of what agy said. Do the parsing in Codex, from what you asked for in words.
- On the observing tools, the envelope reports the outcome of the job being observed, not of the query. A successfully read record of a failed job is still a failure.
- Route on the codes the plugin actually raises. Some codes exist in its vocabulary as internal guards with no runtime path; the plugin's own failure-routing reference marks them, and routing on one produces a branch that never runs.

## Recovery routing

- CLI not discovered: verify trusted plugin configuration and the real executable and version.
- A workspace path that does not exist behaves exactly like giving none at all: the run reports success, says nothing on stderr, and does its work somewhere else entirely. A typo is therefore indistinguishable from a real run by its output alone, which is the second reason the workspace has to be settled before a run rather than checked after one.
- No resolvable workspace: this is refused before a run starts, because agy ignores the process working directory and sees nothing it was not told about. That is a targeting fact, not a confinement one — a run that was told about a directory is not restricted to it. Supply the workspace explicitly rather than retrying. Do not try to confirm the workspace after the fact from the run's own report of its directory — that field names the calling shell's directory even on a run that reached nothing, so it reads as a pass on exactly the runs it should catch.
- Authentication or model uncertainty: separate CLI discovery, model listing, and a harmless real invocation. Pass model identifiers, never display names.
- Silence: a run still emitting events is working however long it has been running. Judge lateness from its last event, not from elapsed time. A quiet run is not a hung one: the plugin already ends a genuine hang on its own, so a run it has left alone is one whose first tool call may simply be a build or a test. Cancelling on quiet alone kills exactly those. A run that exhausts its budget keeps its conversation; a cancelled one does not.
- Ended early as stalled: a provider or model hang rather than slow work. A larger budget will not help, and neither will a narrower target — retry with a lighter explicit model.
- Timeout: a budget that ran out, which is a different thing. The conversation survives, so resume it rather than rerunning the work from the start — unless the run was an isolated review, which must be re-run rather than resumed; see Conversations. Narrow the target when the timeout came from exploration that was too broad.
- Worker unavailable after restart: preserve the failed record, inspect evidence, and rerun narrowly; do not claim agy concluded.
- Partial or truncated output: do not infer absence, and do not quote it as final.
- Cancellation: inspect workspace state before any rerun, especially after an authorized implementation or a rescue, both of which reach the real tree.

## Conversations

A timeout keeps the conversation, so continue it rather than rerunning the work — **except after an isolated review**. Continuing is a write-capable run against the workspace you are pointed at, not a resumption of the isolation the first run had. Resuming a timed-out isolated review therefore aims agy at the live repository, with permissions skipped, carrying paths from a copy that no longer exists. An isolated review that ran out of budget must be re-run as a fresh isolated review with a narrower target. Continue only what was write-capable to begin with.

Two properties change how a continuation must be read:

- **An unknown conversation identifier does not fail.** agy warns, exits successfully, and starts a fresh conversation carrying none of the earlier context — a confident answer from a model holding none of the history it appears to hold. The plugin surfaces this as a warning; when it appears, treat the answer as a fresh run and not as a continuation.
- **Turn counts and token usage accumulate over a conversation**, and wall time grows as it deepens. A long resume chain is slower and more expensive than asking the same question fresh. Continue for continuity, not for convenience.

Any listing available to you is the plugin's record of what it started, not agy's history. A conversation begun outside it cannot appear, and an old one can age out of the record. Do not read an absence there as evidence that a conversation never existed.

Conversation evidence may contain prompts, workspace-derived text, and model output. Apply the same secret and private-context boundary as a new delegation, and note that a prompt is not a private channel while a run is in flight.

Do not claim a Codex-to-agy transfer or import path. The installed plugin exposes none.

## Version drift

The plugin's runtime contract is measured against one agy build, and the CLI updates itself. Read the contract as the behaviour of the version it names, not as a permanent guarantee — and when a measured behaviour turns out not to hold, treat the CLI as having moved and say so, rather than working around it silently. The installed plugin schema stays authoritative over this skill; the CLI's observed behaviour stays authoritative over the contract.
