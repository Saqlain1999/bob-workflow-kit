# Basic Memory v1.0.0 qualification gate

This record maps the backend-neutral project-memory contract to the exact Basic
Memory v1.0.0 release without installing or executing it. It gives a later
disposable runtime comparison exact inputs, isolation boundaries, stop
conditions, and evidence gaps.

## Reviewed source

- Repository: <https://github.com/basicmachines-co/basic-memory>
- Tag: `v1.0.0`
- Commit: `c9bd187b83baba549d5cd16bacc180f8023d51c8`
- Commit date and release published: 29 October 2026 (UTC)
- Licence: AGPL-3.0-or-later; copyright remains with the upstream authors
- Python requirement: 3.12 or later
- Reviewed wheel: `basic_memory-1.0.0-py3-none-any.whl` (1,883,480 bytes)
- Published wheel digest: `sha256:a2d2c1589616c9599aec9edd6597d508028c5af88632312fc0990dcaccf02867`

The exact mapping and source references are in [`profile.json`](profile.json).
No upstream code, package, script, skill, prompt, or documentation text is
copied into this repository. The AGPL licence and its obligations need an
appropriate review before distribution, modification, or service deployment;
this source record is not legal advice or permission to redistribute.

The upstream MCP registry example invokes an unpinned package. This gate instead
requires the reviewed wheel by absolute path. Upstream `SECURITY.md` also still
lists `0.x.x` as supported even though v1.0.0 is released, so support status is
treated as an unresolved documentation inconsistency rather than inferred.

## Decision

**Qualify after runtime evidence; do not adopt yet.** Exact v1.0.0 source has
useful controls: named project routing, project-root validation, local STDIO,
checksum-guarded edits and deletes, and project deletion disabled by default.
Those are stronger source-level candidates for project separation and stale
writer refusal than an unguarded memory store.

They do not establish the contract:

- package dependencies and optional model/cache downloads have not been
  resolved or observed;
- supersession history, source freshness, sanitized promotion, and outage
  fallback still need a bounded adapter;
- project isolation, atomic recovery, hostile-content handling, checksum races,
  and direct/indexed deletion still need disposable runtime evidence;
- local file deletion is irreversible, cloud deletion has different backup
  semantics, and the first trial deliberately excludes cloud mode;
- no Bob discovery, activation, approval, or workflow-following has run.

## Safe preview

The preview helper renders, but does not write, an isolated Basic Memory config,
a disabled project MCP entry, and the first read-only project-list call:

```sh
python3 scripts/preview_basic_memory.py \
  --project /absolute/path/to/disposable-project \
  --uvx /absolute/path/to/reviewed/uvx \
  --wheel /absolute/path/to/basic_memory-1.0.0-py3-none-any.whl
```

The output targets `<project>/.bob/mcp.json`, constrains Basic Memory to the
named local project, moves its configuration/cache under
`<project>/.basic-memory-state`, disables cloud routing, promos, Logfire export,
auto-update, project deletion, and all Bob auto-approval, and starts disabled.
It never creates a directory, writes either config, downloads or imports the
wheel, starts `uvx`, or sends the tool request.

The preview chooses text search for the first contract trial, but that does not
prove v1.0.0 avoids model or dependency downloads. Before execution, verify the
wheel digest independently, review and write both rendered files only in the
disposable project, explicitly trust that folder if Bob folder trust is active,
enable the one server manually, and retain individual tool approvals. Stop if
the release changes, a global or cloud setting is required, another project's
notes are visible, a stale checksum succeeds, or the repository-evidence
fallback is ambiguous.

Removal for this preview is trivial because it writes nothing. A future trial
must document removal of the project MCP entry, isolated config/database/logs,
downloaded dependency and model caches, indexes and any retained backups. That
procedure is intentionally not claimed before the lifecycle is observed.
