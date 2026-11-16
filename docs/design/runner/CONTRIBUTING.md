# Contributing

This repository currently accepts design review, small specification changes, and proposed evaluation cases. It does not yet contain an implementation to install or exercise.

## Useful contributions

Describe a concrete failure: for example, a check passing before a final edit, a child process surviving cancellation, or a retry resetting a task's budget. Identify the affected requirement, propose an observable acceptance condition, and explain which evidence would distinguish success from failure.

For Bob capability claims, link an IBM primary reference, record when you checked it, and distinguish documented behavior from behavior observed on a particular client version. Do not infer Shell support from IDE support or infer a compatible API from similar terminology.

Keep example tasks small and synthetic. Never submit keys, authentication files, customer code, private repository paths, unreviewed command output, or environment dumps. Redact identifying information in a proposed test report while retaining the steps needed to reproduce its logic.

## Review requirements

- Keep proposed behavior labeled as proposed until it exists and has evidence.
- Update the state table, contract explanation, and evaluation plan together when a change affects transitions or evidence validity.
- Explain how a process stops, how interrupted state is recovered, and how an action obtains authorization.
- Avoid adding settings writers, hooks, provider adapters, or automatic retry loops without a reviewed scope and acceptance cases.
- Do not label a fixture definition as a passing test or a documentation review as a Bob integration test.

Complete the [build-versus-adopt decision](ROADMAP.md) before executable work. If a separate controller is justified, its first executable contribution should be a reviewed change implementing the offline contract validator and state transitions. A Bob adapter should wait until local supervisor and state-integrity requirements have been exercised.

By submitting original work, you agree to its inclusion under the repository's MIT license. Linked third-party material is referenced, not relicensed.
