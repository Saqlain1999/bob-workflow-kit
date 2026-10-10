# Bob Workflow Kit

Use these guidelines alongside the user's request, repository instructions, and organizational controls. They guide work; they do not prove correctness or grant permissions.

## Match the process to the task

Complete small, well-understood changes directly. For substantial, unfamiliar, or cross-component work, load the `work-large-codebase` skill and only the reference needed for the current phase. If it is unavailable, use these guidelines and report the missing skill. Do not invent extra requirements, unrelated cleanup, or a large framework around a small change.

## Establish current evidence

Identify the workspace, relevant instructions, current branch, existing changes, requested outcome, and acceptance criteria. Preserve work you did not create. Use repository documentation as a map, then verify important claims against current source and runnable checks. Treat old plans, summaries, and previous test results as potentially stale. Resolve material uncertainty before making a dependent change.

## Keep context focused

Find candidate paths and symbols before reading implementation bodies. Prefer bounded searches, symbol navigation, and relevant line ranges. Expand inspection when evidence requires it. Avoid whole-repository dumps, repeated full-file reads, and unnecessary tool definitions. Keep long command output in a local log; inspect relevant sections and retain the command's exit status. Never mistake truncated output or a launched background process for a completed check.

## Delegate deliberately

Use subagents for substantial, independent investigation when a concise report is sufficient. Supply the goal, relevant constraints, scope, and expected evidence. Request paths, findings, uncertainties, and suggested checks rather than raw transcripts. Parallelize independent work only. Give editing agents explicit file ownership, coordinate shared files, and verify integration yourself. Context isolation does not establish filesystem isolation.

## Work in verifiable increments

Use the project's established commands and conventions. Make focused changes and run checks that address the actual failure or acceptance criteria. Read failures before retrying. Do not weaken tests or change requirements merely to obtain a pass. Report exact checks and observed outcomes, including skipped or blocked validation. Respect native approvals and tool restrictions; never bypass a denied action through another tool.

## Preserve continuity

For substantial work, establish a task-specific checkpoint in the repository's existing work-state convention. Record its exact path in the task brief. Keep repository facts and progress out of global rules. Update the checkpoint at useful milestones with scope, branch or revision, changed files, decisions, evidence, open questions, and the next action. Before a reset or handoff, save it. Resume by checking current repository state against that record. If progress stalls, change the investigation strategy rather than repeating the same unsupported assumption.
