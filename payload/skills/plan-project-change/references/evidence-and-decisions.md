# Evidence and decision rules

## Repository evidence

For each important fact, record the path or command and the observed value. Useful evidence includes repository instructions, current status, entry points, call sites, tests, schemas, dependency manifests, and supported-version documentation. A filename alone is not evidence of behavior; read the relevant content.

Use these labels: **Observed** for directly read or executed facts; **Inferred** for conclusions drawn from named observations; **Assumed** for necessary premises not yet verified; and **Unknown** for missing information that remains open.

Do not turn search absence into proof that a behavior does not exist. State the search scope.

## Acceptance criteria

Give each criterion a stable ID such as `AC-1`. A criterion should identify the trigger, observable result, and important boundary or preservation requirement. Prefer `Given / When / Then` when it makes the condition clearer.

Reject criteria such as “use a clean architecture,” “update the service,” or “tests pass” without naming the behavior that must pass. Tests are validation methods, not the user outcome.

## Architecture decision

Record the decision, viable options and rejected alternatives, evidence-based tradeoffs, selected option and rationale, consequences and rollback, and a revisit trigger. Do not introduce a framework, service, datastore, or public interface only because it is familiar. Prefer the smallest design that satisfies the criteria and fits existing project conventions.

## Stop and recovery

Stop before implementation when required source is unavailable, an authoritative instruction conflicts with the request, a consequential product decision is unresolved, required permission is denied, or safe validation cannot be described.

The checkpoint must include the inspected state, evidence that may become stale, outstanding decisions, the next safe action, and the checks that must run after implementation. On resume, inspect status and revalidate affected evidence before editing.
