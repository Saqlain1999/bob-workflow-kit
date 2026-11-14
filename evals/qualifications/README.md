# Backend qualification records

These records turn the backend-neutral
[`bob-project-memory-v1`](../fixtures/bob-project-memory/README.md) contract into
reviewable backend-specific gates. A record is not an installer, endorsement,
live Bob result, or production-readiness claim.

Each backend record must pin the reviewed source and release, state its licence,
map every contract behaviour to evidence or a named gap, and keep installation
and execution outside this repository's offline test suite. Preview helpers may
render configuration, but must not write Bob settings, start a server, download
a binary, or call a model.

| Record | Decision | Evidence boundary |
| --- | --- | --- |
| [`engram-v0.11.0`](engram-v0.11.0/README.md) | Adapt only after runtime qualification | Source-reviewed profile and non-mutating Bob project-config preview; no Engram or Bob execution |
| [`basic-memory-v1.0.0`](basic-memory-v1.0.0/README.md) | Qualify only after runtime evidence | Source-reviewed profile and non-mutating, isolated Bob project-config preview; no Basic Memory or Bob execution |

Use the backend-neutral
[`memory-runtime-trial-v1`](memory-runtime-trial-v1/README.md) protocol for a
later authorized runtime trial. Its fail-closed validator binds a record to one
of these pinned profiles and the same ten contract behaviours. Adding the
protocol does not authorize or perform a download, installation, or execution.
