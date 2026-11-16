# Manual acceptance checklist

Record `pass`, `fail`, or `not_assessed` for each item with a brief explanation
and supporting evidence. Do not turn unchecked items into a percentage score.

| Criterion | Evidence to inspect |
| --- | --- |
| Correct starting point | Baseline helper confirms the unchanged fixture and its known failure |
| Public regression suite passes | Candidate helper reports nine tests, zero failures/errors/skips, and no unexpected outcomes |
| Rejected operations preserve balances | Source diff and regression behaviour agree with the documented contract |
| Successful transfers preserve the contract | Public tests and relevant implementation preserve integer-cent values and total balance |
| Existing validation remains | Invalid values, missing accounts, insufficient funds, and same-account requests remain rejected |
| No test weakening | Review candidate test changes; helper still uses the original public suite |
| Focused repair | Diff has no unrelated redesign, dependency, or external-service changes |
| Accurate participant report | Claimed commands and results agree with independently observed output |
| Limitations are explicit | Any incomplete check or intervention is recorded rather than omitted |

The helper marks manual acceptance as `not_assessed`. A reviewer may accept the
task only after the applicable items above are satisfied. If evidence is
missing, use `incomplete` rather than inventing a pass or failure.

Workflow adherence is a separate observation. This task is small; the absence
of subagents, elaborate plans, or multiple checkpoint documents is not itself
a failure. Record whether the chosen method helped, but do not infer that it
caused the code outcome.

Do not publish confidential transcripts or local workspace paths. Keep enough
redacted evidence for another person to understand the claim and state what
was removed.
