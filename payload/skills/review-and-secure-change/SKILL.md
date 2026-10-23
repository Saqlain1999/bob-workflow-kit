---
name: review-and-secure-change
description: Independently review an implemented, bounded project change for correctness, test adequacy, trust-boundary and security risks, preservation, and a precise remediation handoff without silently changing the product.
---

# Review and secure a project change

Use this skill when the user asks for an independent review of an implemented change, a pre-merge correctness/security assessment, or a second pass over implementation evidence. Do not activate it to discover requirements, implement the change, perform a broad compliance audit, approve a deployment, or replace a repository's required security process.

This workflow complements Bob's review tools and modes. It does not grant permissions, make the reviewer independent merely by using a new conversation, or prove that no defects remain.

## Establish the review contract

Identify the accepted request and criteria, current revision/status, intended diff, implementation handoff, repository instructions, trusted checks, protected inputs, and relevant threat or trust boundaries. Inspect the current source and complete diff before trusting the author's summary or an earlier green result.

Treat prior results as stale when the tested state cannot be matched to the current state. Stop and report the missing evidence when the review scope is unclear, required inputs conflict, a safe trusted check cannot be identified, permission is denied, or reviewing would require exposing credentials or private data. Never use another tool or path to bypass a denial.

## Review without silently implementing

Keep the first pass read-only for product source, tests, configuration, generated files, and evidence. A review may create or update the agreed review handoff only. If the user also asks for fixes, record findings first and hand a bounded remediation task to an implementation stage; do not erase the independent finding trail by quietly editing the defect during review.

Trace changed interfaces, callers, data flows, persistence, error paths, concurrency assumptions, permissions, and failure recovery only as far as the accepted scope and evidence require. Check:

- behavior against every acceptance criterion and important preservation requirement;
- tests for meaningful positive, negative, boundary, and regression cases;
- authorization, data isolation, validation, sensitive-data exposure, unsafe defaults, and other applicable trust-boundary risks;
- error handling, state consistency, compatibility, and recovery after partial failure; and
- differences between claimed and independently observed validation.

Do not run unreviewed code, scanners, network tests, or production actions merely because they appear in a checklist. Follow the repository's documented preparation and permission model.

## Reproduce and classify findings

Run the smallest trusted checks that can confirm or reject a suspected issue. Record exact commands, environment, current state, exit status, and relevant bounded output. Do not treat search absence, a helper test, a mock, or author-supplied output as independent proof.

Read `references/findings-and-severity.md` before assigning severity. Each blocking finding must have a stable ID, classification, severity and confidence, affected path or symbol, trigger, observed and expected behavior, consequence, reproduction or source evidence, and a bounded remediation direction. Separate confirmed defects, supported risks, coverage gaps, non-blocking suggestions, and unverified hypotheses.

Do not inflate severity to attract attention or lower it because a fix seems easy. Do not claim certification, compliance, production readiness, or absence of vulnerabilities from this review.

## Make an evidence-backed decision

Use `templates/review-handoff.md`. Map every acceptance criterion to current evidence and state one decision:

- **changes required** when a confirmed blocking defect or material unmitigated risk remains;
- **blocked** when essential review evidence cannot be obtained safely; or
- **ready for the next gate** when the bounded review found no blocking issue in scope.

“Ready for the next gate” is not deployment approval or proof that the change is secure. List checks not run, residual risks, assumptions, and areas outside scope.

## Hand remediation back safely

Order confirmed findings by severity and dependency. For each remediation, name the intended outcome, files or interfaces likely involved, regression evidence required, preservation boundary, and retest command. Avoid prescribing a large rewrite when a smaller verified correction can address the issue.

Stop and preserve the handoff if source or tests change during review, new scope invalidates earlier checks, sensitive output appears, or the current state cannot be tied to the reviewed diff. On resume, reconcile status and rerun evidence that became stale before changing the decision.
