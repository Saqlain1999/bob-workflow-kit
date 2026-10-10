# Maintaining and releasing this alpha

Public repository: [Saqlain1999/bob-workflow-kit](https://github.com/Saqlain1999/bob-workflow-kit). Package version: **v0.1.0-alpha.1**, with the included MIT licence. A repository publication and a tagged GitHub release are separate operations. No package-registry name or Marketplace listing is claimed.

## What a reader should receive

A source archive or clone containing the complete guide, payload, installer/tests, prompts, fixture, compatibility notes, and validation record. The first page should make the installation path and alpha status clear.

## Before announcing this alpha

1. Confirm repository ownership and any additional maintainers; retain the community-project description.
2. Review the code, licence, documentation, and generated assets intended for publication.
3. Run the offline tests from the exact source being released.
4. Publish the existing validation limits clearly. Live Bob/OS combinations that have not run must remain marked untested.
5. Enable the issue forms and an appropriate private security-reporting channel if available; the included policy does not invent a contact address or response promise.
6. Inspect CI results for the exact commit being released. A passing local run is not a substitute for the macOS/Windows jobs.
7. Tag an alpha release, attach the archive and its SHA-256, and link the guide.

Live loading and real-project trials can be gathered during an explicitly labelled alpha. Broader stable compatibility claims require those results first.

## Historical first-publication example

This repository has already been published. The commands below document initial repository creation; updates should use the existing remote and a reviewed commit/push. These commands are not performed by the installer.

```sh
git init -b main
git add .
git commit -m "Initial Bob Workflow Kit alpha"
gh repo create Saqlain1999/bob-workflow-kit --public --source=. --remote=origin --push
```

Review `git status` and the staged diff before committing. The installer never calls these commands. GitHub CLI instructions are documented at [gh repo create](https://cli.github.com/manual/gh_repo_create).

Suggested GitHub description:

> Practical IBM Bob workflows for large codebases: reversible setup, focused context, task checkpoints, and verification evidence.

Suggested topics: `ibm-bob`, `developer-tools`, `agent-skills`, `developer-experience`, `workflow`, `documentation`.

## Announcement scope

Describe the concrete alpha contents and link to its validation. Invite reproducible compatibility reports and public examples. Credit relevant existing projects through the ecosystem guide. Do not imply IBM endorsement, a verified Propel integration, an official Marketplace listing, or guaranteed outcomes.

## Future maintenance

Update the compatibility review when Bob changes discovery or extension behaviour. Keep releases versioned and examples reproducible. Coordinate links and scope with the companion repositories described in [the roadmap](roadmap.md); keep their evaluation and controller maturity labels accurate.
