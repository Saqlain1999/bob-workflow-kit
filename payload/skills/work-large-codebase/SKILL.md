---
name: work-large-codebase
description: Plan, implement, verify, and resume substantial or unfamiliar code changes using focused exploration, task-specific checkpoints, and evidence from the current repository.
---

# Work with a large codebase

Use this skill when work spans components, requires substantial investigation, or must continue across conversations. Apply a lighter process to small, well-understood changes. This is a working method, not a guarantee of correctness or an authorization to run tools.

## Start with the requested outcome

Read applicable repository instructions. Identify the current workspace and relevant existing changes without discarding them. Establish the user's goal, constraints, and observable acceptance criteria. Use existing project conventions for plans, tests, and work-state files.

Choose the reference for the current phase; do not load all references and templates by default. Paths below are relative to this skill's directory.

| Situation | Read next |
| --- | --- |
| First substantial task in an unfamiliar repository, or outdated onboarding | `references/onboarding.md` |
| Investigating a defect or implementing a bounded change | `references/change.md` |
| Resuming work, changing conversations, or recovering from a stalled attempt | `references/recovery.md` |

Read the relevant source rather than treating a previous summary as complete. A saved map helps locate evidence; it does not replace evidence.

## Maintain a small working set

Search for relevant paths and symbols, inspect their callers and contracts, then read implementation details as needed. Use available symbol tools or bounded native searches. Do not assume a particular shell, language, package manager, or search utility is installed.

For commands with lengthy output, preserve a log and the actual exit status. Read selected errors and surrounding context. Expand the read if the excerpt is insufficient. Report an asynchronous command as running until its completion has been observed.

Use focused exploration subagents when their findings can be summarized. Pass a precise question, relevant constraints, search scope, and expected output. Avoid copying the entire conversation by default. Keep dependent changes sequential and coordinate any editing agents explicitly.

## Keep state local to the work

For substantial work, select a task-specific checkpoint path under the repository's existing documentation or work-state convention. If there is no convention, choose and state a clearly named local path. That path is an organizational choice, not a special Bob feature, and is not automatically loaded. Include it in future handoff prompts.

Use `templates/repository-profile.md` when an onboarding record would help. Use `templates/checkpoint.md` for task continuity. Read a template only when needed. Adapt it to the repository and omit irrelevant sections; do not leave placeholders presented as facts.

Keep durable rules short. Put changing progress, commands and their outcomes, and unresolved questions in the task record. Respect repository policy about whether those files belong in version control. Do not commit or push them solely because this skill mentions persistence.

## Finish with evidence

Confirm the change against acceptance criteria using relevant checks. Separate passing checks, failures, skipped checks, and untested assumptions. Inspect the final diff for scope and unintended changes. Give a concise result, the checkpoint path if one was used, and any remaining limitation.

Continue authorized work without inserting approval gates of your own. Honour permissions, organizational requirements, and actual user approval boundaries. If a required action is blocked, explain the specific dependency and continue useful independent work.
