# Related projects and where this kit fits

Reviewed 9 October 2026 (UTC).

Bob Workflow Kit helps make work on large repositories easier to scope, resume, and verify. It combines a small set of operating instructions with project context and practical checks. The projects below offer useful complementary approaches, from learning Bob to organizing development around specifications.

This page is a review of public repositories and documentation. Listing a project does not mean we installed it, evaluated its runtime behavior, or verified compatibility with a particular Bob release.

## Start with the documented extension points

IBM's [IDE skills documentation](https://bob.ibm.com/docs/ide/features/skills) and [Bob Shell skills tutorial](https://bob.ibm.com/docs/shell/tutorials/use-skills) describe how Bob discovers and uses skills. Use the current documentation for your installed surface when checking paths, invocation, and supported behavior. An example repository may contain instructions written for an earlier release.

## Public projects worth exploring

| Project | What its public material provides | How it complements this kit |
| --- | --- | --- |
| [GitHub Spec Kit](https://github.github.io/spec-kit/reference/integrations.html) | The official integration documentation lists IBM Bob under the `bob` key. Its default integration installs `speckit-<command>/SKILL.md` files under `.bob/skills/`, invoked as `/speckit-<command>`. It also documents migration from the deprecated Bob 1.x commands layout. | Use its specification-driven development process when a change needs a formal specification and plan. This kit focuses on carrying out and resuming the work with useful context and verification evidence. |
| [IBM Bob workshops](https://github.com/IBM/intro-bob-workshop) | Public workshop source, practical exercises, and a Bob Shell skill. The power-user workshop covers rules, skills, MCP, repository analysis, and team workflows. Apache-2.0. | A learning resource for understanding the capabilities that this kit uses. |
| [IBM Bob demos](https://github.com/IBM/bob-demo) | Examples covering skills, documentation indexing, architecture work, modernization, and DevOps. Apache-2.0. | Useful task examples. Check version assumptions: the reviewed README still names earlier modes such as Code, Advanced, and Orchestrator. |
| [Bob+ Technology Building Blocks](https://github.com/ibm-self-serve-assets/building-blocks) | IBM Build Engineering reference implementations, Bob skills and modes, and runnable integration assets. The repository and its [skills ZIP](https://github.com/ibm-self-serve-assets/building-blocks/blob/main/ibm-bob/skills.zip) are public. Apache-2.0. | Add domain-specific capabilities when a project needs them; keep the general operating instructions small. |
| [bob-skill-installer](https://github.com/funhere/bob-skill-installer) | A community Python project for fetching, converting, validating, and installing third-party skills, with documented project/global scope, dry runs, and upgrade backups. Apache-2.0. | Relevant when evaluating broader skill distribution. Review its options and current implementation before use; its documented default preserves source files, including secret files unless explicitly excluded. |
| [OnboardOps](https://github.com/rohan879/OnboardOps) | A community hackathon project combining Bob onboarding instructions, skills, an MCP server, and a dashboard for repository exploration and learning. MIT. | An example of a richer onboarding experience. This kit keeps repository context useful without requiring a dashboard or service. |
| [Debug Swarm](https://github.com/Gabriel-ASM/IBM-Bob-Hackathon) | A community hackathon project with a debugging skill, focused investigators, stored run artifacts, a dashboard, and a benchmark containing planted bugs. MIT. | An example of making investigation and regression evidence visible. This kit applies similar general engineering principles across different task types. |

For Bob+, the [extension installation guide](https://ibm-self-serve-assets.github.io/building-blocks-docs/ibm-bob/extension/install/) also describes a VSIX interface. The review confirmed the public repository and skills ZIP; it did not verify a downloadable VSIX package or execute its installation.

License labels above describe the reviewed repositories. Check the relevant license and any asset-specific terms before reusing material, and preserve required notices. These links do not imply endorsement or affiliation.

## About “Propel SDLC for IBM Bob”

We have not confidently identified a public repository, installation guide, or license for the exact offering called “Propel SDLC for IBM Bob.” Its status remains unverified here.

[KANINI's Propel SDLC page](https://kanini.com/governed-ai-framework-for-enterprise-sdlc/) describes a vendor offering, but the reviewed page does not establish that it is the same Bob-specific project. A direct link to the intended offering would allow a precise comparison. This guide does not infer capabilities or open-source availability from the name.

## A deliberately small installation scope

This kit's installation scope is its own named payload. It does not need a universal third-party skill converter, marketplace, or new agent runtime to make its instructions available. Keeping that scope explicit makes it easier to inspect the files, check for collisions, preserve existing configuration, and understand what removal should affect.

When combining tools, choose which instructions own planning, implementation, and verification. Reuse existing specifications and project guidance instead of adding duplicate checklists. Add a skill because the current task benefits from it, then check its behavior on the Bob version and surface you actually use.

Instructions guide an agent; they do not by themselves enforce filesystem boundaries or prove that a patch is correct. The useful outcome is a reviewable change with appropriate verification and enough recorded context to continue the work.
