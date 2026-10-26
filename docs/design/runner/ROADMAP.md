# Roadmap

The current design preview is published. Later milestones describe proposed work, not available executable features or delivery dates. Implementation milestones are conditional on the build-versus-adopt decision below; adopting an existing tool is a valid outcome.

## 0. Design preview — current

The architecture, transitions, example contract, source notes, and evaluation criteria are published. Resolve disagreements about scope and evidence before introducing executable behavior. No runtime evaluation has been performed.

## 1. Build-versus-adopt decision

Complete this review before accepting executable implementation work. Start with the user's concrete missing behavior, then compare the simplest existing approaches:

| Candidate | What to assess | Primary sources reviewed through 13 October 2026 |
| --- | --- | --- |
| Native Bob | Whether task history/resume, ACP task sharing, client-selected initial mode, editor/runtime ownership, workspace trust, context management, subagents, and available workflows already address the need; distinguish conversation continuation from file restoration, fresh-session handoff, shared work records, and current verification. | [Shell commands](https://bob.ibm.com/docs/shell/features/slash-commands), [Shell 2.0.6 changelog](https://bob.ibm.com/docs/shell/changelog#206), [Shell 2.0.5 changelog](https://bob.ibm.com/docs/shell/changelog#205), [ACP guide](https://bob.ibm.com/docs/shell/features/acp), [IDE context](https://bob.ibm.com/docs/ide/core-concepts/context-window-management), [v2 workflows](https://bob.ibm.com/blog/bob-v2-release-announcement/) |
| Bob Control | Existing task state, worker, dependencies, checkpoints, attempts, and verification behavior; identify any required behavior missing from the applicable version/configuration. | [README](https://github.com/PounceAI/bob-control/blob/315cbf54076842f06462ea8846aae837594c67cd/README.md), [checkpoint implementation](https://github.com/PounceAI/bob-control/blob/315cbf54076842f06462ea8846aae837594c67cd/src/checkpoint.ts), [judge implementation](https://github.com/PounceAI/bob-control/blob/315cbf54076842f06462ea8846aae837594c67cd/src/judge.ts) |
| Bob+ Headless Bob | Existing service interfaces, persistent runs, cancellation, queues, and limits when the use case requires remote or application-driven task execution. | [Runtime README](https://github.com/ibm-self-serve-assets/building-blocks/blob/5c610971dc72f9e9035821b3cb2c3edea868f8b4/ai/engineering/headless-bob/assets/headlessbob/README.md) |
| IBM workshop agent example | Whether its existing Plan–Act–Evaluate example is enough for an educational or small workflow use case. Review current client semantics before reusing its examples. | [Skill source](https://github.com/IBM/intro-bob-workshop/blob/352cdb45d8ad2a53b27aaa31a9248edf3bc8f2fe/.bob/skills/agent-with-bob-shell/SKILL.md) |

The source review above is complete; runtime comparison and the adoption decision are **not complete**. At minimum, the decision must cover native Bob and Bob Control. Include other candidates when their interfaces match the need. Keep the comparison proportionate to the proposed change.

For a cross-editor handoff scenario, evaluate native ACP task sharing before proposing another persistence layer. Qualify the editor, initial mode, workspace trust, launch environment, and ownership of each MCP server; the ACP guide warns that editor and Bob MCP configuration can overlap and that Bob runs commands in its own child-process environment. The documentation establishes that continuity and client-selected starting mode are available; it does not show whether an old check still applies after source or requirements change, provide a controller-owned contract, or replace an independently inspected shared task board.

Record the required scenario, candidate revision/client version, configuration, prerequisites, applicable authorization, and the observed outcome. Distinguish documentation review, local fixture execution, and live Bob execution. An unexecuted candidate is unresolved rather than a demonstrated failure. Any live trial needs an authorized disposable workspace and explicit resource limits.

Useful discriminating scenarios include a relevant input changing after a passing check without a new commit, an unavailable verifier, an interrupted task with an unrelated user edit, and cancellation that leaves a descendant process running. Choose the scenarios that the proposed use case actually requires. Check a tool's configured semantics: a successful invocation, a favorable model verdict, and independently current verification are different evidence. Do not infer missing capability from a product label or infer enforcement from a prompt.

Exit condition: a reviewed record chooses **adopt**, **contribute upstream**, **build a narrow adapter**, or **implement a separate bounded component**. A separate component must identify the remaining gap, explain why a smaller change is insufficient, and define an observable acceptance case. If no material gap remains, retain this repository as a design reference and evaluation resource instead of building a duplicate runner. No comparison-performance claim follows from this decision alone.

## 2. Offline contract and state core

Implement strict input validation, canonical contract digests, a single-writer state store, transition guards, and atomic recovery records. Reject placeholders and unsupported schema versions. Test illegal transitions, modified state records, interruption, and stale evidence without Bob or a network connection.

Exit condition: local tests demonstrate that a task cannot become `review_ready` through a model-authored status field or stale verification record.

## 3. Local command supervisor

Add reviewed command profiles, explicit argument vectors, time and output budgets, cancellation, process containment, and snapshot-based validation. Begin with one documented operating system. Reject unsupported containment requirements rather than imply portability.

Exit condition: the local failure fixtures in the evaluation plan pass, including descendant cleanup, hung pipes, output floods, and concurrent workspace changes.

## 4. Version-qualified Bob adapter

Specify a narrow adapter and a test protocol before making any live calls. A volunteer must explicitly authorize their own credentials, spending limit, isolated test workspace, and network use. No contribution should require sharing a key with this project.

Exit condition: published, redacted evidence identifies the exact Bob version and tested options, session termination behavior, observed cost accounting, applicable approval semantics, and remaining gaps. Unsupported or changed client behavior blocks launch.

## 5. Evaluated alpha

Run repeated, small tasks with and without the controller, using the companion evaluation definitions. Report failures and overhead alongside success, and publish no aggregate improvement claim without a reproducible method and results.

Only after these gates should this repository offer installation instructions, supported-platform claims, or a stable contract schema. Hooks, parallel execution, multiple agents, automatic publishing, and additional client adapters remain outside the initial scope.
