---
name: document-and-prepare-release
description: Update technical documentation and prepare an evidence-backed release handoff for a reviewed, bounded change without publishing or hiding unresolved blockers.
---

# Document and prepare a release handoff

Use this skill when implementation and independent review evidence exist and the user asks to update user/operator documentation, assemble release notes, or prepare a bounded change for its repository's release gate. Do not activate it for requirements discovery, implementation, defect remediation, a general rewrite, release automation, deployment, publication, or a change whose accepted behavior is still unknown.

This workflow prepares evidence for a human or repository-defined release decision. It does not approve, tag, publish, deploy, or prove production readiness.

## Reconcile the release contract

Read the accepted request and criteria, current revision and complete diff, implementation handoff, latest independent review handoff, trusted checks, existing user/operator documentation, compatibility policy, versioning and changelog rules, and the repository's release instructions. Label observations, prior evidence, assumptions, unknowns, and checks not run.

Treat a check as current only when its tested state matches the state being documented. Stop and record the conflict when inputs disagree, a required review is missing, a blocking finding has no disposition, the intended release contents cannot be identified, a required check cannot run safely, permission is denied, or documentation would expose secrets or private data. Never use a different tool, credential, destination, or wording to bypass a denial or conceal a blocker.

Read `references/release-evidence.md` before making a release decision.

## Update documentation without inventing behavior

Keep product source and tests read-only. Change only the documentation and release-handoff paths agreed for this stage. Describe the current implementation, not the intended design or an earlier passing state.

For each affected audience, record only applicable facts:

- behavior changes and non-changes tied to acceptance criteria;
- prerequisites, exact commands, configuration names, versions, compatibility limits, and migration or upgrade steps;
- security, privacy, data-handling, failure, recovery, and rollback implications;
- known issues, unresolved findings, unavailable checks, and evidence limits; and
- removal or fallback steps that preserve user data and unrelated configuration.

Preserve identifiers, commands, numbers, conditions, negation, order, uncertainty, and requirement strength. Do not convert a proposed feature, passing helper, mock, historical result, or author claim into observed product behavior. Do not expose sensitive evidence in release notes.

## Decide the next gate honestly

Use `templates/release-handoff.md`. Choose exactly one decision:

- **release blocked** when a confirmed blocking finding remains, required acceptance behavior fails, a required migration or rollback path is unsafe, or essential release evidence is unavailable;
- **ready for release review** when the exact candidate state has current required checks, no unresolved blocking finding, complete required documentation, and an identified rollback or removal path; or
- **documentation blocked** when the documentation contract itself cannot be completed safely or accurately.

“Ready for release review” is not approval to tag, publish, deploy, or announce. Do not create a release note that implies readiness while the handoff says blocked. If blocked, document the current limitation for maintainers and users without presenting the candidate as available.

## Preserve evidence and recovery

Record the exact candidate revision or content identity, complete diff scope, commands, environments, exit status, bounded results, and links or paths to current evidence. Map every acceptance criterion, blocking review finding, required document, and release check to its status and next action. State explicitly when no release artifact, tag, deployment, migration, or rollback artifact exists.

Stop if product source, tests, version metadata, review findings, or required documentation changes unexpectedly. Preserve the incomplete handoff, list stale evidence, and name the first safe resume action. After any candidate edit, reconcile the new state and rerun evidence affected by the edit before changing the decision.
