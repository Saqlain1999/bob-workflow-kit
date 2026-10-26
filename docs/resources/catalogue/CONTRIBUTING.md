# Contributing

Useful contributions make this catalogue more accurate or easier to use. You can suggest a project, correct a description, document a version-specific issue, or supply a reproducible runtime report.

## Add or update an entry

1. Read the [curation policy](docs/curation.md) and find a primary source showing the project's relationship to IBM Bob.
2. Open the repository, relevant documentation, and license evidence. Record exactly what you established.
3. Copy the fields from [templates/project-entry.json](templates/project-entry.json) into [catalog/projects.json](catalog/projects.json), replace every placeholder, and follow the [metadata format](docs/metadata.md).
4. Add or update a concise README entry in the appropriate category. Link the sources near factual claims.
5. Run `python3 tools/validate_catalog.py` from the repository root.
6. Open a pull request explaining the value, evidence, remaining unknowns, and any affiliation.

Do not change `review_status` to `runtime-report-linked` without a public reproducible report. A passing local metadata check says nothing about a project's runtime behavior. Contributors do not need to execute a third-party installer merely to propose a documentation-reviewed entry.

## Correct stale or misleading information

Identify the entry, the disputed statement, the supporting source, and what should replace it. For compatibility reports, include the exact Bob version, interface, source revision, operating system, and a minimal reproduction. Separate a failed installation from a runtime task failure.

Use the issue templates if you prefer to provide evidence before editing files. A narrowly scoped correction is welcome.

## Keep the catalogue useful

Write original descriptions. Keep claims specific. Do not add star badges, unverifiable performance numbers, affiliate links, bulk link dumps, copied secrets, or unrelated product promotion. Disclose if you authored, maintain, sell, or work on the submitted project.

Preserve failures and limitations in reports. Do not silently rewrite someone else's report into a successful test.

## Contribution terms

By submitting original contributions, you agree to provide them under this repository's MIT license. Do not submit material you cannot share under those terms. Linked projects retain their own licenses.

Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Consult [SECURITY.md](SECURITY.md) before posting sensitive information.
