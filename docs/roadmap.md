# Project scope and roadmap

The first section describes the implemented alpha. Later milestones describe future development. Four complementary repositories are published under the Saqlain1999 account; their implementation status is explicit below.

## First public project: `bob-workflow-kit`

The alpha includes the guide, a small documented rules/skills payload, offline setup tooling, copyable prompts, task templates, a deliberately failing fixture, and validation/reporting materials. The [first-use walkthrough](try-alpha.md) is the public entry point. The companion evaluator adds a constructed stale-evidence recovery exercise; its live Bob behavior remains to be recorded. Next useful evidence is actual client loading and task behavior on each target interface.

Keep user installation simple: one download, one preview, one install, one fresh-session check, then project onboarding. Keep deeper material available without loading it all into every conversation.

## Milestones

| Milestone | User outcome | Evidence required |
| --- | --- | --- |
| Alpha foundation | Install, inspect, and remove the kit; learn the workflow | Offline tests, readable docs, explicit unsupported states |
| Live compatibility | Use the payload in specific Bob versions | Recorded IDE and Shell loading and small-task results, including override handling |
| Repository recovery | Resume a realistic interrupted change | Public fixture, saved checkpoint, current-file reconciliation, relevant checks |
| Stack recipes | Apply the method to common project shapes | Tested Python/JS/Java or other examples with real commands and no guessed dependencies |
| Optional native plugin package | Install a documented bundle in a supported client | Verified format, precedence, update/removal behaviour, and exact client versions |
| Optional workflow controller | Launch tasks through fixed stages and bounded retries | Independent state-machine/process tests, real Bob integration tests, accurate cost/status limits |

## Repository responsibilities

| Repository | Responsibility | Initial state |
| --- | --- | --- |
| [bob-workflow-kit](https://github.com/Saqlain1999/bob-workflow-kit) | User guide, core rules/skills, installer, templates | Implemented alpha; user starting point |
| [bob-workflow-evals](https://github.com/Saqlain1999/bob-workflow-evals) | Reproducible tasks and evaluation materials | Tiny Ledger repair plus Parcel Resume policy/freshness exercise; live Bob and large-repository trials remain future work |
| [bob-workflow-runner](https://github.com/Saqlain1999/bob-workflow-runner) | Controller architecture, task contract, process and verification requirements | Design preview; no executable controller |
| [awesome-bob-workflows](https://github.com/Saqlain1999/awesome-bob-workflows) | Curated links with provenance, status, and compatibility notes | Original catalogue and contribution guidance |

They are independent community projects, not IBM products or registered package names. Core kit installation does not require installing the companions. Keep user setup and installer issues here; route fixture, controller-design, and catalogue changes to the relevant companion.

## Controller design direction

First complete the companion runner's [build-versus-adopt review](https://github.com/Saqlain1999/bob-workflow-runner/blob/main/ROADMAP.md). Native Bob, Bob Control and Headless Bob already provide substantial execution/recovery functionality. Adopting an existing tool, contributing a focused change, or adding a narrow adapter are valid outcomes. The remaining requirements below do not imply a new controller is necessary.

Keep instructions and enforcement distinct. A controller should validate a task/profile, invoke a bounded worker, run required checks itself, and transition among prepare, implement, verify, accept, repair, and stop. It must not accept a model's completion statement as a substitute for actual check results.

Required design questions include changing verification inputs, worker edits to check definitions, cancellation and child cleanup, concurrent edits, unavailable prerequisites, and missing usage data after interrupted calls. Native turn/cost limits and tool restrictions need version-specific tests. Normal IDE conversations remain outside the controller unless explicitly launched through it.

Do not turn lifecycle hooks into a recursive “keep fixing until perfect” engine. Avoid adding an MCP server, vector database, or web dashboard until a specific use case requires one.

## Evaluate benefit rather than advertise it

For each candidate improvement, compare the same starting project/task under a stated environment. Track task correctness and scope, regressions, successful recovery, elapsed time, commands, context/usage data when available, and manual interventions. Repeat trials; one demonstration is not a performance estimate.

Useful early community issues are concrete: duplicate skill discovery on a specific version, loss of task state after a handoff, a missed relevant check, or an installer collision that is hard to understand. Each can produce a reproducible fix and a better documented workflow.
