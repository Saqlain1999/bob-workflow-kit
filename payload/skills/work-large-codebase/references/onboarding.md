# Onboard an unfamiliar repository

Create a reliable navigation aid without reading every file into one conversation.

## Establish scope

1. Confirm the repository root, applicable instructions, current revision or branch, and existing changes. In a multi-repository workspace, identify which repository owns the requested work.
2. Read existing onboarding and work-state documentation before creating overlapping files. Preserve established conventions and user-authored instructions.
3. Identify the requested outcome. A repository map should support that outcome; it need not become a complete audit of unrelated systems.

## Build the map from evidence

Inspect top-level structure, manifests, build configuration, CI definitions, and relevant entrypoints. Locate the components involved in the task, their public interfaces, and their tests. Follow dependencies where the proposed work crosses boundaries.

Use bounded searches and symbol tools where available. A file listing locates candidates; it is not proof that every file was examined. Read important implementation bodies and their callers before drawing conclusions about behaviour.

Delegate substantial independent questions to exploration subagents when available. Suitable questions include locating a component's entrypoints, identifying how tests run, or tracing a particular API contract. Require each report to include supporting paths, uncertainty, and the extent of its investigation. Avoid asking several agents to produce the same full repository summary.

## Capture a concise profile

Adapt `../templates/repository-profile.md` only if a profile is needed. Record:

- Relevant components and where their responsibilities meet.
- Verified runtime and tool versions, or the files that declare them.
- Actual setup, build, lint, and test commands from the repository.
- Important invariants, generated files, and required services.
- Where task plans and checkpoints live.
- What was inspected, when, and what remains unknown.

Label command status accurately: found in configuration, executed successfully, failed, or not attempted. A documented command is not necessarily safe or runnable in the current environment. Do not install dependencies, contact services, or run migrations merely to mark onboarding complete.

If the installed Bob client supports `/init`, it can create or refresh root `AGENTS.md`. Review the generated content and existing changes. Do not assume every generated statement is correct or overwrite a maintained file blindly. Keep root instructions concise and link to deeper documentation as appropriate.

## Set practical boundaries

Identify generated artifacts, dependency directories, large binary assets, and sensitive files that are not needed for the task. Propose repository-specific exclusions when useful. Keep source fixtures and relevant generated interfaces accessible when they are needed to verify behaviour.

`.bobignore` is workspace-scoped and is not an operating-system sandbox. If Bob's tools prevent editing it, provide the proposed change for an authorized user to apply; do not use another tool to bypass that protection.

End onboarding when the current task has a useful map, known validation routes, and an explicit next step. Record gaps rather than extending exploration indefinitely.
