# Catalogue metadata

The canonical entry data is [catalog/projects.json](../catalog/projects.json). The README provides the human browsing view; changes to an entry should update both when the description or status changes.

The editable [project template](../templates/project-entry.json) contains placeholders. It is intentionally not a live entry and is not validated as one.

## Top-level fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1` for this format |
| `reviewed_on` | Date of the catalogue's most recent recorded source review, `YYYY-MM-DD` |
| `review_timezone` | The timezone used for the dates; initially `Europe/Dublin` |
| `entries` | List of independently reviewable project records |

## Entry fields

| Field | Requirement |
| --- | --- |
| `id` | Unique lowercase slug containing letters, digits, and single hyphens |
| `name` | Upstream project name |
| `category` | One of `specifications`, `learning`, `skills`, `distribution`, `onboarding`, `debugging`, `orchestration`, or `evaluation` |
| `repository` | Public HTTPS source repository URL; a distinct application in a larger repository may use its source-subdirectory URL; no credentials |
| `summary` | Original factual one-sentence description |
| `publisher_type` | `organization` or `community`; describes the publisher, not endorsement |
| `license` | Observed SPDX identifier or expression, or `NOASSERTION` if it cannot be established; explain separate asset scopes in `notes` |
| `license_evidence` | Primary HTTPS page supporting the license observation |
| `availability` | `public-source` for this initial catalogue format |
| `installation` | `documented` or `not-assessed`; never means independently installed |
| `bob_relation` | `explicit-integration`, `bob-example`, or `bob-extension` |
| `review_status` | `documentation-reviewed` or `runtime-report-linked` |
| `reviewed_on` | Date the cited source facts were inspected |
| `runtime_evidence` | Empty for documentation-only entries; otherwise one or more reports described below |
| `notes` | Concrete compatibility, availability, or review limitations |
| `sources` | Primary HTTPS URLs paired with a `supports` description of the relevant claim |

Source evidence must include the repository and the page used for the license observation. A full Bob version or product support level is not inferred from the existence of a similarly named configuration directory.

Record the reviewed source revision in `notes` and use commit-pinned URLs in `sources` when available. The existing schema does not have a separate source-review revision field. A release tag or main snapshot describes the inspected material, not a compatibility result. When the Bob relationship is through a host tool such as Spec Kit, name that relationship explicitly and state whether the extension itself has been exercised with Bob.

## Runtime reports

Each runtime report has these fields:

| Field | Meaning |
| --- | --- |
| `date` | Date of the reported execution |
| `bob_version` | Exact version as observed, not “latest” |
| `surface` | Client or interface used, such as IDE or Shell |
| `platform` | OS and execution host details sufficient to understand the result |
| `source_revision` | Commit, release, or other immutable source identifier |
| `task` | Reproducible task and relevant verification scope |
| `result` | `passed`, `partial`, or `failed` |
| `evidence_url` | Public HTTPS report with commands, outcomes, and limitations |

A linked report is attributable evidence, not a claim that the catalogue maintainers repeated it. No structured runtime reports are currently included. A maintainer report can be listed as a source with explicit attribution without being promoted to `runtime-report-linked` until its exact version, revision, environment, task and result have been assessed against these fields.

## Validator limits

The standard-library validator checks these structural rules and local Markdown file/heading targets. It also rejects duplicate IDs or repositories and entries absent from the README.

It does not connect to the internet, verify license interpretation, inspect upstream code, validate the truth of a runtime report, or prove Bob compatibility. Human review remains necessary for source accuracy. The JSON template and issue forms are contributor aids, not machine-generated endorsements.
