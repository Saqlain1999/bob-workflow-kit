# Debugging and implementation evidence

## Reproduction record

Record the triggering input or state, expected behavior, observed behavior, exact command or observation, and current revision. A log message without the input and state is not a complete reproduction.

If the behavior is intermittent, record attempts and frequency. Do not silently retry until one attempt passes.

## Hypothesis loop

For each hypothesis:

1. Name the suspected cause and the observation supporting it.
2. Choose one discriminating check.
3. Run the check and record the result.
4. Reject, refine, or accept the hypothesis.
5. Edit only after the evidence identifies a justified change.

Search absence is not proof. State the paths, symbols, revisions, or output range searched.

## Regression evidence

A useful regression check fails against the reproduced defect and passes after the repair for the intended reason. It should also protect important compatibility and preservation behavior. Do not:

- weaken assertions to match the faulty output;
- skip or delete the failing case;
- replace a meaningful integration boundary with a mock that cannot expose the defect;
- treat a changed snapshot as automatically correct; or
- rely only on a test the candidate can rewrite.

Run trusted or independently reviewed checks when available.

## Diff and preservation review

For every changed file, name the acceptance criterion or required validation it serves. Inspect unrelated working-tree changes before and after the edit. Preserve existing user files, settings, credentials, generated evidence, and teammate-owned content unless the authorized task explicitly changes them.

Record known failures and unrun checks. A clean focused check does not erase a failing broader suite, and a green suite does not prove performance, security, deployment, or live-client compatibility.
