# Compatibility and evidence

Documentation review date: **9 October 2026 (UTC)**. Package: **0.1.0-alpha.1**.

## Mechanisms used by this package

| Mechanism | Documentation evidence | Package status |
| --- | --- | --- |
| Global rules under `~/.bob/rules/` | [IDE](https://bob.ibm.com/docs/ide/configuration/rules) and [Shell](https://bob.ibm.com/docs/shell/configuration/bobshell-custom-rules) | Implemented by the installer; live loading must be tested per client |
| Global skill under `~/.bob/skills/work-large-codebase/` | [IDE skills](https://bob.ibm.com/docs/ide/features/skills) and [Shell skills](https://bob.ibm.com/docs/shell/features/skills) | Implemented; supporting references/templates are included |
| Simple `name` and `description` front matter | Same skill references | Present; description fallback differences between clients are avoided |
| Shell skill selection | [Shell skills tutorial](https://bob.ibm.com/docs/shell/tutorials/use-skills) describes `$skill-name`, the `$` picker, and `/skills` | Documented; not an offline installer assertion |
| Workspace overrides | Rule/skill docs above describe workspace precedence | Users must inspect same-name project copies when diagnosing loading |
| Global Shell `~/.bob/AGENTS.md` | [Shell configuration](https://bob.ibm.com/docs/shell/configuration/configuring) | Preserved; the kit does not duplicate its rule there |
| Native plugin directories | [October 1 release post](https://bob.ibm.com/blog/september-2026-release/) | Documented by IBM, but not this package's distribution format |
| Lifecycle hooks / MCP / custom modes | Separate Bob configuration mechanisms | Not installed or changed by this release |

Current Shell documentation describes the same rules system as the IDE. That lets this kit use one global payload instead of maintaining duplicate full instructions in separate entrypoints.

## Runtime test matrix

| Environment | Installer tests | Live Bob loading | Bob task behaviour |
| --- | --- | --- | --- |
| Linux, Python 3.12.14, local disposable configuration | See [VALIDATION.md](../VALIDATION.md) | Not tested | Not tested in Bob |
| macOS | CI definition included; not executed in this preparation environment | Not tested | Not tested |
| Windows | CI definition included; not executed in this preparation environment | Not tested | Not tested |
| Remote SSH / containers / managed workstations | Target can be selected explicitly; host-specific execution not qualified | Not tested | Not tested |

Python 3.10 is the source compatibility target. Local execution evidence currently comes from Python 3.12.14. GitHub-hosted jobs are definitions until they actually run; a workflow file is not a passing CI result.

No live Bob installation was available for this preparation. The small independent-agent exercise described in the validation record checks the written workflow on a fixture, not Bob's loader or runtime.

## Check the actual host

The default target comes from the process running the installer. If Bob runs on a remote host or inside a container, a local installation might not reach it. Preview the explicit `--bob-home` target and record the active host before writing.

A directory managed through symlinks may be rejected by this conservative installer. That is a supported limitation, not a reason to force through an unexpected filesystem target. Inspect and choose an appropriate direct target or use a reviewed manual installation.

Older clients may differ. The [Shell changelog](https://bob.ibm.com/docs/shell/changelog) and [IDE changelog](https://bob.ibm.com/docs/ide/changelog) should be consulted before claiming compatibility with a specific release. Do not infer compatibility merely from the product name.

## Report a tested combination

Record the kit version/commit, exact Bob version, interface, OS, execution host, target path (redacted where needed), installation integrity output, observed rule/skill loading, fixture results, and remaining limitations. Submit a compatibility report with no credentials or private project content.

Promote a combination from “documented” to “tested” only with actual execution evidence. Promote “tested” to a broader support claim only after the project's maintainers accept an ongoing test/maintenance commitment.
