# Bob Workflow Runner

**Design preview: specifications and examples only. There is no executable runner, supported installation command, or tested Bob integration in this repository.**

This project explores a small controller for bounded coding tasks delegated to IBM Bob. The goal is to make a workflow's scope, stage transitions, budgets, and verification evidence inspectable. A controller could eventually decide when a task may advance; a prompt alone cannot provide that guarantee.

The central proposed rule is straightforward: a successful agent session and a passing command are separate observations. A task may reach `review_ready` only when the required checks pass against the exact recorded candidate state, the state remains current, and the process and budget records are complete. `review_ready` would mean ready for human review, not approved, merged, or deployed.

## What is available

| Document | Purpose |
| --- | --- |
| [Architecture](docs/architecture.md) | Components, authority boundaries, command supervision, and workspace identity |
| [State transitions](docs/state-transitions.md) | Proposed guards and failure paths |
| [Task contract](docs/task-contract.md) | Meaning and validation requirements of a future contract |
| [Example contract](examples/task.example.json) | Deliberately incomplete template with explicit placeholders |
| [Evaluation plan](docs/evaluation-plan.md) | Observable acceptance criteria and failure fixtures |
| [Roadmap](ROADMAP.md) | Evidence required before implementation or compatibility claims |
| [Source notes](docs/sources.md) | IBM primary references checked on 2026-10-13 |

Start with the architecture, then trace one task through the state table. Review the example contract as a proposal; no application here consumes it.

## Before implementation: build or adopt

Existing tools already provide much of the proposed shape. Bob's [native session commands](https://bob.ibm.com/docs/shell/features/slash-commands), [rollback](https://bob.ibm.com/docs/ide/features/rollback), and [documented workflows and subagents](https://bob.ibm.com/blog/bob-v2-release-announcement/) should be the first comparison. The [Bob Shell 2.0.5 changelog](https://bob.ibm.com/docs/shell/changelog#205) documents task sharing between Bob Shell running as an ACP agent and connected editors; [2.0.6](https://bob.ibm.com/docs/shell/changelog#206) lets ACP clients select the initial session mode. The current [ACP guide](https://bob.ibm.com/docs/shell/features/acp) lists Zed, IntelliJ IDEA, Neovim, and Xcode, and documents editor/runtime ownership, workspace trust, MCP ownership, and launch-environment differences that affect a real handoff. Treat these as native adoption candidates, not as proof of a controller-owned task contract, an external shared board, or current verification evidence. [Bob Control](https://github.com/PounceAI/bob-control/blob/315cbf54076842f06462ea8846aae837594c67cd/README.md) already has an MCP server, CLI, worker, task state, and checkpoint recovery. [Bob+ Headless Bob](https://github.com/ibm-self-serve-assets/building-blocks/blob/5c610971dc72f9e9035821b3cb2c3edea868f8b4/ai/engineering/headless-bob/assets/headlessbob/README.md) supplies a service runtime with persistent run state, cancellation, and limits. IBM's workshop also includes a [Plan–Act–Evaluate example](https://github.com/IBM/intro-bob-workshop/blob/352cdb45d8ad2a53b27aaa31a9248edf3bc8f2fe/.bob/skills/agent-with-bob-shell/SKILL.md).

These references were reviewed as documentation and source on **13 October 2026**; they were not executed in this comparison. They are adoption candidates, not compatibility endorsements. Their invocation, permission, version, and workspace assumptions require review before use.

Before accepting an executable implementation here, complete the [build-versus-adopt gate](ROADMAP.md#1-build-versus-adopt-decision). Identify a specific unmet scenario, compare native Bob and Bob Control, and evaluate a relevant existing runtime where authorized. Prefer documentation, an upstream contribution, or a narrow adapter when that solves the problem. A separate controller needs evidence of a remaining gap and a bounded acceptance case; a generic agent loop is insufficient justification.

The kit's [alternatives and coexistence guide](https://github.com/Saqlain1999/bob-workflow-kit/blob/main/docs/alternatives.md) also covers Spec Kit, repository context, onboarding, and debugging tools. This repository makes no uniqueness or performance claim for its proposed design.

## Proposed shape

The controller would validate a task contract, capture a baseline, request a bounded plan, run one authorized implementation stage, and independently supervise repository checks. A failed relevant check could permit a bounded repair attempt. A changed candidate would invalidate earlier verification.

If a separate implementation is justified, its first version should support one task and one isolated workspace at a time. Repository commands must come from a reviewed project profile. This avoids treating `npm test`, `pytest`, or another conventional command as a universal definition of correctness.

IBM documents that `bob run` pre-approves tool calls. The proposed adapter must consequently obtain applicable authorization before launching a session and qualify the restrictions it relies on. See the [primary source and capability notes](docs/sources.md); this preview does not change Bob's approval settings.

## Current limits

- No executable controller, parser, state store, supervisor, or Bob adapter is included.
- No evidence of enforcement, compatibility, reliability improvement, or benchmark performance has been collected.
- No API keys, paid model calls, credential setup, global configuration changes, hooks, or external integrations are needed to review this repository.
- The design is not a security sandbox. A future implementation must separately qualify process containment, filesystem isolation, and its supported operating systems.

## Companion projects

- [bob-workflow-kit](https://github.com/Saqlain1999/bob-workflow-kit): instruction and skill starter kit.
- [bob-workflow-evals](https://github.com/Saqlain1999/bob-workflow-evals): evaluation definitions and evidence discipline.
- [awesome-bob-workflows](https://github.com/Saqlain1999/awesome-bob-workflows): curated workflow references.

The runner is optional. These specifications do not make the companion kit enforce a fixed execution pathway.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md). Original repository documentation and examples are available under the [MIT license](LICENSE). IBM software, product names, and linked documentation retain their respective rights and terms. This is an independent community project, without a claim of IBM endorsement.
