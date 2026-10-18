# Installer behaviour

The installer is a Python 3.10+ standard-library program at `tools/bob_workflow.py`. It manages this repository's known payload only. It does not run Bob, make network requests, install dependencies, or change authentication and permission settings.

## Commands

All paths below are relative to the selected Bob home, which defaults to the current user's `.bob` directory. Supply an explicit absolute `--bob-home PATH` for another target.

| Command | Writes? | Purpose |
| --- | --- | --- |
| `preview` | No | Validate source payload and inspect destinations, ownership, local edits, and proposed changes |
| `install` | Yes, after successful preflight | Create the packaged rule, named skill files, and this kit's ownership metadata |
| `doctor` | No | Compare installed files with recorded hashes and identify a missing or interrupted installation |
| `uninstall` | Yes | Remove unchanged owned files, or roll back a journalled partial installation |

`--help` and module import do not install anything. JSON output separates command status and local file facts from `client_loading_not_tested: true`. The process exit code is 0 for a successful command outcome, 1 for a reported condition such as not installed/conflicts, 2 for an operational/validation error, and 130 for a handled interruption.

`doctor` checks the installed files against their installation record. It does not inspect your full repository, prove the adequacy of project tests, or attest that Bob followed the workflow. Read the recorded installed version separately from the current package version.

## Managed locations

- `rules/bob-workflow-kit.md`
- `skills/work-large-codebase/SKILL.md`
- `skills/write-clear-technical-content/SKILL.md`
- Supporting text assets under each named skill's `references/` and `templates/`
- `workflow-kit/manifest.json` and a temporary `workflow-kit/journal.json`

The metadata directory is a kit convention outside the rule/skill discovery directories. No existing shared JSON configuration or `AGENTS.md` is merged or replaced.

Manifest and journal paths are validated against this narrow managed scope and the two enumerated skill names. An extra skill directory inside the source payload is rejected rather than becoming implicitly trusted. Absolute paths, traversal, unexpected destinations, and unsupported filesystem redirections are rejected. A same-name unowned file is a conflict even if its contents happen to match. Files are bounded UTF-8 text, not an arbitrary package payload.

## Install and reinstall

Installation performs a full preflight before publishing payload files. It stages complete files under `workflow-kit/`, records intended ownership in a journal, publishes through create-if-absent hard links, then writes the manifest and removes the journal. File identity is recorded before publication to support interruption cleanup. Existing files are never replaced by that operation.

The filesystem must support the required hard-link operation and usable file identity across the selected metadata/payload paths. If it does not, installation fails and reports rollback/recovery state; it does not fall back to overwriting a destination. Network shares, removable filesystems, and redirected homes require their own testing.

An identical package/version over an unchanged installation returns `unchanged`. Missing or edited managed files are reported. A different version or payload requires uninstalling the unchanged previous installation before installing the new package. This alpha deliberately has no automatic overwrite, merge, or upgrade-backup engine.

Keep a separate copy of intentional customisations before resolving a conflict. When a file has been edited, the installer cannot decide whether that edit should become an upstream contribution, a project override, or a different local rule.

## Interrupted installation

Caught failures trigger cleanup of files the transaction created. The output reports whether rollback completed. If termination prevents cleanup or a file changes during cleanup, a journal may remain.

1. Stop any still-running installer for the same target.
2. Run `doctor` with the original `--bob-home` value and inspect its status.
3. Run `uninstall` against that target to remove the unchanged journalled files.
4. Resolve any preserved local modification explicitly, then retry preview/install.

Do not erase a journal merely to force installation through. It records which paths the transaction intended to create. If metadata is corrupt or ambiguous, inspect the reported files and seek a reproducible repair rather than deleting the entire Bob configuration directory.

The installer is intended for one configuration operation at a time on a trusted local filesystem. It is not an operating-system sandbox or protection against a malicious process concurrently rewriting paths or metadata. Its interruption tests and limitations are recorded in the validation material.

## Uninstall

Uninstall validates all ownership records and checks local edits before deleting files. A modified managed file stops the ordinary removal preflight, preserving the installation. Missing files are tolerated so interrupted removal can be retried. During removal, hashes are checked again before individual deletions.

Only empty directories recorded as created by the installation are eligible for cleanup. Shared/nonempty directories and unrelated files remain. The selected Bob root itself is not recursively removed. Running uninstall again after completion reports that the kit is not installed.

If removal is interrupted, inspect the reported paths and retained metadata, then retry with the same target after stopping other operations. Do not interpret a partial removal as a completed uninstall. A hard termination may leave staging files under `workflow-kit/`; recovery preserves and reports nonempty directories rather than recursively deleting them.

## Test isolation

All functional installer tests use explicit temporary Bob roots. The test suite exercises read-only commands, conflicts, ownership, local edits, path validation, atomic publication, and interruption/recovery. It neither changes the real home variables nor invokes a live model. See [VALIDATION.md](../VALIDATION.md) for the executed environment and results.
