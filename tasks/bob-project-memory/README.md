# Bob project memory v1

This small public exercise asks a participant to complete a backend-neutral
project-memory adapter and an evidence handoff. It covers two isolated projects
and one deliberately promoted shared lesson.

It measures whether the candidate state satisfies the twelve public contract
checks. It does not establish IBM Bob discovery, correct model use, an MCP
integration, production durability, privacy compliance, or the suitability of
Engram, Basic Memory, Honcho, or any other backend.

Use `python scripts/evaluate.py prepare --task project-memory --output <dir>`.
The prepared baseline must reproduce the named expected failures before a
participant starts. Candidate validation uses the original trusted tests and
accepts changes only to `memory_adapter.py` and `MEMORY_HANDOFF.md`.
