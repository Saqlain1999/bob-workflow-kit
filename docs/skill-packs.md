# Skill packs: selection and evidence

The kit packages focused Bob skills, not a universal prompt collection. IBM's current IDE and Shell documentation recommends clear activation descriptions, focused instructions, supporting files, and one responsibility per skill. Each packaged skill must therefore solve a named user problem without making every Bob conversation carry its full instructions.

## Included skills

| Skill | Activate it for | Do not treat it as |
| --- | --- | --- |
| `work-large-codebase` | Repository onboarding, substantial changes, and recovery from an interrupted task | A controller, code index, or guarantee that Bob read every relevant file |
| `write-clear-technical-content` | Drafting or revising technical procedures, errors, runbooks, handoffs, API text, and agent messages | Certified ASD-STE100 output, a semantic-equivalence proof, or a technical-correctness check |
| `plan-project-change` | An ambiguous or multi-file feature, refactor, migration, or integration that still needs requirements and design decisions | A source-code implementation, proof that the design works, or a reason to delay an already-bounded direct edit |
| `implement-and-debug-change` | An accepted bounded change, reproducible defect, or interrupted implementation with defined expected behavior | Requirements discovery, architecture selection, independent final review, deployment, or production-readiness approval |

All four skills are installed under the standard global `~/.bob/skills/` location. Bob uses each description to decide whether the skill is relevant, and current clients request approval before activation unless the user changes that setting. A project skill with the same name takes precedence over the global copy.

## Why the communication skill is bounded

The skill uses controlled-language ideas that are valuable beyond aerospace writing: stable terms, explicit actors, direct verbs, small procedural steps, and careful handling of ambiguity. Its most important addition is a semantic-fidelity pass that protects numbers, units, commands, identifiers, conditions, negation, and requirement strength.

It does not include or claim to implement the official ASD-STE100 dictionary. It does not claim ASD-STE100 compliance. A structural style rule or linter cannot prove that a rewrite preserved meaning.

The design review used two public, MIT-licensed sources as evidence, without copying their prompt libraries into this kit:

- [`danyuchn/asd-ste100-skill` at `3944283c183eea13fe5bd902b572da3b4de8bf44`](https://github.com/danyuchn/asd-ste100-skill/tree/3944283c183eea13fe5bd902b572da3b4de8bf44) demonstrates a controlled-language rewrite skill and explicitly documents the limits of structural linting, dictionary redistribution, and semantic verification.
- [`msitarzewski/agency-agents` at `652b2692f8d8ec2b1f1a38e559073e287dfdc469`](https://github.com/msitarzewski/agency-agents/tree/652b2692f8d8ec2b1f1a38e559073e287dfdc469) demonstrates explicit roles, deliverables, handoffs, and evidence gates across a large agent catalogue. The kit adopts that separation of inputs, process, output, and evidence—not the collection's personas, commands, or tool assumptions.

The resulting skill text and examples are original to this repository. The upstream links are review provenance, not bundled dependencies or compatibility claims. Neither upstream project was installed or executed for this review.

## Why the planning skill is bounded

`plan-project-change` stops before product-source edits. It turns current repository evidence into observable acceptance criteria, an explicit design choice, criterion-to-file/check traceability, and a checkpoint that another session can revalidate. It adapts the useful input/process/output and handoff discipline seen in the pinned Agency Agents review without importing personas or prompt text. A good plan remains a proposal: it does not prove that implementation, tests, security, performance, or live Bob activation will succeed.

## Why the implementation skill is bounded

`implement-and-debug-change` starts only after expected behavior is bounded. It requires a current reproducible baseline, minimal criterion-linked edits, regression evidence, preservation review, and a resumable handoff. It complements Bob's native Agent mode rather than replacing modes, permissions, rollback, or task history.

The 22 October 2026 review of [`msitarzewski/agency-agents` at `4e3ac3ca6604c75113f52c695dbddcc7af928b46`](https://github.com/msitarzewski/agency-agents/tree/4e3ac3ca6604c75113f52c695dbddcc7af928b46) found useful minimal-diff and evidence-reporting patterns. This kit adapts restraint, line-of-evidence, and explicit untested-scope ideas into original stack-neutral instructions. It rejects hard-coded Laravel/FluxUI/visual-QA assumptions, unmeasured numeric success targets, persona identity text, and bulk agent import. The upstream remains an MIT-licensed review source, not a dependency; it was not installed or executed.

## Gate for another skill

Add a skill only when all of the following are true:

1. A real Bob task has a repeatable failure or quality gap.
2. The responsibility is distinct from an existing skill.
3. The activation description can exclude unrelated tasks.
4. The workflow names inputs, outputs, evidence, and stop conditions.
5. Supporting material is original or reusable under a verified licence.
6. Offline structure and installer lifecycle tests pass.
7. A public fixture and acceptance criteria can evaluate behavior separately from installation.

Static tests can establish that a skill is well-formed and safely installed. A recorded live trial is still required before claiming that a Bob version discovered the skill, selected it correctly, followed it, or improved task outcomes.

## Next candidates

The next useful pack may cover independent evidence-first review and security. It should not be added merely to make the catalogue larger. First build a public fixture that exposes a failure the new skill should prevent, compare the same task with and without the candidate, and retain results that do not support the idea.
