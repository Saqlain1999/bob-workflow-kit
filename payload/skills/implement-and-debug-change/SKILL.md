---
name: implement-and-debug-change
description: Implement an accepted, bounded project change or diagnose a reproducible defect with minimal edits, regression evidence, preservation checks, and a resumable implementation handoff.
---

# Implement and debug a project change

Use this skill when the user asks to implement an accepted change, repair a defect, or continue an interrupted implementation whose expected behavior is already bounded. Do not activate it for requirements discovery, architecture selection, independent final review, deployment, or a small direct edit that already has an obvious change and check.

This workflow complements Bob's Agent mode; it does not replace the client's permissions, approvals, rollback, task history, or native tools.

## Verify the input contract

Identify the requested outcome, acceptance-criterion IDs, authorized scope, preservation requirements, and validation commands. If a `DELIVERY_PLAN.md` or checkpoint exists, inspect current repository instructions, status, relevant source, and tests before trusting it. Mark stale evidence and reconcile it with the current state.

Stop before editing when a consequential requirement is unresolved, current evidence contradicts the plan, unrelated changes overlap the necessary files, required permission is denied, or safe validation cannot be described. Never use another command, shell, tool, or path to bypass a denial.

## Establish a reproducible baseline

Run the smallest relevant existing check before changing code. For a defect, record the input, observed result, expected result, and exact failing check. If the defect cannot be reproduced, do not guess at a repair: report the attempted scope and the missing evidence.

Read `references/debugging-evidence.md` when a test fails unexpectedly, the cause is unclear, or more than one implementation path is plausible.

## Implement one reviewable slice

Make the smallest coherent change that advances named acceptance criteria. Follow repository conventions and preserve public interfaces, unrelated work, user data, tests, and configuration unless the accepted scope explicitly changes them.

Do not weaken, skip, delete, or rewrite a failing test merely to obtain a pass. Do not mix opportunistic refactors, dependency updates, formatting churn, or hypothetical flexibility into the slice. Record useful out-of-scope findings separately.

When debugging, test one evidence-backed hypothesis at a time. Prefer a regression test that fails for the observed reason, then make it pass. Inspect the complete diff after implementation and justify every changed file against the acceptance criteria.

## Validate the current state

Run the focused regression check, relevant surrounding suite, and required static or build checks. Bound large command output and preserve the command, exit status, relevant result, and environment. A previous green result is stale after later edits.

Map every acceptance criterion to observed evidence. Distinguish:

- executed and passed;
- executed and failed;
- not run;
- manually inspected; and
- inferred but unverified.

Never describe an unavailable check as passed. Helper tests, mocks, or packaging checks do not establish live service, performance, security, or Bob behavior.

## Leave a resumable handoff

Use `templates/implementation-handoff.md` when work spans multiple files, stops before completion, encounters a failed check, or will pass to review. Record the inspected state, changed files and reasons, criterion evidence, exact checks, failures, preserved inputs, remaining risks, and next safe action.

Stop and preserve the handoff if scope expands materially, a protected input changes unexpectedly, validation becomes unsafe or unavailable, or the current state no longer matches the plan. On resume, inspect status and rerun stale checks before editing.

Return the completed change and concise evidence, not a claim of production readiness. Independent review, security assessment, deployment, and release approval remain separate stages.
