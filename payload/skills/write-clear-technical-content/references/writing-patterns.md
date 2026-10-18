# Technical writing patterns

These patterns are preferences, not mechanical proof of quality. Repository style and the requested format take precedence.

## Procedure

State the outcome, prerequisites, ordered actions, expected observation, and recovery path. Put one action in each numbered step. Place a condition immediately before the step it controls.

Weak: “After checking things, run the setup and it should probably work.”

Clearer: “Confirm that Python 3.10 or later is installed. Run `python3 setup.py`. A successful run exits with status 0.”

The clearer version is valid only if the source establishes the version, command, and exit behavior.

## Error message

State what failed, the known cause or evidence, and a safe next action. Do not present a suspected cause as confirmed.

Weak: “Something went wrong while processing the configuration.”

Clearer: “Bob could not parse `settings.json`. The parser reported an unexpected comma on line 12. Remove the comma, then validate the file again.”

## Handoff

Record the requested outcome, current revision or state, relevant files, completed checks with results, known failures, constraints, and the next concrete action. Separate observed results from hypotheses.

## Review finding

Name the location, behavior, impact, evidence, and bounded fix. Avoid ratings without a defined scale. Do not claim “production ready,” “secure,” or “fully compatible” from a narrow check.

## Agent or tool instruction

Define the input, permitted scope, required steps, output schema, evidence requirement, and stop conditions. A role label can help routing, but a persona does not replace acceptance criteria or tool-enforced permissions.
