# Engram Alpha v0.11.0 qualification gate

This record maps the backend-neutral project-memory contract to a pinned Engram
Alpha release without installing or executing Engram. It exists so a later
disposable runtime trial has exact inputs, stop conditions, and evidence gaps.

## Evidence status after local correction

This is optional inert research and a disabled text preview, not a default
memory backend or permission to execute a trial. The following pin, dates,
license, source statements and asset digest are inherited recorded assertions.
Independent upstream/source/asset verification is **NOT RUN** in this correction;
no asset was downloaded. Static self-consistency tests do not authenticate them.
The internal preview contract uses `brief` with `{}` on the DB-pinned project;
this wording alignment does not verify or guess the actual upstream API.
Runtime/MCP/Bob qualification remains **NOT RUN**, with conflict/deletion blocked.

## Reviewed source

- Repository: <https://github.com/techtheist/engram>
- Tag: `v0.11.0`
- Commit: `ed4fe24d97f16f1c362d0c4d6b74bfe4d2caf0c3`
- Commit date: 31 October 2026 (UTC)
- Release published: 1 November 2026 (UTC)
- Licence: MIT; copyright remains with the upstream authors
- Reviewed Linux asset: `engram-alpha-v0.11.0-x86_64-unknown-linux-gnu.tar.gz`
- Published asset digest: `sha256:287708d36f27d72dca86d45ea40d269fd57525e8ab8a987c5cf00837998bf8d5`

The exact mapping and source references are in [`profile.json`](profile.json).
No upstream source, binary, script, persona, prompt, or documentation text is
copied into this repository.

## Decision

**Adapt after runtime evidence; do not adopt yet.** Source inspection supports a
bounded project-local STDIO trial with an explicit `brief` call against the
graph already pinned by `mcp --db`.
It does not establish the full contract:

- agent-facing hard deletion is deliberately absent, so direct and indexed
  deletion cannot be accepted until a safe user-owned removal path is observed;
- no optimistic expected-revision interface has been accepted for the contract's
  stale-writer refusal case;
- database interruption recovery, project isolation, hostile-content handling,
  outage fallback, and supersession still require disposable runtime evidence;
- no Bob discovery, activation, tool approval, or workflow-following has run.

## Safe preview

The preview helper renders, but does not write, a disabled project MCP entry and
the first explicit briefing call:

```sh
python3 scripts/preview_engram.py \
  --project /absolute/path/to/disposable-project \
  --binary /absolute/path/to/reviewed/engram-alpha
```

The output targets `<project>/.bob/mcp.json`, uses a project-local
`<project>/.engram/graph.db`, starts disabled, and grants no automatic tool
approval. It never creates directories, changes Bob's global configuration,
downloads or runs Engram, or sends the briefing request.

Exact v0.11.0 CLI source says `mcp` is a light bridge that can start a detached
machine-local core, and the bridge may append `.engram/mcp.log`. A runtime trial
must therefore observe core startup/status/stop behavior, loopback binding,
project registration, files created, model/download behavior, and cleanup. The
preview deliberately does not simulate or hide that lifecycle.

Before a live Bob trial, independently verify the downloaded asset against the
published digest, inspect the project config, explicitly trust only the
disposable workspace if folder trust is enabled, enable the one project server,
and approve tools individually. Stop if the pin or digest differs, the backend
touches another project/global setting, deletion cannot be demonstrated, or the
repository-evidence fallback becomes ambiguous.

Removal for this preview is trivial because it writes nothing. Removal after a
future trial must cover the reviewed `.bob/mcp.json` entry, the project-local
`.engram` data/logs, any machine registry/core process and derived index, and
backup limitations; that procedure is intentionally not claimed before it is
observed.
