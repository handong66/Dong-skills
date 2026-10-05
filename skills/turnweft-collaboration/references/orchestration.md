# Task ownership and review

## Agree on a bounded packet

Use the current user's assignment and project entry documents. Defaults fill gaps; they do not override an explicit role, read-only constraint, model preference, or existing authorization. A small change needs a short packet, not a new specification ceremony. Use a reviewed design and implementation plan when the project requires them or the change needs unresolved design decisions.

```text
Goal and acceptance: one observable outcome and its checks
Target: repository/worktree, base commit, exact diff or named files
Roles: coordinator, implementer, reviewer, integrator; current writer
Authority: allowed reads/edits, forbidden actions, temporary override end condition
Review scope: acceptance criteria and stated operating/threat model
Verification: required project checks, independent evidence, available host
Return: findings or changed files, evidence, attempted checks, remaining risks
```

Keep one role per delegated call. A few named files, one narrow directory, or an explicit diff are useful starting scopes, not universal file-count limits. Do not fold unrelated design, coding, broad discovery, and security scanning into the same call. A bounded adversarial review does not authorize a repository-wide security audit or native subagents.

## Assign and hand off writes

Keep one active writer per shared working tree. A reviewer may read a pinned snapshot while a writer works elsewhere; it must not silently review a moving target. Parallel implementation needs authorized, isolated scopes/worktrees and an integrator. Separate feature names do not isolate shared fixtures, registries, generated files, or documentation.

Roles may change during the task. Before transferring writes:

1. Confirm that the previous writer finished or stopped; an interruption request alone is insufficient.
2. Inspect the complete diff, attribute changes, and preserve unrelated work.
3. Record worktree, base commit, current diff, job/session handles, verified and unverified checks, and remaining edits.
4. Assign the next writer and its exact scope. Sequential edits to the same file are allowed after this handoff.

Existing authorization remains valid within its scope. Multiple external sessions, native subagents, or parallel work require explicit user authorization; do not ask again when already authorized. A role change does not grant broader access or publication rights. Repository cleanup does not authorize deleting global sessions, user configuration, or other projects.

## Reach a review decision

1. Pin the artifact, scope, acceptance criteria, and operating assumptions. Give the reviewer the necessary authorized evidence.
2. Verify each claim against current source or observable behavior. Record `accepted`, `rejected`, or `narrowed`, with a reason and reproducible evidence.
3. Fix validated in-scope findings and run the relevant regression checks.
4. Recheck the repair and directly affected behavior. For a small task, one initial review plus a targeted repair confirmation is a useful starting budget, not a mandatory round count or automatic approval rule.
5. Close the ledger when required evidence is complete and no verified in-scope blocker remains. Reopen only for a relevant change, new evidence, incomplete prior result, or an explicit review request.

Use `OPEN`, `CLOSED`, and `REJECTED` to track findings separately from whether the reviewer finished. Do not introduce unrelated criteria on each round. Out-of-model observations are advisory under the stated scope; if evidence contradicts that scope, explain the discrepancy to the coordinator rather than silently widening it.

A budget cannot turn an open blocker into GO. If the agreed budget is exhausted with a material disagreement, report the pinned evidence, unresolved issue, and recommended resolution; continue independent authorized work. Avoid both automatic passing and endless unchanged review loops. A fresh session can provide independence; a continuation can confirm a narrow repair. Neither is proof of correctness. Model agreement is not an acceptance oracle.

```text
Finding ID and claim:
Pinned target and evidence:
Verdict: accepted | rejected | narrowed, with reason
State: OPEN | CLOSED | REJECTED
Repair and verification actually performed:
Remaining blocker or advisory:
```

## Verify and deliver

Use the project's required checks and the actual capabilities of the current host. Historical sandbox failures are not permanent test restrictions. Distinguish not run, blocked, failed, and passed; a check run against another commit is historical evidence.

For critical gates, derive expected behavior independently of the implementation. Confirm that a representative wrong behavior is rejected; do not let the same generator create both the implementation and its expected answer. Static/AST checks, in-memory probes, filesystem/database tests, integration checks, and production observations support different claims. Do not present one as another. Do not add tests that only match instruction wording or repeat a full suite on unchanged code without a new reason.

When concurrent jobs produce failures, establish a controlled baseline or rerun with bounded resources before attributing them to contention. A later pass alone does not prove the original failure was a flake; retain unresolved evidence.

The assigned integrator inspects the final diff and owns authorized Git and release actions. Follow the project's release runbook, pin the deployed source/artifact, and verify the actual user entry point. A platform's ready status alone is not proof that the intended content or behavior is live. See [evidence-and-artifacts.md](evidence-and-artifacts.md) when reviewing generated or visual deliverables.
