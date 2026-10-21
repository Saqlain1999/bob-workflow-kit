# Changelog

## 0.1.0-alpha.4 — unreleased

- Add the focused `plan-project-change` skill with an evidence/decision reference and durable delivery-plan template.
- Extend the fixed-scope installer to manage exactly three reviewed skills; arbitrary skill directories remain rejected.
- Define planning activation, non-activation, source-edit boundary, acceptance traceability, stop conditions, and interruption-safe resume evidence.

## 0.1.0-alpha.3 — unreleased

- Add the focused `write-clear-technical-content` Bob skill with on-demand fidelity and writing-pattern references.
- Preserve numbers, units, commands, identifiers, negation, conditions, sequence, uncertainty, and requirement strength during technical rewrites.
- Extend the fixed-payload installer and manifest validation to manage both named skills without accepting arbitrary skill directories.
- Document the evidence gate for future skill packs and the bounded design review of two public MIT-licensed sources.

Offline installer tests prove payload structure and lifecycle behavior only. They do not prove live Bob discovery, activation, semantic equivalence, technical correctness, or ASD-STE100 compliance.

## 0.1.0-alpha.2 — 2026-10-10

- Add one first-use walkthrough with a copyable Bob handoff, explicit success criteria, and a short feedback route.
- Add a comparison and coexistence guide covering native Bob, specification/context tools, and existing runtimes. Reuse existing project records and evaluate existing runtimes before building a separate controller.
- Link the companion Parcel Resume exercise for a constructed stale-evidence handoff, policy changes, preservation of teammate work, and independent candidate verification.
- Add a live trial record template, demo recording instructions, and an evidence-led launch plan.
- Correct the compatibility matrix to include the completed alpha.1 Windows, macOS, and Linux CI jobs with their exact source revision.
- Keep the installed rule/skill payload and installer ownership behavior unchanged. Bump the installer's reported version and check it against the package `VERSION` file. Updates still use the documented uninstall-then-install policy.

No live Bob execution or large-repository effectiveness result is included. Release notes identify checks for the exact tagged source; historical validation stays scoped to its original version.

## 0.1.0-alpha.1 — 2026-10-09

Initial community alpha.

- Add a practical IBM Bob guide and current ecosystem references.
- Add one concise global rule and a `work-large-codebase` skill with on-demand onboarding, change, and recovery references.
- Add repository-profile and task-checkpoint templates plus copyable setup/use prompts.
- Add an offline Python installer with preview, install, doctor, uninstall, owned-file integrity, conservative collision handling, and interruption recovery.
- Add 24 passing local installer tests and a deliberately failing Tiny Ledger exercise.
- Record a separate assistant trial of the written skill, without claiming live Bob runtime validation.
- Add compatibility/evaluation materials, issue templates, pinned CI definitions, and a roadmap for optional future components.

At initial preparation, live Bob, native macOS/Windows, and GitHub-hosted CI were untested. Hosted Linux/macOS/Windows installer jobs subsequently passed on 10 October; see the exact source and run in [VALIDATION.md](VALIDATION.md). Live Bob remains untested.
