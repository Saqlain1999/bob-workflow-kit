# Manual acceptance checklist

Complete this after the helper result. Deterministic checks are necessary but
not sufficient.

- [ ] The reviewer reconciled current source/tests and the remediation handoff with the accepted request/plan and historical review/release records.
- [ ] Product source, trusted tests, implementation evidence, and historical blocked records remained byte-identical during re-review.
- [ ] REV-001 remains High in the historical record and is now marked resolved only with equality-filter source evidence and owner-isolation behavior evidence.
- [ ] REV-002 remains Medium in the historical record and is now marked resolved only with generic-conflict source and exception-text evidence.
- [ ] The review distinguishes resolved historical findings, new findings, and untested scope rather than reporting a superficial approval.
- [ ] Exact current command, 12/12 result, exit status, complete-diff inspection, and candidate-test preservation are recorded.
- [ ] Process-safe concurrency remains unknown; no helper result is treated as a general security or production-readiness proof.
- [ ] The only permitted output is `REMEDIATION_REVIEW.md`, with the decision `ready for release preparation` when the bounded gate passes.
- [ ] The decision does not authorize release, tag, artifact, deployment, publication, or announcement.
- [ ] Stop/recovery guidance covers permission denial, changed protected inputs/tests/source, failed checks, stale evidence, and preservation of unrelated work.

A pass does not establish that an unseen participant will review arbitrary
remediations correctly or that Bob selected or followed a particular skill.
