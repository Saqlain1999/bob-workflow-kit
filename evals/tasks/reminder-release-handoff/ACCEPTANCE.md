# Manual acceptance checklist

Complete this after the helper result. The deterministic checks are necessary but not sufficient.

- [ ] The participant reconciled current source, complete available diff, implementation handoff, independent review, trusted checks, and existing documentation.
- [ ] The historical implementation 10/10 result is labelled stale and is not carried forward as release evidence.
- [ ] `USER_GUIDE.md` says the candidate is unreleased, records both known blocking issues, and provides safe operator guidance without presenting intended behavior as current behavior.
- [ ] `RELEASE_HANDOFF.md` maps AC-1 through AC-4 and REV-001/REV-002 to current evidence, disposition, release effect, and next action.
- [ ] The exact decision is `release blocked`; no contradictory ready, tag, artifact, deployment, publication, or announcement claim appears.
- [ ] Current validation distinguishes reproducing the two defects from proving corrected behavior and records unrun live Bob, compatibility, performance, and process-concurrency scope.
- [ ] Product source, tests, request, plan, implementation/review handoffs, and team note remain byte-identical; only the two agreed documentation files changed.
- [ ] Recovery returns both findings to a bounded implementation stage, requires regression evidence and a new independent review, and states what would make evidence stale.
- [ ] No compliance, production-readiness, deployment-approval, broad compatibility, performance, or live-Bob claim is made.

A passing documentation contract does not establish that a participant will make correct release decisions on unseen projects or that Bob activated the intended skill.
