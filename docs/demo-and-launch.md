# Demonstrate a result, then invite a trial

Status: **recording instructions and launch materials; no live Bob recording has been produced for this release**. This file is a maintainer plan, not evidence that outreach or testing happened.

The public starting point is [Try the alpha](try-alpha.md). Link people there first. Keep the kit as the user-facing entry point, the evaluator as supporting evidence, the catalogue as reference material, and the runner as a design preview.

## Record one real demonstration

Use the public Parcel Resume task from [bob-workflow-evals](https://github.com/Saqlain1999/bob-workflow-evals/tree/main/tasks/parcel-resume). Run on a machine with Bob installed; record the exact kit/evaluator revisions, Bob surface/version and relevant configuration. Follow that task's README and acceptance checklist.

The helper constructs an interruption scenario. Its historical check is an actual local test run; its checkpoint is **not** a transcript of a prior Bob session. State that at the start of a recording. To claim a real interrupted-agent trial later, separately capture the original Bob session, interruption, intervening edits and resumed session.

Suggested edited video length is 2–3 minutes. Preserve the complete run evidence; cuts and playback speed changes must not be presented as elapsed task time.

| Scene | Show | What the viewer learns |
| --- | --- | --- |
| Setup | Exact versions, fixture task and unchanged original | What was tested and how to reproduce it |
| Starting state | Historical passing result, current policy and teammate note, failing interrupted baseline | An earlier green result can be stale |
| Fresh session | Actual Bob conversation inspecting the handoff/current files | Whether the recorded behavior matches the intended workflow |
| Verification | Independent candidate report and focused diff | Whether current checks passed and protected work survived |
| Result | Accepted, failed or incomplete status; limitations; first-use link | A concrete outcome and the next step |

Use the task's ordinary participant prompt. Extra hints or human repairs are interventions and belong in the report. Keep API keys, private repository content, personal file paths and unrelated desktop windows out of the recording.

Publish a recording only after reviewing the observed result. Accompany it with the [live trial record](live-trial-template.json), evaluator reports, a diff, and links to the exact source revisions. A failure is still a useful demonstration if accurately labelled.

## Launch sequence

1. Publish an explicitly labelled alpha with exact-source CI, a source archive and checksum, the first-use guide, and known limitations.
2. Complete at least one real Bob trial and review the evidence. Start with one surface; do not infer IDE/Shell parity.
3. Invite a small initial group to run the walkthrough and report where it fails or becomes confusing. A useful initial target is five trial participants, three who try a second task, and two actionable reports. These are planning targets, not measured adoption or promises.
4. Fix the most common setup or workflow failure before expanding promotion. Publish substantive changes and failures alongside successful examples.
5. Offer a concrete example to existing Bob learning communities, with credit to alternatives. Avoid presenting a new general framework when a small useful exercise is what is available.

## Where a contribution could fit

| Route | Appropriate contribution | Requirement |
| --- | --- | --- |
| [IBM Bob community](https://community.ibm.com/community/user/groups/community-home?CommunityKey=300ac388-08f0-427e-a600-0199bfc9dd2a) | A helpful, original tutorial with a reproducible example and limitations | Follow [blog guidance](https://community.ibm.com/community/user/participate/blogging-in-the-community) and [netiquette](https://community.ibm.com/community/user/community/community-netiquette); current posting access may need approval |
| [IBM/bob-demo](https://github.com/IBM/bob-demo) | A small resume/freshness demo | Follow [CONTRIBUTING.md](https://github.com/IBM/bob-demo/blob/main/CONTRIBUTING.md): propose the demo in Discussions before a contribution PR |
| Existing context/workflow projects | A Bob compatibility result or focused documentation/test fix | Reproduce their supported configuration and respect their contribution process |
| The maintainer's own professional account | A short account of the problem and observed result | Link one first-use page, state alpha status and actual test scope |

These routes were reviewed on 10 October 2026. This repository does not claim an accepted submission, an IBM endorsement, or a verified public third-party Marketplace listing process. Repository publication does not authorize someone operating an assistant to send outside messages on the maintainer's behalf.

## Draft announcement for review

> I’m working on Bob Workflow Kit, a small community alpha for developers who lose task context while working in larger repositories. It combines a concise global rule, focused on-demand skills, an inspectable installer, and exercises that make verification evidence visible.
>
> Existing tools already solve much of this problem, so the guide includes alternatives and coexistence advice. Our new recovery exercise starts with an old passing check, a changed policy and a teammate’s unrelated edit. It gives us a reproducible way to inspect how a fresh Bob session handles the current state.
>
> Offline checks are published. Live Bob compatibility and large-repository effectiveness still need recorded trials. If you use Bob, try the first-use walkthrough and tell us the first step that fails or feels unclear: https://github.com/Saqlain1999/bob-workflow-kit/blob/main/docs/try-alpha.md

Update the evidence sentence only after a live trial actually exists. This draft is not a sent message or published community post.

## Measure usefulness

Track completed first trials, exact client combinations, first confusing steps, accepted recovery attempts, repeat use and resolved reports. Stars are a discovery signal, not evidence that people successfully used the kit. Use opt-in issue reports; the kit does not add telemetry.

When reviewing GitHub's repository traffic, preserve periodic summaries if needed: its [traffic view](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository) covers a limited recent window. Do not infer installations from clone or download counts.
