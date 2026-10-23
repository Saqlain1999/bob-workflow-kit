# Try the alpha

**Goal:** install the kit, find out whether your Bob client loads it, and finish one small repair with evidence you can inspect. You need only this repository for the first exercise.

This is a community alpha. Offline installation checks are recorded in [VALIDATION.md](../VALIDATION.md). A successful installer result and a successful Bob task are separate observations. No setup can guarantee that an agent never makes a mistake.

## 1. Get a fixed copy

Download the source ZIP from [Releases](https://github.com/Saqlain1999/bob-workflow-kit/releases) and extract it. Prefer a named alpha release when reporting a result. Its notes identify the exact commit and archive checksum. A clone also works; record `git rev-parse HEAD`.

Prerequisites are an existing Bob IDE or Shell installation and **Python 3.10 or later** on the host where you will run the installer. The commands below use `python3`; on Windows with the Python launcher use `py -3` instead. Check your interpreter with `python3 --version` or `py -3 --version`.

Open the extracted **kit directory** in Bob first. You will open a separate exercise directory later. If you run Bob remotely, determine which host owns its configuration before installing.

## 2. Preview, install, and inspect

To let Bob perform setup, paste the contents of [try-alpha.txt](../prompts/try-alpha.txt) in an Agent conversation. It uses the included installer and ends with the fresh-session handoff.

To operate the installer yourself, run from the kit root:

```sh
python3 tools/bob_workflow.py preview
python3 -m unittest discover -s tests -v
python3 tools/bob_workflow.py install
python3 tools/bob_workflow.py doctor
```

Read the preview **before** running install. It shows the actual target and collisions. The offline test suite uses disposable targets and should pass. `doctor` should report the managed files' installation and integrity state.

The default is the current user's `.bob` directory. If Bob uses a different configuration directory, append the same `--bob-home /absolute/path/to/.bob` to preview, install, and doctor. For an installation-only rehearsal use an explicit temporary directory; Bob will not discover that temporary target automatically.

An edited managed file or an unowned collision needs review. Do not delete it simply to get a green result. [Installer troubleshooting](troubleshooting.md) explains supported recovery. To update alpha.1 through alpha.5, inspect and uninstall it using the old checkout and target before installing alpha.6; preserve any local edits first.

## 3. Check loading in a fresh conversation

Start a **new** Bob conversation and paste [verify.txt](../prompts/verify.txt). Record the exact Bob version, IDE/Shell surface, active mode, and execution host. The prompt separates filesystem integrity, native rule/skill discovery, and a small command check.

Ask Bob to report `NOT VERIFIED` when native loading cannot be observed. Opening the Markdown files manually is useful reading, but does not establish that the client discovered them. A project skill with the same name may take precedence over the global copy. See [compatibility](compatibility.md) for the documented mechanisms.

## 4. Prepare the included exercise

From the kit root, copy the fixture into a **new** disposable directory:

```sh
python3 -c "import shutil; shutil.copytree('examples/tiny-ledger', 'runs/ledger-001')"
cd runs/ledger-001
python3 -m unittest discover -s tests -v
```

`copytree` refuses to overwrite an existing directory. For another attempt, use `ledger-002` or another unused name. Keep `examples/tiny-ledger` unchanged.

**Expected baseline: nine tests, eight passes, one failure, exit code 1.** The failed transfer changes a balance when it should leave balances intact. This deliberate application failure is separate from the installer suite.

Open **`runs/ledger-001` as the Bob workspace**, start a fresh Agent conversation, and paste that directory's `PROMPT.md`. Let Bob investigate and repair it. This task needs a small change; elaborate planning or extra services are unnecessary.

## 5. Verify and review

In the exercise directory, run the same test command independently after Bob finishes:

```sh
python3 -m unittest discover -s tests -v
```

Expected after a correct repair: **nine tests pass, exit code 0**. Review the changed source and confirm the original public tests are still intact. If tests were edited, compare them with the original copy and treat the result as needing review. The companion evaluator can run the original tests independently, but is optional for this first walkthrough.

Check these outcomes separately:

| Observation | What it establishes |
| --- | --- |
| Installer suite and `doctor` succeed | The offline installer and managed files passed the checks you ran |
| Native discovery is observed in your fresh Bob client | Loading for that recorded surface/version/host |
| The original nine checks pass after a focused repair | Correctness covered by this small public suite |
| You review the diff and Bob's evidence | Whether its explanation matches the observed work |

None of these alone establishes reliable behavior on your large repository. Save failed or incomplete attempts too; they often reveal the most useful fixes.

## 6. Tell us what happened

Open [a Bob compatibility result](https://github.com/Saqlain1999/bob-workflow-kit/issues/new?template=compatibility.yml). Report the kit version, Bob version/interface, host, the three observed outcomes, and the first confusing or failing step. Short reports are welcome. Include only public fixture evidence and redact local identities or confidential paths.

For a recorded demonstration or a detailed result, copy [live-trial-template.json](live-trial-template.json). It is a manual reporting aid, not an automated attestation. Leave unobserved values as `null`; record unsuccessful attempts instead of replacing them with a later pass.

## Next: test recovery, then your own repository

The companion [Parcel Resume task](https://github.com/Saqlain1999/bob-workflow-evals/tree/main/tasks/parcel-resume) adds a specific recovery challenge. Its helper really runs a historical passing check, constructs a labelled handoff, then changes a relevant policy and an unrelated teammate note. A fresh Bob session must work from current files. The candidate check tests the current policy and preservation of protected files; a person still needs to observe the recovery behavior.

When the small exercises are understood, use [onboard.txt](../prompts/onboard.txt) on your own repository. Start with one bounded change, reuse its existing specifications and task records, and verify with that project's actual commands. Read [alternatives and coexistence](alternatives.md) before adding another workflow framework.

To remove the global installation, run `python3 tools/bob_workflow.py uninstall` from the kit root with the same target used during install. The exercise files remain yours to keep or remove.
