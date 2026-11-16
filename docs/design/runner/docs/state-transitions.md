# Proposed state transitions

**This is a specification, not an implemented state machine.** All guards belong to the controller; model text is an input, not an authorization or state mutation.

## Separate the observations

| Record | Example values | Meaning |
| --- | --- | --- |
| Task stage | `planning`, `executing`, `verifying`, `review_ready` | Where the controller is in the workflow |
| Agent invocation | `running`, `completed`, `errored`, `timed_out`, `cancelled`, `unknown` | What happened to one Bob process |
| Check result | `passed`, `failed`, `timed_out`, `output_limit`, `not_run` | What happened to one approved command |
| Verification validity | `not_run`, `current`, `stale`, `incomplete` | Whether evidence applies to the current candidate and required input set |
| Cleanup | `complete`, `incomplete`, `unknown` | Whether supervised processes have been accounted for |

An invocation marked completed does not mark a task verified. A zero exit code is insufficient when the check list is incomplete, inputs changed, output was cut off by a hard limit, or descendants remain unresolved.

## Allowed transitions

| From | To | Required guard and recorded action |
| --- | --- | --- |
| `draft` | `preflight` | Contract parses; placeholders, unknown keys, and unsupported versions are rejected. |
| `preflight` | `planning` | Dedicated workspace and baseline recorded; applicable launch authorization, adapter capability check, process boundary, and budget reservation are valid. |
| `planning` | `awaiting_approval` | A bounded plan exists but the proposed implementation is not yet covered by an applicable authorization. No implementation is launched. |
| `planning` | `executing` | Plan is within the approved contract; launch budget and capability profile remain valid. |
| `awaiting_approval` | `executing` | External approval refers to the exact plan and contract; fresh preflight still passes. A changed baseline returns to preflight. |
| `executing` | `verifying` | Agent has stopped; cleanup is complete; candidate and diff are recorded and in scope. The agent's exit status remains a separate observation. |
| `verifying` | `repairing` | A relevant check failed; diagnosis permits code repair; authorization still applies; total retry and cost budgets permit another invocation. |
| `repairing` | `verifying` | Repair process is accounted for; fresh candidate snapshot recorded; all invalidated required checks are scheduled again. |
| `verifying` | `review_ready` | Every required check passed on one current candidate; snapshot consistency and cleanup are complete; live state still matches; no budget, scope, or authorization issue remains. |
| Any active stage | `blocked` | Missing authorization, unresolved process, unknown cost, input drift, unsupported capability, infrastructure problem, or exceeded scope prevents safe advancement. |
| Any active stage | `failed` | The defined task cannot complete within its accepted contract, or a terminal validation failure exhausts the repair budget. |
| Any active stage | `cancelled` | Cancellation requested; retain the actual cleanup outcome and unfinished-work record. |

Every unlisted transition must be rejected. A controller error must not fall through to `review_ready`.

## Resume and repair

Resuming a blocked or interrupted task requires a new preflight using the existing run history. Invocation counts and spend reservations persist. Unknown prior process state is reconciled before any new launch. A stale approval or a changed contract cannot be silently carried forward.

The default example permits one repair attempt. Authentication problems, unavailable dependencies, timeouts, output limits, broken containment, and unclear test infrastructure should block for diagnosis rather than trigger a code-edit loop. Merely repeating an unchanged successful command does not refresh evidence for a changed candidate.

## Evidence invalidation

A source edit, staged-index change, relevant untracked-file change, validation-profile change, declared-input change, or unqualified toolchain change invalidates current verification. A new relevant file must enter the inventory; recording only files the model mentioned is insufficient.

Keep old check records immutable and mark their relationship to the current state as stale. Do not rewrite an old record's candidate ID. A later implementation may justify selective reruns through an explicit dependency model, but the initial controller should rerun every required check after a repair.

## Terminal meaning

`review_ready` packages the contract, baseline and candidate identities, readable diff, check outcomes, budget accounting, cleanup status, and limitations. It never performs an automatic commit, merge, publication, or deployment. Any such action would require a separately designed and authorized workflow.

If the candidate changes after the report is produced, the report remains historical evidence of its recorded snapshot. It is no longer a claim about the current workspace.
