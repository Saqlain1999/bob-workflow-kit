# Bob project memory fixture

This original, standard-library fixture defines a backend-neutral contract for
project memory. It uses two fictional projects and an explicit shared-lessons
scope. The starting `memory_adapter.py` is deliberately incomplete.

The exercise is about observable memory boundaries, not a particular database,
MCP server, model, or Bob client. It makes no network calls and stores only
constructed public data. Prepare a disposable copy through the repository
helper; do not repair this original fixture in place.

Protected inputs are `contract.json`, both files under `projects/`, and the
trusted tests. A participant may change only `memory_adapter.py` and
`MEMORY_HANDOFF.md`.

The corrected local gate adds declared-scope/delimiter checks, distinct writer
and reader processes, injected actual-save failures, and sequential stale-instance
refusal. The packaged adapter's defects remain intentional. See the
[acceptance boundaries](../../tasks/bob-project-memory/ACCEPTANCE.md) for manual
provenance, token-only freshness, outage coverage, and concurrency limitations.
Fixture green never qualifies a live backend.
