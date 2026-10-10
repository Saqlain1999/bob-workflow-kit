# Evaluation guide

Measure installation correctness and coding-workflow usefulness separately. No single test proves both.

## 1. Offline installer suite

From the repository root:

```sh
python3 -m unittest discover -s tests -v
```

The suite uses disposable explicit targets and does not call Bob. It checks configuration-writing behaviour and error handling. A passing result establishes those tested software properties on the executed environment; it does not establish live Bob compatibility.

## 2. Fresh-client loading

Install the kit, start a fresh Bob conversation, and use [verify.txt](../prompts/verify.txt). Record the exact interface/version and host. Verify the actual resolved rule/skill paths using available client evidence. Report unavailable introspection rather than guessing.

Use a project with a same-name override as a separate case when testing precedence. Keep the global and workspace cases distinguishable. Record permissions as observed; do not enable blanket execution merely to make an acceptance run pass.

## 3. Tiny Ledger exercise

The [fixture](../examples/README.md) uses only Python's standard library. Copy it into a disposable folder, read its README, and run:

```sh
python3 -m unittest discover -s tests -v
```

Run that command from the copied `tiny-ledger` folder. The shipped baseline deliberately has **nine tests with one failure**. Use its PROMPT.md as the coding request. A successful repair should preserve the public API and existing checks, fix the underlying behaviour, and complete all nine tests successfully.

The original fixture should remain broken for the next demonstration. Do not update the repository's baseline just because a trial succeeded. A missing test run or an edited-away assertion is not a successful repair.

This small task also checks proportionality: a direct repair should not require a large plan, an unnecessary agent team, or a checkpoint merely for ceremony.

## 4. A realistic recovery trial

The alpha supplies a recovery method and template, not a completed large-repository benchmark. Use a public multi-component fixture for a stronger trial:

1. Define a change spanning an interface, implementation, caller, and regression checks.
2. Fix the starting revision, dependencies, and acceptance criteria.
3. Ask Bob to investigate and complete one coherent milestone, then save a concise checkpoint.
4. Start a fresh conversation with only the relevant project instructions and checkpoint path.
5. Verify that the new session inspects current files, recognises stale results, and continues productively.
6. Run the required checks and inspect the complete diff against the original criteria.

If testing stale state, modify one relevant input between sessions and record that intervention. Evaluate whether the old check is treated as stale. Avoid copying the whole previous conversation into the new session because that would conceal whether the checkpoint was sufficient.

## 5. Compare fairly

Use the same task, starting state, machine/services, tool availability, permissions, and criteria in baseline and kit-assisted runs. Record model/mode choices and usage where the client exposes them. Repeat trials and publish failures alongside successes.

| Metric | Why it helps | Limitation |
| --- | --- | --- |
| Acceptance criteria met | Measures the requested outcome | Depends on the quality and coverage of criteria |
| Regression results and diff scope | Reveals collateral change | Tests and review can still miss defects |
| Recovery success | Measures continuity after interruption | A tiny task does not represent a large repository |
| Commands, files inspected, and output volume | Shows operational behaviour | Lower counts can mean under-investigation |
| Elapsed time and reported usage | Helps assess cost and efficiency | Environment, caching, model variance, and missing usage affect comparison |
| Manual interventions | Shows where autonomy needed help | Record whether the intervention was necessary or merely a preference |

Do not publish claims such as “40% faster” or “never loses context” without an appropriate experiment and evidence. The current results are documented in [VALIDATION.md](../VALIDATION.md).
