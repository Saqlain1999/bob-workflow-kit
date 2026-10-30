# Release evidence and claim boundaries

## Evidence classes

| Class | Supports | Does not support |
| --- | --- | --- |
| Exact-state check | The named command and observed result for the identified state and environment | Other commits, clients, platforms, configurations, or unrun behavior |
| Independent review | The review's bounded findings and decision for the reviewed state | Absence of defects outside scope, compliance, or release approval |
| Static/document check | Syntax, structure, links, or packaging covered by the check | Runtime behavior, usability, compatibility, or performance |
| Live client observation | The named client/version behavior under the recorded conditions | Universal compatibility or behavior on another version/environment |
| Historical result | What was observed for an earlier state | Current readiness after source, test, dependency, configuration, or documentation changes |

## Release-blocking conditions

Treat the release as blocked when any of these apply to the agreed scope:

- a confirmed blocking review finding is unresolved;
- required acceptance behavior currently fails;
- the candidate state cannot be tied to the required checks;
- required upgrade, migration, removal, or rollback behavior is unsafe or unknown;
- a required license, attribution, security, privacy, or compatibility statement cannot be made accurately; or
- a required permission or trusted check is unavailable and the repository does not define a safe exception.

Do not lower a finding, omit a failed check, relabel a historical result, or narrow the documented scope merely to reach a ready decision.

## Release review packet

A complete handoff identifies:

1. candidate state and complete release diff;
2. included and excluded behavior;
3. acceptance and preservation results;
4. independent findings and their current dispositions;
5. exact checks, environments, results, and unrun scope;
6. user/operator documentation changes;
7. compatibility, migration, removal, rollback, security, and privacy notes;
8. artifact, tag, deployment, and announcement status; and
9. the next authorized action and the evidence invalidated by a later change.
