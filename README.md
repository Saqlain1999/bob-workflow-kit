# Bob Workflow Kit

**Practical workflows for investigating, changing, verifying, and resuming code with IBM Bob.**

Version: **0.1.0-alpha.1**. Community alpha. This toolkit is independent of IBM and is not an IBM product or Marketplace listing.

Bob Workflow Kit combines a public guide, a concise global rule, an on-demand skill, repository/task templates, and an offline installer. It is designed for developers who lose the thread in large repositories, get overwhelmed by command output, or cannot tell what an agent actually verified.

The installer manages a small known payload. The workflow uses Bob's existing tools. The kit does not need a model API key, MCP server, package manager, or background service to install. Bob itself remains a separate prerequisite.

## Start here

1. Read the [practical guide](docs/guide.md) if rules, skills, and task memory are new to you.
2. Preview and install the package below.
3. Verify loading in a **fresh Bob conversation** using [verify.txt](prompts/verify.txt).
4. Open your project and use [onboard.txt](prompts/onboard.txt).
5. Use [work.txt](prompts/work.txt) for substantial changes and [resume.txt](prompts/resume.txt) after an interruption.

Prefer Bob to operate the installer? Open this extracted repository in Bob Agent mode and paste [install-with-bob.txt](prompts/install-with-bob.txt). It tells Bob to inspect and run this implementation, rather than generate a different installer.

## Quick installation

Prerequisites: Python **3.10 or later**, a local copy of this repository, and a Bob version that supports the documented global rules/skills layout. The offline installer does not check out code or install Python/Bob for you.

From the repository root on Linux/macOS:

```sh
python3 tools/bob_workflow.py preview
python3 tools/bob_workflow.py install
python3 tools/bob_workflow.py doctor
```

On Windows with the Python launcher:

```powershell
py -3 tools/bob_workflow.py preview
py -3 tools/bob_workflow.py install
py -3 tools/bob_workflow.py doctor
```

Inspect the resolved target shown by `preview`. The default is the current user's `.bob` directory. `--bob-home` means the **Bob configuration directory itself**, not the parent user home:

```sh
python3 tools/bob_workflow.py preview --bob-home /absolute/path/to/.bob
```

Use an explicit temporary target to try installation without changing your active Bob configuration. Do not change system home environment variables to redirect the installer. Remote SSH hosts and containers may use a different Bob home.

The installer writes the packaged rule and skill under:

- `rules/bob-workflow-kit.md`
- `skills/work-large-codebase/SKILL.md` and its supporting references/templates
- `workflow-kit/` for this kit's own installation records and recovery data

These are relative to the selected Bob home. `workflow-kit/` is our convention, not an IBM configuration feature. The kit does not edit your existing settings, global `AGENTS.md`, modes, hooks, permissions, model selection, authentication, or MCP configuration.

The same global rules/skills layout is documented for current [Bob IDE rules](https://bob.ibm.com/docs/ide/configuration/rules), [Bob Shell rules](https://bob.ibm.com/docs/shell/configuration/bobshell-custom-rules), [IDE skills](https://bob.ibm.com/docs/ide/features/skills), and [Shell skills](https://bob.ibm.com/docs/shell/features/skills). Actual loading remains a separate acceptance check for each version, interface, and execution host.

## What the first release includes

| Component | Purpose |
| --- | --- |
| Global operating rule | Keep routine work light; use focused investigation, bounded output, and real verification for substantial tasks |
| `work-large-codebase` skill | Onboard a repository, make a substantial change, or resume from a checkpoint |
| Repository profile | Record actual components, commands, dependencies, constraints, and evidence sources |
| Task checkpoint | Preserve decisions, changed files, check results, failed approaches, and the next action |
| Offline installer | Preview changes, install known assets, inspect ownership/integrity, and uninstall carefully |
| Tiny Ledger exercise | Demonstrate a real failing check, a focused repair, and a useful handoff in a disposable project |
| Compatibility and evaluation records | Separate documented mechanisms, local software tests, and live Bob testing |

The kit encourages a working method. It cannot force every agent action or guarantee correct software. A separate controller would be needed to enforce its own stage transitions; that is a [planned extension](docs/roadmap.md), not part of this release.

## Verify before relying on it

`doctor` inspects local installation facts. A successful result does **not** prove Bob loaded the files or followed the workflow. Start a fresh IDE/Shell conversation, use the verification prompt, and record the interface and version separately. If your project supplies a skill with the same name, it can override the global copy.

Try the [Tiny Ledger exercise](examples/README.md) in a disposable copy. Its test suite deliberately starts with one failure; the installer test suite must pass normally. A tiny fixture is a smoke test, not evidence that every large repository will work.

See [compatibility](docs/compatibility.md), [evaluation](docs/evaluation.md), and [troubleshooting](docs/troubleshooting.md) for exact limits and reporting guidance.

## Remove or update the installation

```sh
python3 tools/bob_workflow.py uninstall
```

Use the same `--bob-home` override if you installed somewhere else. Uninstall uses this kit's ownership records; it preserves conflicting local edits rather than deleting them. Reinstalling unchanged content should be a no-op. Read the command output and [installer design](docs/installer.md) before resolving an interrupted transaction or updating modified files. There is no blind overwrite option.

## Contribute

Useful contributions include reproducible installation failures, IDE/Shell compatibility reports, clearer onboarding examples, and realistic recovery exercises. Follow [CONTRIBUTING.md](CONTRIBUTING.md). Do not submit credentials, private source code, or raw confidential logs.

Run the offline suite from this repository root:

```sh
python3 -m unittest discover -s tests -v
```

The [existing ecosystem](docs/ecosystem.md) already has workshops, skill collections, installers, and specification workflows worth using. This project focuses on a small configuration that people can understand, verify, and maintain alongside those tools.

## Project status and licence

This alpha is available at [Saqlain1999/bob-workflow-kit](https://github.com/Saqlain1999/bob-workflow-kit). [VALIDATION.md](VALIDATION.md) records what was actually executed; [the release guide](docs/releasing.md) describes publication and release checks. No performance improvement or live Bob compatibility is claimed without a corresponding result.

The companion repositories are [bob-workflow-evals](https://github.com/Saqlain1999/bob-workflow-evals), an evaluation starter; [bob-workflow-runner](https://github.com/Saqlain1999/bob-workflow-runner), a controller design preview; and [awesome-bob-workflows](https://github.com/Saqlain1999/awesome-bob-workflows), a curated resource catalogue. Their scopes differ: the runner preview does not contain an executable controller. See the [roadmap](docs/roadmap.md) for how the projects fit together.

Original kit content is provided under the [MIT licence](LICENSE). Linked third-party projects keep their own licences and support policies.
