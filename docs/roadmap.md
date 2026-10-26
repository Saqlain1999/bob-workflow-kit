# Project scope and roadmap

Bob Workflow Kit is the intended single user-facing product: one checkout, one installation, one first-use guide and one issue tracker. This branch prepares that layout locally; it is not a new published release. See the [consolidation record](consolidation/README.md) for original source commits and outstanding PRs.

## Implemented alpha and included material

The alpha includes the guide, a small documented rules/skills payload, offline setup tooling, copyable prompts, task templates, a deliberately failing fixture, and validation/reporting materials. The [first-use walkthrough](try-alpha.md) is the entrypoint. The [included recovery exercise](exercises.md) uses constructed stale evidence; live Bob behavior must be recorded separately.

- Product and installation: the root kit and `payload/`.
- Evaluation quality and optional exercises: `evals/`, not another product to install.
- Optional reference catalogue: [resources](resources/README.md), not another download.
- Controller proposals: [deferred design notes](design/README.md), not an executable runtime or a committed build.

Keep user installation simple: preview, install, fresh-session loading check, one verified exercise, then project onboarding. Do not require users to understand the internal directory split or import every skill into every conversation. Use the canonical kit tracker for the proposed unified journey; preserve existing URLs and history during transition.

## Evidence-led priorities

1. Finish independent consolidation review and resolve the outstanding PR stack without losing accepted work or historical attribution. Publication and main merge require separate approval.
2. Record actual client loading and a bounded useful task on each named Bob interface/version. Offline green tests do not prove loading or workflow quality.
3. Test realistic interruption recovery: reconcile current source and policy, preserve unrelated edits, execute relevant checks and produce a usable handoff.
4. Improve only what observed failures justify. Add a stack recipe or specialist skill when a repeatable need and acceptance test exist.

The combined offline command is `python3 tools/check_all.py`. CI is configured to run it with full source history; hosted results for this new branch do not exist until it is explicitly published. Existing imported validation records retain their original source/version scope.

## Avoid a second runtime by default

Native Bob and existing runtimes may already supply the needed execution/recovery behavior. Only consider implementing a controller after a specific observed gap and the [build-versus-adopt review](design/runner/ROADMAP.md). Adopting an existing tool, contributing a focused change or doing nothing are valid outcomes. The preserved runner documents are requirements exploration, not another installation step.

Instructions are not execution enforcement. If a controller is ever justified, it must validate task/profile inputs, bound workers and retries, run checks independently and handle cancellation, concurrent edits and unavailable prerequisites. Do not build a recursive keep-fixing engine or add a database, dashboard, scheduler or MCP server without an evidenced need.

## Evaluate benefit rather than advertise it

Compare the same starting task under a stated environment. Track correctness, scope, regressions, recovery, elapsed time, relevant commands, available usage data and human interventions. Repeat trials and include unsuccessful or abandoned attempts. One demonstration is not a performance estimate or proof of large-repository reliability.

Prioritize confusing onboarding, installation collisions, duplicate skill discovery, stale verification and lost handoffs over the number of skills or repositories. The kit remains an independent community project, not an IBM product or Marketplace listing.
