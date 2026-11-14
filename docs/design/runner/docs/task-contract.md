# Proposed task contract

The [example JSON](../examples/task.example.json) is a design template. **No parser or runner is implemented, and this is not an IBM configuration format.** `example_only` and all `REPLACE_WITH_...` values deliberately make the template ineligible for execution by a future validator.

## Required concepts

| Field group | Meaning and future validation requirement |
| --- | --- |
| `task` | A unique task ID, concrete objective, measurable acceptance conditions, and explicit exclusions |
| `workspace` | Operator-selected canonical path, clean baseline commit, isolation profile, and nonsecret input inventory policy |
| `scope` | Allowed write paths, forbidden read/write paths, and workspace-process network policy; no implicit authority to clean or reset the workspace |
| `validation` | Reviewed project-profile digest and a complete list of required checks, with exact argument vectors and working directories |
| `budgets` | Positive, finite job/process deadlines, output limits, invocation/repair ceilings, and a reviewed cost policy |
| `authorization` | References to externally established scope and capability approvals; references are not secret values |
| `adapter` | Qualified local client/version and capability-profile reference, plus the proposed invocation budget settings |
| `evidence` | State-manifest policy, output-retention policy, and required report fields |

Paths must be canonicalized and checked for traversal, redirection, unsupported files, and overlap with controller state. Command strings must not be evaluated by a shell merely because a model suggested them. Any repository command can execute project code, so each check needs an approved project profile rather than a guessed universal test command.

The workspace-process network policy is distinct from the adapter's approved connection to the Bob service. Disabling repository-command networking does not provide the model connection. Both policies need separate qualification; this example configures neither.

The template's numerical limits illustrate units and relationships, not recommended defaults for every codebase. A future validator must check that per-process limits fit the remaining task deadline, repair limits fit the total invocation limit, and cost reservations fit the remaining approved allocation. Zero must not accidentally mean unlimited.

## Input identity

The contract is canonicalized and hashed before approval. Changing it creates a new contract revision and invalidates approvals that do not cover the revision. Runtime state and verification records refer to that digest, the actual baseline, and the current candidate manifest.

An input policy must cover all files and toolchain inputs that affect the declared checks, including relevant ignored or untracked files. Unknown inputs make verification incomplete. A future validator should reject features whose state model is not implemented, such as unsupported submodules or uncontrolled network dependencies, instead of approximating them as exact.

## Authorization and credentials

An approval record binds the contract revision, effective capability profile, permitted actions, budget, and applicable expiry or revocation rule. A generated approval-shaped string has no authority. Where existing user authorization already covers these actions, a controller should reuse that authorization after validating its scope.

The task file contains no key or credential value. Any future adapter must use a separately reviewed secret-delivery mechanism. This preview provides no credential provisioning steps and performs no integration setup.

## Future compatibility

Schema names, field names, transitions, and flags in this proposal may change. Before introducing an executable parser, contributors should publish its exact supported schema and negative validation cases. A future parser must reject this unfilled example instead of substituting permissive defaults.
