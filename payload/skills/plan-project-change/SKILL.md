---
name: plan-project-change
description: Inspect an existing project and turn an ambiguous or multi-file change request into evidence-backed acceptance criteria, an architecture decision, a staged implementation plan, and a resumable handoff before source edits begin.
---

# Plan a project change

Use this skill for a feature, refactor, migration, or integration that crosses files or components and still needs requirements or design decisions. Do not activate it for a trivial edit, a pure explanation, or work whose file scope, behavior, and validation are already explicit.

This is a planning workflow. Do not edit product source while using it. The required output is `DELIVERY_PLAN.md` unless the user names another plan file.

## Establish the planning boundary

Restate the requested outcome, constraints, non-goals, and authorization boundary. Inspect repository instructions, status, relevant source, tests, configuration, and documentation before proposing a design. Prefer bounded searches and targeted reads; record the commands or files that support each important repository fact.

Separate observations from assumptions and unresolved questions. Do not invent behavior to complete the plan. Stop and request the missing decision when it changes public behavior, security, data handling, compatibility, or destructive scope. Stop on denied approval; do not try a different command or tool to bypass it.

Read `references/evidence-and-decisions.md` for the evidence, acceptance-criterion, and architecture-decision rules. Use `templates/delivery-plan.md` for the handoff structure.

## Define observable success

Write uniquely identified acceptance criteria. Each criterion must describe externally observable behavior or a verifiable preservation property, not an implementation preference. Include important failure behavior, compatibility boundaries, and unchanged-user-data requirements.

List at least two viable design options when a material design choice exists. Compare their repository fit, complexity, failure modes, migration or rollback cost, and validation path. Select one option and explain why. If only one option is viable, name the disqualifying evidence for the rejected alternative instead of pretending there was no decision.

## Produce an implementable handoff

Divide the work into ordered, independently reviewable slices. For every slice, map:

- the files or components expected to change;
- the intended behavior change;
- the acceptance-criterion IDs it advances;
- the exact check or observation that will validate it; and
- dependencies, permissions, or stop conditions.

Include risks, security and privacy considerations, compatibility limits, rollback or recovery steps, and documentation or release-handoff work. Preserve unrelated work and existing user files by default.

Finish with a durable checkpoint: inspected revision or state, first safe implementation action, commands still to run, unresolved decisions, and conditions that make the evidence stale. A future implementer must be able to resume by rechecking state rather than trusting the plan blindly.

## Review the plan

Trace every acceptance criterion to at least one implementation slice and one validation method. Trace every planned source edit back to a criterion. Remove speculative files and checks that do not serve the requested outcome.

Label evidence honestly. Repository inspection can support a plan; it cannot prove the future implementation, test result, performance, security, or live Bob behavior.
