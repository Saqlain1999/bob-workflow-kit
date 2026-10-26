# Awesome Bob Workflows

A curated guide to public IBM Bob workflows, skills, learning material, and integration projects.

This is an independent community catalogue. It is not an IBM product, an official marketplace, or a certification programme. Entries are selected for relevance and inspectable evidence; inclusion is not an endorsement or a guarantee that a project will work in your environment.

**Latest source update: 17 October 2026 (Europe/Dublin).** Each entry carries its own review date; this date does not imply that every upstream changed or was re-reviewed on the same day. None has been installed or run with Bob by this catalogue. The machine-readable [catalogue](catalog/projects.json) records the evidence and review date for each entry. The [comparison review](docs/comparison-review.md) records source revisions, overlap, and important limitations.

## Find a useful starting point

| Your goal | Start with |
| --- | --- |
| Recover or manage an existing Bob session | [Native Bob first](#native-bob-first) |
| Learn the extension points and see examples | [Official references](#official-references), IBM Bob Workshops, and IBM Bob Demos |
| Structure a feature or a scoped bug fix | GitHub Spec Kit |
| Maintain evidence-qualified repository context for Spec Kit | Verified Codebase Context |
| Add a domain-specific skill or integration | Bob+ Technology Building Blocks |
| Investigate skill installation and conversion | bob-skill-installer |
| Coordinate a shared task board and dispatch agent work | Bob Control |
| Expose Bob through a service with sessions and cancellation | Headless Bob |
| Explore repository onboarding as a guided experience | OnboardOps |
| Study investigation, regression evidence, and debugging handoffs | Debug Swarm |
| Install a small operating workflow, evaluate it, or explore a runner | [Companion projects](#companion-projects) |

Follow the upstream instructions for the version you intend to use. This catalogue does not install third-party content or run commands from the linked projects.

## Native Bob first

Start with the features already available in your Bob client: [Shell session history, resume, and compact commands](https://bob.ibm.com/docs/shell/features/slash-commands), [context-window management](https://bob.ibm.com/docs/ide/core-concepts/context-window-management), and [IDE rollback](https://bob.ibm.com/docs/ide/features/rollback). These are IBM product features; they are not additional open-source packages in this catalogue.

Restoring a conversation or a checkpoint does not establish that an old test result still applies after source or requirements change. Use an additional workflow when you need explicit task ownership, source-backed handoff, shared orchestration, or independently recorded acceptance evidence. Check [large-project guidance](https://bob.ibm.com/docs/ide/core-concepts/large-projects) before adding another layer.

## Read the status correctly

Three different observations matter:

- **Public source:** an inspectable repository is available. This does not establish that a release package exists or that the project runs.
- **Installation documented:** upstream provides setup or usage instructions. Those instructions have not necessarily been executed by a catalogue contributor.
- **Runtime evidence:** a dated report names the source revision, exact Bob version, interface, environment, task, and result. A linked report applies to that combination and task; it is not universal support.

All entries retain **documentation review only**. Some sources include maintainers' execution reports; this catalogue has not reproduced them or promoted them into its structured runtime-evidence records. “Not assessed” means we did not establish a fact during this review; it does not mean the capability is absent. Repository licenses describe upstream material and do not turn every dependency or service into a free or supported product.

See the [curation policy](docs/curation.md) and [metadata format](docs/metadata.md) for the full definitions.

## Specifications and planning

### GitHub Spec Kit

[Source](https://github.com/github/spec-kit) · [Official IBM Bob integration reference](https://github.github.io/spec-kit/reference/integrations.html) · MIT

Spec Kit supplies structured development processes and reusable templates. Its integration guide explicitly lists IBM Bob under the `bob` key. The default writes `speckit-<command>/SKILL.md` files into `.bob/skills/` and uses `/speckit-<command>` invocation. The guide distinguishes the deprecated Bob 1.x command layout and migration, and documents hash-tracked installation and preservation of modified files on uninstall.

It also includes a separate [bug workflow](https://github.com/github/spec-kit/blob/9dca9bf42a031765ee5e5f2371137f2f26967e11/extensions/bug/README.md): assess, fix, and test, with per-bug reports and explicit partial/not-run verification. Useful for specifications or scoped fixes. The reviewed release is [v1.2.1, published 16 October 2026](https://github.com/github/spec-kit/releases/tag/v1.2.1). It adds opt-in, per-stream-limited workflow output capture with timeout/interruption fields and process-tree cleanup, plus catalogue trust and source-precedence guidance. Captured text is stored unredacted and is explicitly treated as untrusted; installation and runtime dispatch were not executed here.

### Verified Codebase Context

[Source](https://github.com/philo-x/spec-kit-preset-codebase-memory-context) · [Reviewed v1.1.0 README](https://github.com/philo-x/spec-kit-preset-codebase-memory-context/blob/52b67e61b0ecdac0aec7c17acb0852e0355f31c1/README.md) · MIT

A Spec Kit community preset for established repositories. It generates `.specify/memory/codebase.md` from repository evidence, preserves a manual overrides section, and makes plan/tasks/analyze/implement consult that context. Code graphs are optional; direct reads and search are the baseline. The generator records build and test commands without executing them.

The four consumer commands replace core files and target **Spec Kit 1.1.2**. The now-current Spec Kit 1.2.1 release is outside that stated baseline, so treat the combination as requiring a compatibility review rather than assuming it is safe. The documented test matrix names Codex, Claude, Copilot, and Gemini, not Bob. Its Bob connection is through Spec Kit's integration, and this catalogue has not established Bob compatibility. If using it, refer to its context from other workflows rather than maintain a second authoritative profile.

## Learning and examples

### IBM Bob Workshops

[Source](https://github.com/IBM/intro-bob-workshop) · [Workshop site](https://ibm.github.io/intro-bob-workshop/) · Apache-2.0

Workshop source, exercises, and an [agent-with-bob-shell skill](https://github.com/IBM/intro-bob-workshop/blob/352cdb45d8ad2a53b27aaa31a9248edf3bc8f2fe/.bob/skills/agent-with-bob-shell/SKILL.md) with Python Plan → Act → Evaluate loop examples. The power-user material covers rules, skills, MCP, repository analysis, and team workflows. Labs have different audiences; the power-user workshop specifically targets IBM employees, while other material addresses external audiences.

Use it to learn the underlying mechanisms and adapt an appropriate exercise. Check current product documentation before copying version-dependent flags or mode descriptions; a workspace argument is not an OS sandbox. Setup and usage are documented; no catalogue runtime test has been performed.

### IBM Bob Demos

[Source](https://github.com/IBM/bob-demo) · Apache-2.0

Examples cover skills, documentation indexing, architecture work, modernization, and DevOps. A [Beads example](https://github.com/IBM/bob-demo/blob/bc8a8f874cd34abd6cff97bcbf863070710e7566/beads/README.md) supplies a project rule and MCP setup for persistent issue tracking. Check each example's version assumptions: the reviewed README still lists earlier modes such as Code, Advanced, and Orchestrator. Its public-repository disclosure distinguishes this source project from a supported IBM product.

Useful as task examples, with installation instructions to review before trying them.

## Skills and domain integrations

### Bob+ Technology Building Blocks

[Source](https://github.com/ibm-self-serve-assets/building-blocks) · [Extension documentation](https://ibm-self-serve-assets.github.io/building-blocks-docs/ibm-bob/extension/install/) · Apache-2.0 at repository root; MIT for `ibm-bob/skills/`

IBM Build Engineering reference implementations include domain skills and runnable integration assets. A public skills ZIP and [Bob+ 1.1.0 VSIX](https://github.com/ibm-self-serve-assets/building-blocks/tree/5c610971dc72f9e9035821b3cb2c3edea868f8b4/ibm-bob/extension) are present. The [1.1.0 changelog](https://github.com/ibm-self-serve-assets/building-blocks/blob/5c610971dc72f9e9035821b3cb2c3edea868f8b4/ibm-bob/extension/CHANGELOG.md) describes Building Blocks and Specs, removal of the Modes panel, and automatic configuration of required MCP servers.

The main branch added a [Granite TTM forecasting skill](https://github.com/ibm-self-serve-assets/building-blocks/blob/36e24f5bbab28fac99c2a0a20deeaf2f423dd35b/ibm-bob/skills/ttm-forecasting/SKILL.md) on 14 October 2026. Its source routes among watsonx.ai, a local Hugging Face pipeline, and a mock path, and separates inference, dashboard, and fleet guidance. On 15 October, the upstream [generated skills catalogue](https://github.com/ibm-self-serve-assets/building-blocks/blob/f422bb7b98614fdc1fff08a8fb800c86eee5c66f/explore-BBs/bb-catalog/skills/ttm-forecasting.md) marked it active and exposed a generated ZIP download. This is source and distribution evidence only: the catalogue did not download or extract the archive, install the skill, download model weights, call watsonx.ai, or reproduce its production and performance claims. Review the archive and the selected path's credentials, network, storage, and dependency requirements before use; the mock path is explicitly non-production.

The older website guide still describes modes, so use the versioned source when checking behavior. The binary and skills ZIP were not downloaded or run here. Choose domain assets individually and review their configuration effects. Preserve [asset-level license notices](https://github.com/ibm-self-serve-assets/building-blocks/blob/36e24f5bbab28fac99c2a0a20deeaf2f423dd35b/ibm-bob/skills/LICENSE.txt).

## Orchestration and services

### Bob Control

[Source](https://github.com/PounceAI/bob-control) · [Reviewed README](https://github.com/PounceAI/bob-control/blob/315cbf54076842f06462ea8846aae837594c67cd/README.md) · Apache-2.0

An MCP server, CLI, and worker around a SQLite task board. Its source includes task dependencies, notes/evidence, attempts, checkpoints, and recovery. The documented adapters cover headless Bob Shell 2.x through `bob acp`, a Bob IDE companion, and a shared board with Claude Code. All participating processes must point to the same board; the README explains that setup.

This is an executable orchestration project to evaluate before writing a queue worker. It documents unattended approval and optional acceptance judging, so examine those policies for your workflow. A judge label alone is not proof that checks ran or passed; see the [review caveat](docs/comparison-review.md#bob-control-acceptance-policy). No worker or adapter was executed by this catalogue.

### Headless Bob

[Source](https://github.com/ibm-self-serve-assets/building-blocks/tree/main/ai/engineering/headless-bob/assets/headlessbob) · [Reviewed README](https://github.com/ibm-self-serve-assets/building-blocks/blob/5c610971dc72f9e9035821b3cb2c3edea868f8b4/ai/engineering/headless-bob/assets/headlessbob/README.md) · Apache-2.0 repository source; inspect dependency and specification notices

The `headlessbob` application in Building Blocks exposes Bob through REST, Agent Communication Protocol, and MCP. The source includes sessions, SQLite run storage, cancellation, queue and output limits, a browser UI, and Python client examples. The reviewed package identifies itself as **0.4.0** and documents Node.js 22.22+ with Bob Shell 2.0.4.

Its [maintainer verification record](https://github.com/ibm-self-serve-assets/building-blocks/blob/5c610971dc72f9e9035821b3cb2c3edea868f8b4/ai/engineering/headless-bob/assets/headlessbob/VERIFICATION.md) distinguishes fixture checks, live Bob checks, and deployment stages. Those results were not reproduced here. The documented trust model is for trusted operators and explicitly does not provide an OS sandbox between untrusted users. Useful when a service interface is needed; it is separate from a rules-and-skills preset.

## Distribution and installation tools

### bob-skill-installer

[Source](https://github.com/funhere/bob-skill-installer) · Apache-2.0

A community Python implementation for fetching, converting, validating, and installing skills. The reviewed package is **0.1.0**, requires Python 3.12+, and provides project/global scope and dry runs.

Review the options before use: its default preserves source files, including secret files unless excluded. The README's retained-upgrade-backup claim conflicts with the [reviewed implementation and test](docs/comparison-review.md#skill-installer-backup-behavior), which remove the backup after success. A converter's output still needs inspection for the destination client's tools and behavior; a static pattern scan is not a security guarantee. Installation is documented; this catalogue has not run the tool or scanner.

## Onboarding and debugging

### OnboardOps

[Source](https://github.com/rohan879/OnboardOps) · MIT

A community hackathon project combining Bob onboarding instructions, skills, an MCP server, and a dashboard for repository exploration and learning. It is useful as an example of a richer onboarding experience.

The public source and documented design were reviewed. Installation was not assessed. Its custom-mode representation needs checking against the actual Bob client before use.

### Debug Swarm

[Source](https://github.com/Gabriel-ASM/IBM-Bob-Hackathon) · MIT

A community hackathon project with a seven-phase debugging skill, focused investigators, stored run artifacts, a dashboard, and a benchmark containing planted bugs. It documents setup and replayable reference runs.

Useful for studying how investigation and regression evidence can be made visible. Upstream test counts and benchmark outcomes have not been independently reproduced here.

## Official references

These are product references, not open-source package entries. Consult the page for your actual client and version:

| Topic | Primary reference |
| --- | --- |
| IDE custom rules | [IBM Bob IDE rules](https://bob.ibm.com/docs/ide/configuration/rules) |
| Shell custom rules | [IBM Bob Shell rules](https://bob.ibm.com/docs/shell/configuration/bobshell-custom-rules) |
| IDE skills | [IBM Bob IDE skills](https://bob.ibm.com/docs/ide/features/skills) |
| Shell skills and invocation | [Create and use skills in Bob Shell](https://bob.ibm.com/docs/shell/tutorials/use-skills) |
| Working with large projects | [Large projects](https://bob.ibm.com/docs/ide/core-concepts/large-projects) |
| Context management | [Context-window management](https://bob.ibm.com/docs/ide/core-concepts/context-window-management) |
| Automated Shell use | [Non-interactive Bob Shell](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive) |
| Native session continuation | [Shell slash commands](https://bob.ibm.com/docs/shell/features/slash-commands) |
| Native file restoration | [IDE rollback](https://bob.ibm.com/docs/ide/features/rollback) |
| Release-specific changes | [IDE changelog](https://bob.ibm.com/docs/ide/changelog) and [Shell changelog](https://bob.ibm.com/docs/shell/changelog) |

Descriptions in this catalogue are original summaries. Primary links and the claims they support are also recorded in [catalog/projects.json](catalog/projects.json).

## Unresolved suggestions

**Propel SDLC for IBM Bob:** the exact public project repository has not been established. It has no catalogue entry until a primary source identifies the Bob-specific project and its licensing. We have not substituted a similarly named product. The unresolved link does not establish that a capability is absent or that another project is unique.

## Companion projects

These public companion repositories cover different parts of the workflow. Check each repository's own implementation status and available validation evidence.

| Repository | Intended responsibility |
| --- | --- |
| [bob-workflow-kit](https://github.com/Saqlain1999/bob-workflow-kit) | A practical guide, operating instructions, a focused skill, installation tooling, and recovery templates |
| [bob-workflow-evals](https://github.com/Saqlain1999/bob-workflow-evals) | Reproducible tasks and evidence for assessing workflow behavior |
| [bob-workflow-runner](https://github.com/Saqlain1999/bob-workflow-runner) | Controller design preview; no executable runner |
| This catalogue | Source-backed discovery and clearly scoped compatibility notes |

Keep each project's role separate. A catalogue entry is not a performance result; an evaluation is not an installation guide; a runner only controls work launched through that runner.

## Contribute a useful entry

Start with [CONTRIBUTING.md](CONTRIBUTING.md), copy [the entry template](templates/project-entry.json), and provide a direct primary link showing the Bob connection. An author's own example or a public implementation is useful evidence. Popularity and marketing language alone are not.

Corrections to stale paths, ambiguous licensing, unavailable artifacts, or version assumptions are valuable contributions. Disclose an affiliation with a project you submit. We do not rank projects by stars, claim exhaustive coverage, or copy upstream performance claims as verified results.

## Validate the catalogue locally

Python 3.10 or later is the validator's compatibility target. It uses only the standard library.

```sh
python3 tools/validate_catalog.py
```

The command checks metadata structure, source URLs, IDs, review/evidence consistency, README coverage, and repository-local Markdown links. It performs no network requests and does not install or evaluate any listed project. It exits nonzero for invalid catalogue content. The included CI workflow runs this same check; a workflow definition is not evidence that hosted CI has passed.

See [VALIDATION.md](VALIDATION.md) for the actual local preparation record.

## License and community

Original catalogue text, metadata, and tooling are available under the [MIT license](LICENSE). Linked projects retain their own licenses, trademarks, and support arrangements.

Follow the [community conduct guide](CODE_OF_CONDUCT.md). For catalogue corrections, use an issue or pull request; for a problem in an upstream tool, consult that project's support instructions. See [SECURITY.md](SECURITY.md) before sharing sensitive findings.
