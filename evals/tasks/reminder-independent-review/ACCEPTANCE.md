# Manual acceptance checklist

Complete this after the helper result. The deterministic checks are necessary
but not sufficient.

- [ ] The participant inspected current source/diff and treated the author
  handoff's historical 10/10 result as stale, not independent current evidence.
- [ ] Both seeded issues were independently reproduced: cross-owner disclosure
  and stored record content in the conflict exception.
- [ ] Each finding includes a justified severity/confidence, precise location,
  trigger, observed/expected behavior, consequence, evidence, remediation, and
  blocking decision.
- [ ] Product source, tests, request, plan, implementation handoff, and team
  notes remain byte-identical; only `REVIEW_HANDOFF.md` changed.
- [ ] The review distinguishes confirmed defects, residual risks, coverage
  gaps, and areas not assessed.
- [ ] The decision is `changes required`, and the remediation handoff returns
  work to a bounded implementation stage with required regression evidence.
- [ ] Process concurrency remains a residual untested risk rather than an
  invented third reproduced defect.
- [ ] No certification, compliance, release approval, production readiness,
  absence-of-vulnerabilities, or live Bob claim is made.
- [ ] Any unavailable command, intervention, or changed review input is
  recorded with its effect on the decision.

A passing report-format check does not prove that a reviewer would find unseen
defects in another project or that Bob activated the intended skill.
