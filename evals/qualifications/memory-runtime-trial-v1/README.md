# Project-memory runtime trial protocol

This protocol makes a later Engram or Basic Memory trial comparable and
fail-closed. It binds a result to one reviewed backend profile, the exact
published asset digest, the ten `bob-project-memory-v1` behaviours, observed
side effects, cleanup, and explicit evidence limits.

It is an evidence protocol, not permission to run software. The template keeps
execution unauthorized and every behaviour `not_run`. The validator reads JSON
only: it does not download an asset, write Bob settings, start a process, call a
model, or contact a service.

## Before an authorized trial

1. Use a disposable project containing only the constructed public fixture.
2. Obtain separate authorization to download or execute the reviewed third-party
   artifact.
3. Independently verify the artifact digest against the selected profile.
4. Review the disabled project-only STDIO preview and retain manual tool
   approvals. If Bob is used, use an interactive IDE or Shell session and
   record the client mode, version, and explicit folder-trust decision. Bob
   Shell non-interactive sessions are outside this first protocol because
   [their tools are pre-approved](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive),
   which conflicts with the manual-approval safeguard.
5. Copy [`memory-runtime-trial-template.json`](../../results/memory-runtime-trial-template.json)
   outside the candidate workspace and fill it from observed evidence.

Record process, file, network and model-download effects even when the observed
answer is “none”; include how each observation was made. Record MCP server
instructions returned during initialization separately because current Bob IDE
can forward them into the system prompt. Exercise the same ten behaviours for
each backend. Keep repository evidence as the outage fallback.
Stop on a digest mismatch, global-setting requirement, cross-project disclosure,
instruction-like stored content changing control flow, a stale write being
accepted, dishonest outage success, or incomplete deletion.

Validate a record from the repository root:

```sh
python3 scripts/validate_memory_trial.py path/to/trial.json
```

Exit `0` means the record is internally consistent with its decision. It does
not mean the backend qualified: inspect the emitted decision. Exit `2` means
the evidence record is invalid or overclaims its observations.

`qualified` is intentionally narrow. It requires all ten behaviours to pass,
successful cleanup, and complete side-effect evidence. It never means production
ready. Every executed IBM Bob record—including a blocked or incomplete
trial—requires an observed interactive client mode and version, explicit
workspace trust, and `live_bob_observed=true`. This records where the evidence
came from; it does not turn a blocked or incomplete result into backend
qualification. Direct MCP records must instead mark workspace trust as not
applicable. Every executed record also names its operating system and
architecture. Backup erasure, privacy/licence compliance, durable multi-process
safety and production readiness remain separate gates.
