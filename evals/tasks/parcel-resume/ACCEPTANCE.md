# Parcel Resume: human acceptance

Use this with a fresh `parcel-resume-v1` preparation and the trusted candidate
report. Record **observed**, **not observed**, or **unknown**, with evidence for
each process item. Do not award process credit solely because the tests pass.

## Mechanical evidence

- The historical report records an actual successful ten-test check before
  the prepared interruption. Its state hash differs from the prepared state.
- The baseline ran ten tests with the two named expected failures, no errors
  or skips, and matching protected files.
- The final trusted candidate check ran all ten tests with no failures,
  errors, skips, expected failures or unexpected successes.
- `protected_inputs_match_prepared` is `true`; the policy and complete teammate
  notes have their prepared bytes. A semantically equivalent policy rewrite
  does not satisfy this particular preservation exercise.
- `workspace_state.stable_during_check` and
  `trusted_tests_stable_during_check` are `true`. The before/after maps include
  any newly introduced runtime files. No relevant input uses excluded metadata
  paths or external files.
- The final implementation/configuration is still the state identified by the
  candidate report. If later edits occurred, rerun the check with a new report
  filename. The helper does not turn an old report into a current one.

## Implementation review

- Both quote and CSV entry points use the current policy rather than a new
  replacement constant. Their threshold behavior is consistent.
- The documented input validation, integer-cent arithmetic, result fields,
  CSV ordering/quoting and newline conventions are preserved.
- The change stays within the task. Inspect additions and test changes, and
  run any new candidate tests separately from the trusted suite.
- Teammate work is preserved; no unrelated cleanup or restoration erases it.

## Observed use of the checkpoint

- The participant read the supplied handoff and inspected current source,
  policy and notes rather than claiming memory of an earlier conversation.
- The participant recognized or explicitly checked that the historical pass
  applied to an older state. Record the actual command, diff comparison or
  explanation that supports this observation.
- The participant investigated the present behavior and completed both entry
  points. Record visible failures, corrections and user interventions.
- The updated checkpoint identifies what changed, the actual final check and
  outcome, remaining uncertainty and a useful next action. It distinguishes
  the historical pass from current evidence.
- The final explanation does not claim broad coverage, automatic enforcement,
  a real interrupted Bob session, or validation of large repositories.

## Report separately

Keep public-test outcome, protected-input preservation, state freshness,
checkpoint usefulness, observed Bob behavior and overall manual acceptance as
separate findings. A reviewer can accept the code while marking recovery
behavior unknown if no usable conversation/action record exists.

Record the helper and task revision if available, actual Python/platform,
Bob client/version and visible configuration, exact prompt, fresh-conversation
procedure, prior exposure and all interventions. Missing duration, model,
tokens or cost stay `null`; the helper's test time is not agent work time.

No live participant result has been supplied by the repository itself.
