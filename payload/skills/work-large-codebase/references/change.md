# Investigate and implement a bounded change

## 1. Establish the baseline

State the requested behaviour and observable acceptance criteria. Identify applicable instructions, relevant existing changes, and any task checkpoint. Inspect current code before trusting an old summary.

Locate candidate files through names, symbols, imports, call sites, or diagnostic evidence. Follow the relevant data flow across component boundaries. Read enough context to understand contracts and side effects; do not impose an arbitrary maximum number of files.

Run an appropriate existing check when it will clarify the defect or establish the baseline. Record pre-existing failures separately from failures caused by the change. Do not treat an unavailable environment as a passing result.

## 2. Choose the smallest coherent plan

For substantial work, record the affected components, required ordering, compatibility constraints, and verification steps. Separate independent investigation from dependent implementation. Explain material tradeoffs or missing requirements before making a consequential assumption.

Choose routine, reversible implementation details using the repository's conventions. Do not turn every step into a permission request. Follow the actual user authorization and native approval controls.

Create or update a task-specific checkpoint when continuity is useful. Include its exact path in the task brief. A plan is not evidence that a change has been implemented.

## 3. Implement and inspect

Make focused edits that fit the existing design. Avoid unrelated formatting, dependency upgrades, or architecture changes. Preserve user changes and coordinate any shared files.

Use exploration subagents for substantial independent questions that need only a summarized result. If editing is delegated, state file ownership and integration expectations. Do not assume separate conversation contexts provide separate working directories.

For long commands, retain their logs and exit statuses. Use background execution when available and useful, but wait for dependent results before proceeding. Read failures and relevant surrounding output before retrying. Change the hypothesis or investigation when evidence contradicts the current approach.

## 4. Verify the behaviour

Select checks that could detect the actual bug or acceptance failure. For a bug fix, an appropriate regression test should distinguish the faulty behaviour from the intended behaviour. Avoid tests that merely repeat the implementation or assert a self-written completion marker.

Run focused validation first, then broader checks when integration risk or repository policy requires them. Do not rerun expensive suites without a concrete reason. Do not weaken tests, bypass validation, or relabel an error to manufacture a pass.

Check failure paths and cross-component interfaces when they are affected. A successful command does not prove requirements it did not exercise.

## 5. Close or hand off

Inspect the final diff and compare the observed result with the acceptance criteria. Update the checkpoint with actual changed files, commands and outcomes, remaining risks, and the next action if work continues.

Report completed work distinctly from proposals and unverified assumptions. Include blocked validation and its cause. Commit, push, publish, deploy, or change external systems only when that action is authorized; saving a checkpoint does not require any of them.
