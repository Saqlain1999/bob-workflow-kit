# Troubleshooting

Start with the exact command output and the active execution host. Preserve unrelated work while diagnosing one concrete condition at a time.

| Observation | What to check | Useful next action |
| --- | --- | --- |
| `preview` reports a collision | A desired file already exists without this kit's ownership record | Inspect that file and its origin. Keep the existing workflow, or move/merge it deliberately before retrying; do not force overwrite |
| `local_changes` or `modified_files` | A managed file is missing or differs from its recorded content | Preserve intentional edits; compare with the package and decide how to retain them |
| `upgrade_requires_uninstall` | Installed package/version differs from this package | Use the unchanged installation's uninstall flow, then preview/install the new package |
| `recovery_needed` | An installation journal remains | Stop any active installer; inspect doctor output and use the documented uninstall recovery path |
| A symlink/redirection error | The target or a managed component redirects filesystem operations | Inspect the resolved destination and use an appropriate direct target; do not relax the checks blindly |
| A hard-link/publication error | The selected filesystem may not support the required operation | Inspect rollback status; use a supported local target or a reviewed manual installation |
| Bob asks for approval or blocks a write to `~/.bob` | Current Bob Shell protects Bob-home writes even when auto-approve is enabled; managed workstation policy may deny them | Verify the exact included-installer command and previewed target, then approve once only if policy permits. Otherwise stop after read-only checks and leave settings unchanged. Do not retry the denied write manually or through another shell. A rehearsal against an explicit, non-active temporary target is separate and must itself be permitted by policy |
| `doctor` is healthy but Bob cannot find the skill | Client loading is distinct from file integrity | Restart/start a fresh conversation, inspect Skills settings or the Shell picker, and confirm the same host/home |
| Bob loads a different `work-large-codebase` | A project skill can override a global skill | Inspect the resolved skill path and reconcile duplicate installations intentionally |
| Bob still reads too broadly | The request lacks a useful scope, or the workflow was not activated | Give the affected behaviour/interface and ask for entry points, callers, and tests before implementation |
| Bob forgets earlier decisions | The task record may be absent, stale, or too large | Use a concise checkpoint and name its exact path in a fresh recovery request |
| Bob repeats the same failing command | The cause may be environmental, denied, or misunderstood | Classify the failure and change the next action based on new evidence |
| Bob says tests passed but evidence is absent | The command may not have completed or may not have run | Request the actual command, working directory, exit status, relevant output and scope |
| Live-trial validation rejects the record | The result lacks run/host identity, explicit trust, interactive Bob observation, loading evidence, or task evidence for its claim level | Keep the actual status as `blocked` or `incomplete`; add only evidence that was observed. Do not relabel `bob run`, file existence, or helper output as an interactive live-Bob task |
| Trial preparation cannot resolve the kit commit | The checkout has no Git history, or Git is unavailable | For a reviewed source archive, rerun preparation with the exact release/PR commit and recorded archive SHA-256. Do not substitute the newest main commit or an unverified digest |
| Trial preparation says the output already exists | The command refuses to replace prior or partial evidence | Choose a new run-specific path. Preserve and inspect the existing file; delete it only when you have deliberately decided it contains no evidence worth retaining |
| Trial recording says the input is not `not_run` | The recorder accepts only the immutable prepared starting record | Keep every prior result. Start from the original prepared record and choose a new output path for each blocked or incomplete attempt |
| A recovery trial passes tests but validation rejects `completed` | Mechanical correctness does not show that the participant used the handoff, reconciled current state, detected stale evidence, reran current checks, updated the checkpoint, or preserved unrelated work | Complete the human acceptance review from visible evidence, or keep recovery status `partial` and the overall trial `incomplete`; never infer process observations from a green candidate report |

Current IBM references: [IDE skills](https://bob.ibm.com/docs/ide/features/skills), [Shell skills tutorial](https://bob.ibm.com/docs/shell/tutorials/use-skills), [rules precedence](https://bob.ibm.com/docs/ide/configuration/rules), and the [Shell changelog entry for protected Bob-home writes](https://bob.ibm.com/docs/shell/changelog#201).

## Record a blocked or incomplete trial

Keep the prepared `not_run` record as the immutable starting point. After an
actual interactive IDE or Shell attempt, create a new result rather than editing
or replacing either file. This example records a healthy offline installation
whose skill did not appear in an interactive Shell picker:

```sh
python3 tools/record_live_trial.py \
  --input /path/to/prepared.json \
  --output /path/to/blocked-001.json \
  --status blocked \
  --claim-level installation_only \
  --run-id parcel-blocked-001 \
  --observed-at-utc 2026-11-13T08:00:00Z \
  --bob-interface shell_interactive \
  --bob-version RECORDED_VERSION \
  --bob-mode agent \
  --os RECORDED_OS \
  --python-version RECORDED_PYTHON \
  --execution-host-type local-disposable \
  --workspace-trust-decision trust_folder \
  --workspace-trust-evidence "Fixture trust dialog accepted" \
  --native-loading-evidence "Skill absent from the interactive picker" \
  --installation-status healthy \
  --doctor-evidence "doctor reported healthy" \
  --fresh-conversation-confirmed \
  --live-bob-observed \
  --first-confusing-step "Installed skill did not appear" \
  --limitations-and-redactions "Public fixture; local paths removed"
python3 tools/validate_live_trial.py /path/to/blocked-001.json
```

Replace every `RECORDED_...` value with the value actually observed. Use
`loading_observed` only with `--rule-loaded` or `--skill-loaded`; do not use an
installation-only claim after recording native loading. The recorder accepts
only `blocked` or `incomplete`, requires explicit fresh-conversation and live-Bob
confirmation, preserves the kit/task identity from the prepared record, and
refuses an existing output path. It does not run Bob, attest observations,
complete the task, or turn helper output into live-client evidence.

## If your setup came from the earlier prompt-only approach

This package installs a known rule and the named `work-large-codebase` and `write-clear-technical-content` skills. A manually generated skill with either name may already occupy that directory. That is a real collision, not an installer failure to bypass.

Compare the existing content and this package. Preserve customisations outside automatically loaded rule/skill directories while you decide how to merge them. Remove an older duplicate only after identifying what it contributes. The kit does not automatically take ownership of manually created files.

## Sharing a useful report

Include the kit version, command or prompt, actual output, OS/Python/Bob versions, and a minimal disposable reproduction. Redact sensitive paths and omit credentials, private code, and confidential logs. A screenshot of “done” alone does not establish loading or verification.
