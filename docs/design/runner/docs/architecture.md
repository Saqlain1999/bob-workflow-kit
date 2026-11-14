# Proposed architecture

**Status: unimplemented design.** Requirements below describe what a future controller would need to prove. They are not claims about this repository's present behavior.

## Components and authority

| Component | Proposed responsibility | Must not decide |
| --- | --- | --- |
| Contract validator | Resolve project profile, scope, budgets, and applicable authorization | Whether a model's answer is correct |
| Controller and state store | Own transitions, invocation counts, reservations, and evidence references | Unapproved changes to the contract |
| Workspace recorder | Identify baseline, candidate, and verification inputs | That a hash alone establishes adequate test coverage |
| Bob adapter | Start one authorized, bounded agent session; parse a qualified output format | Task completion or approval |
| Command supervisor | Run reviewed checks and record outcomes | Invent new checks or repair code |
| Human reviewer | Assess the candidate and grant any additional authorization | Retroactively turn missing execution evidence into a pass |

The model may propose a plan, edits, or a diagnostic explanation. It must not write the authoritative state store, grant approval, increase a budget, or declare a check passed. A future implementation should place controller state outside the agent-writable workspace and protect it with an independently tested filesystem boundary. A path convention alone would not protect it.

## One task, one workspace

The initial implementation should require a dedicated, initially clean Git workspace selected by the operator. It should never clean, reset, or silently replace a user's working directory. Changes already present must cause preflight to stop; support for dirty baselines can be evaluated later.

Only one writer may control a run. The record needs a unique run ID, contract digest, monotonic event sequence, current stage, budget ledger, candidate state ID, and evidence references. Write-ahead intent and atomic state replacement must distinguish a completed transition from an interrupted action. A process found running after a controller crash is unresolved work, not permission to start a duplicate.

## What identifies the current candidate

`HEAD` alone cannot identify uncommitted work. The proposed state manifest should include:

- The canonical workspace identity, full base and current commit IDs, and index entries, including staged paths, modes, and object IDs.
- A sorted inventory of tracked working-tree bytes, additions, deletions, file types, modes, and symlink targets; include relevant untracked files.
- Declared verification inputs, such as lockfiles and nonsecret configuration, including relevant ignored files that tests actually consume.
- The contract and validation-profile digests, toolchain identity, approved environment identifiers, and any isolated dependency snapshot identity.

A readable binary-capable diff from the baseline accompanies this manifest; a diff hash is useful but is not a complete input inventory. Repository identity must account for submodules or reject them in the first supported profile. Symlinks escaping the workspace and unsupported special files should fail preflight.

A secret-dependent or network-dependent check cannot be called reproducible merely because source hashes match. The first profile should reject those dependencies unless an explicit input and isolation model has been reviewed. Never copy credential values into the state manifest.

Verification should run against a frozen candidate snapshot with separately declared writable output locations. Record its identity before starting and inspect it after all checks. A before/after hash match alone cannot prove that another process did not temporarily alter an input during execution. Until snapshot consistency has been demonstrated, the result must remain incomplete. Recheck the live candidate immediately before producing `review_ready`; any difference invalidates its current verification.

## Bob adapter boundary

The adapter would translate a reviewed stage profile into options qualified against a specific Bob version. IBM documents group-level restrictions, including `edit`, `execute`, `mcp`, `subagent`, and `mode`. Plan and Ask mode names alone do not establish the restriction profile needed here. [IBM tool groups](https://bob.ibm.com/docs/shell/core-concepts/tools)

A proposed planning profile would disable editing, execution, external tools, spawning, and mode changes. A proposed editing profile would permit only the capabilities that its contract authorizes. The controller would supervise verification commands itself, keeping test execution evidence independent of the agent's summary.

These options are not an operating-system sandbox. Preflight must identify whether hooks, plugins, inherited settings, or other processes could defeat the intended boundary. If the adapter cannot qualify an isolated effective configuration and containment policy without changing the user's global configuration, it must stop. This preview supplies no configuration rewriting mechanism.

Existing scoped authorization may cover several launches. The controller must check that it still matches the contract, candidate baseline, capability profile, and remaining budget; it must not invent a new approval or repeatedly ask for authorization that already applies. A changed scope or capability profile needs a new applicable authorization before launch. See [source notes](sources.md) for noninteractive approval behavior.

## Command supervision

Resolve commands from the reviewed project profile and launch explicit argument vectors with a canonical working directory. Do not turn arbitrary model text into a shell command. A listed executable can still run arbitrary project code; command selection is an authorization boundary, not proof of safety.

Use a monotonic job deadline and per-process deadline. Drain stdout and stderr concurrently into bounded buffers. On the hard output limit, terminate the process and record `output_limit`; a truncated transcript must not become a success by omission. Preserve exit code or signal, start/end times, dropped-byte counts, and cleanup status as separate fields.

On cancellation or timeout, request termination, wait a bounded grace interval, escalate, and reap the process. Qualify POSIX process groups against detached-descendant fixtures; a descendant can escape an ordinary group. A Windows implementation needs a separately qualified containment mechanism, such as job management, or must reject that platform. Any unresolved descendant makes cleanup incomplete and blocks retries and advancement.

Never launch Bob recursively from a hook, verifier, repair script, or another controller instance. Keep one explicit launch authority, a single-writer run lock, and a marker that a child controller invocation must reject. Such a marker does not substitute for process isolation.

Only the authorized adapter should receive the Bob authentication secret. Verification processes should receive an explicit nonsecret environment and must not inherit that credential or the adapter's provider-network permission.

## Budgets and retained data

Track invocation and repair counts across the whole task, including resumed runs. Reserve an invocation's allowed cost before launch; do not refund an unknown outcome. A stopped process may already have incurred a charge. The adapter must qualify provider accounting and any overshoot before claiming a financial ceiling; wall-time and turn limits are not currency guarantees.

Store status metadata by default. Optional bounded command output needs a reviewed retention policy. Never serialize credential values, environment dumps, authentication files, or unrestricted raw event payloads. Redaction tests can cover known synthetic secrets; they cannot prove detection of every possible secret. Keep logs local and private until a human has reviewed anything intended for publication.
