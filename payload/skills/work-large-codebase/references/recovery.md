# Resume work or recover from a stalled attempt

A fresh conversation can remove stale tool output, but it also loses details that were never saved. Preserve useful evidence before resetting when possible.

## Before a handoff

Adapt `../templates/checkpoint.md` to a task-specific file using the repository's work-state convention. Keep it concise and include:

- The requested outcome, acceptance criteria, and constraints.
- The repository, branch or revision, and timestamp.
- Existing changes that must be preserved and changes made for this task.
- Decisions and the source paths or observations supporting them.
- Exact checks, their observed results, and log paths where needed.
- Failed approaches and the evidence that ruled them out.
- Open questions, blockers, and the next concrete action.

Record running background processes as running, with the available process identifier and log location. Do not call them successful or start duplicate jobs merely because the conversation changes.

Read the saved checkpoint back to verify that it contains the necessary handoff. Provide its exact path and a short instruction for the next conversation to read it. The filename has no automatic loading semantics.

## When resuming

1. Read applicable repository instructions and the named checkpoint.
2. Compare the recorded repository, branch or revision, and changed files with current state. Identify changes made since the checkpoint without discarding them.
3. Re-read source relevant to the next action. Treat prior claims as evidence to check, not immutable facts.
4. Reuse still-valid results. Rerun checks when relevant code, configuration, dependencies, or environment changed, or when the earlier result is uncertain.
5. Continue from the next unfinished step. Update the checkpoint when new evidence changes the plan.

If the checkpoint is missing or incomplete, reconstruct only the relevant state from current source, diffs, and logs. Identify uncertainty explicitly. Do not claim memory of a conversation that is unavailable.

## When progress stalls

Classify the failure before changing settings:

| Observation | Investigate |
| --- | --- |
| A tool waits for approval | Native permissions and active mode |
| A run reaches an explicit limit | Actual turn or cost limit reported by the client |
| A command appears hung | Process status, output, environment, and background execution |
| Searches repeatedly find irrelevant code | Scope, query, entrypoints, and dependency map |
| Constraints disappear or wrong assumptions recur | Stale context and the current checkpoint |
| Checks fail | The actual failure and relevant source, not only the last line |

Correct the cause that evidence supports. Raising a turn limit does not enlarge the context window or fix a wrong hypothesis. Do not repeatedly run the same command without new information.

If a clean conversation would help, save the checkpoint and start from a brief handoff rather than copying the entire transcript. Native compaction may help preserve continuity, but summaries can lose detail. Verify important constraints and results after either compaction or a reset.
