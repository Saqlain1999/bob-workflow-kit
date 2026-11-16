# Validation record

Prepared 10 October 2026; source evidence last refreshed 17 October 2026 (Europe/Dublin).

## Source review

The catalogue now contains ten entries, including Verified Codebase Context, Bob Control, and Headless Bob. Primary sources are recorded in [catalog/projects.json](catalog/projects.json); the [comparison review](docs/comparison-review.md) identifies inspected commits and limitations. Commit identifiers were confirmed through GitHub commit endpoints. Repository availability, documented features, representative implementation, and license scopes were inspected. The 17 October refresh resolves Spec Kit's annotated `v1.2.1` tag to release commit `9dca9bf42a031765ee5e5f2371137f2f26967e11` and records its source-level workflow-capture and catalogue-trust guidance. No listed project was installed or executed by this catalogue, and no live Bob compatibility is claimed.

The Bob+ tree contains a skills ZIP and `bob-plus-assets-1.1.0.vsix`; neither was executed, and the binary was not downloaded. A focused 15 October review records the Granite TTM skill merged the previous day, its three documented inference paths, and the difference between source evidence and runtime proof. A 16 October follow-up records the upstream generated catalogue entry and archive link; the archive was not downloaded, extracted, or inspected. No skill was installed, no model weights were downloaded, and no watsonx.ai or local model call was made. The review records the tree's root Apache-2.0 and skills-subtree MIT notices, documentation drift, and the skill installer's source-level backup mismatch. Upstream test totals, performance numbers, and runtime outcomes were not independently reproduced. Maintainer execution reports remain attributed source links rather than structured catalogue runtime records.

## Local checks

Executed on Linux with Python **3.12.14** during preparation. Python 3.10 is the source compatibility target; no Python 3.10 execution is claimed.

`python3 tools/validate_catalog.py` exited **0** after the comparison update and reported:

```text
Validated 10 project entries, 11 Markdown files, and 29 local links.
External sources and Bob runtime behavior were not tested by this command.
```

`git diff --check` also exited **0**. No validator source change or upstream execution was required for these content updates.

During initial preparation, an additional in-memory/disposable-fixture check confirmed rejection of four invalid cases: a runtime claim without evidence, a duplicate project, a credential-bearing source URL, and missing local file/heading targets. It exited **0**. No upstream installer, model, or work repository was used. The comparison update changes catalogue content and documentation; the validator implementation is unchanged.

The command checks metadata and inline local Markdown paths/headings. It does not fetch external links or establish that their contents remain accurate. Repository URLs and technical facts need human review.

## Hosted CI and publication

The [GitHub Actions workflow](.github/workflows/validate.yml) uses the official [checkout](https://github.com/actions/checkout) and [setup-python](https://github.com/actions/setup-python) actions pinned to v7 commit references, read-only repository permissions, and no Bob credentials.

[GitHub Actions run 38008136347](https://github.com/Saqlain1999/awesome-bob-workflows/actions/runs/38008136347) completed successfully for published commit `c57876a4e6c3d1a8f894c795d12bf99fa63068ce` on 10 October 2026 (UTC). The `catalogue` job passed on `ubuntu-latest` with Python 3.12. This validates the catalogue's own metadata and local links; it does not install or execute any listed project.

That hosted run predates the expanded comparison content. The expansion passed [GitHub Actions run 38027939652](https://github.com/Saqlain1999/awesome-bob-workflows/actions/runs/38027939652) for commit `d88cacdb4ca3c06ad43375182d932a8fedd9e05a` on 10 October 2026 (UTC). The Ubuntu/Python 3.12 catalogue job and its **Check metadata and local links** step completed successfully. This remains catalogue validation, not execution of the listed projects.

The catalogue and companion repositories are now public. Publication and catalogue CI do not change the listed projects' runtime-evidence labels.
