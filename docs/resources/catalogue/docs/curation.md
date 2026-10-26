# Curation policy

## Scope

Include public projects that help people use IBM Bob for development workflows: specifications, skills, setup, repository onboarding, investigation, verification, and repeatable examples. A general tool can qualify when a primary source explicitly documents its Bob integration.

A preset or extension for such a tool can qualify when its host relationship is clear. Cite both the extension's contract and the host's Bob integration, and label any missing Bob-specific execution evidence. Host integration alone does not establish that the extension works with Bob. Native Bob features belong in the product-reference section, separate from open-source package entries.

Prefer a small useful entry over a long list of names. Each entry should answer what it provides, why it belongs here, what can be inspected, and what remains unverified.

## Inclusion evidence

An entry needs an inspectable public repository, a direct source for its relationship to Bob, a review date, and clear licensing evidence or `NOASSERTION`. The source should be the maintainer's repository, official documentation, or an author's own implementation description.

A repository being public does not itself grant a reuse license. A license visible at the repository root may have narrower asset-specific exceptions. Record the scope you can establish.

Do not substitute a similarly named product for an unverified project. Do not promote a product name, a search snippet, a demo request page, or an uninspected download into a public-source entry. Such suggestions can remain in an issue while contributors find the exact source.

## Evidence levels

- `documentation-reviewed`: a contributor inspected primary sources. It includes no runtime claim.
- `runtime-report-linked`: the entry also links a reproducible report identifying the exact revision, Bob version, interface, platform, task, and result. The report may describe a failure or partial result.

Installation is recorded separately as `documented` or `not-assessed`. The first describes available upstream instructions, not successful installation.

Keep source review and runtime evidence separate. A project can publish useful code, have good setup instructions, and still be untested with the contributor's current Bob version. A maintained CI workflow is evidence of the workflow's contents until an actual run is inspected.

## What not to claim

Avoid guaranteed correctness, broad enterprise readiness, universal compatibility, independent security certification, unmeasured productivity improvements, or ongoing vendor support without direct evidence. Do not infer active maintenance from a recent timestamp alone. Stars and download counts are not inclusion criteria.

Describe project features as documented features. If a contributor reports running something, identify their environment and result. Preserve a failure report rather than rewriting it as an endorsement.

## Review and correction

Review changed entries when a concrete trigger appears: a broken link, renamed project, license change, release that changes configuration, credible incompatibility report, or a new runtime report. Update `reviewed_on` only after inspecting the relevant sources again.

The offline validator cannot determine whether an external page is still reachable or accurate. During human review, open changed sources and check the facts they support. A date on an entry records an inspection; it is not a promise of scheduled monitoring.

If a project becomes unavailable, explain what changed in an issue or pull request. Remove or revise the entry with a short reason in the commit or PR, without speculating about the maintainer.

## Neutrality and attribution

Disclose authorship, employment, or another relevant affiliation when submitting a project. Use original concise descriptions and link to the source. Preserve required notices if any upstream text or code is reused. Vendor and community projects are held to the same evidence standard.

Catalogue maintainers can reject an entry for poor evidence, duplication, misleading claims, or scope mismatch. That decision concerns the entry, not the people behind the project.
