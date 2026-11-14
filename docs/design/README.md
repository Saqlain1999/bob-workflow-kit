# Deferred design notes

The [preserved runner design](runner/README.md) is reference material, **not an executable controller, another product to install, or a committed build plan**.

The kit works through Bob's existing capabilities. Only pursue a new runtime if observed client/workflow trials demonstrate a specific unmet need. Complete the existing [build-versus-adopt decision](runner/ROADMAP.md) first; adopting an existing runtime, contributing a narrow change or doing nothing are valid outcomes.

Original design documents remain unchanged for source/history preservation. Their references to companion repositories describe the original layout. The current intended entrypoint, exercises and quality command are all in [the kit](../../README.md). This consolidation adds no service, scheduler, MCP server or live model calls.
