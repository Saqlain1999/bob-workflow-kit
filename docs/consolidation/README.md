# One-product consolidation preview

Status: local preparation, not publication or a release. The canonical product is **Bob Workflow Kit**: one checkout, one installation, one first-use guide and one intended issue tracker. This branch does not change Bob's proprietary client. Local kit ports extend the packaged payload to alpha.7 with six fixed-scope skills; they do not update any active Bob installation.

## Layout

- Root, `payload/`, `tools/`, `tests/`, `examples/`: the existing kit and offline installer.
- `evals/`: included evaluation tasks, fixtures, helper and their original validation records. See [exercise instructions](../exercises.md) for the working-directory boundary.
- `docs/resources/catalogue/`: preserved resource catalogue and provenance; no additional installation.
- `docs/design/runner/`: deferred controller design only; no executable runner.

## Source and history preservation

The [source map](source-map.json) records exact source commits, prefixes, original blob IDs and SHA-256 checksums for every imported tracked file. The source commits are parents/ancestors of the consolidation branch, imported with Git subtree **without squashing**. Existing source-repository working copies, branches, URLs, licences and validation records remain intact. Original repository URLs:

- https://github.com/Saqlain1999/bob-workflow-kit
- https://github.com/Saqlain1999/bob-workflow-evals
- https://github.com/Saqlain1999/awesome-bob-workflows
- https://github.com/Saqlain1999/bob-workflow-runner

The initial import used only each repository's `main`; the accepted October preview preserved ten reviewed source heads. The current refresh records **15 exact source PR heads** in the [PR map](open-pr-map.json). Fourteen native imported heads remain local ancestors. The final cross-repository evaluator PR #14 head `083ed29533ca292fefa4784efac644f57de9735a` remains pinned as the source revision; its five active files retain the exact final Git blob identities, and reviewed kit port `e6c39afdc03d4a044788952eaa6b009eadbba393` is the local ancestor that reconciles those bytes with the combined evaluator tree. Current kit #6/#7 changes were already content-covered by the unified kit, so their ancestry was reconciled without replacing its documentation or payload. Evaluator #3–#10 were reconciled prerequisite-first, then #11/#12 were merged with a separately reviewed correction to the project-memory fixture gate (`c1b471a0658989e4341ad7fcf194d91e93b284fc`). The corrected fixture adds real process-separated recall and injected save/replace failures, not live-backend qualification. PR #14's schema-v2 evidence controls are active: executed records identify the run, host and client mode; executed Bob results require interactive mode, exact version, explicit trust and live observation; non-interactive `bob run` is rejected because it pre-approves tools. Engram and Basic Memory remain optional inert research, not runtime dependencies or licence approval. The runtime-trial JSON validator checks evidence structure, not whether its assertions are true or authorised. Nothing here merges or closes an external PR. Older CI results stay attributed to their exact old heads; final assembled-source review and fresh hosted CI remain separate.

The imported Markdown, nested CI files and contribution instructions are source snapshots, not competing entrypoints. Only root `.github/workflows/` workflows are active in the proposed canonical repository. Original relative links within each subtree remain valid. Root documentation uses the integrated layout.

## Verification

```sh
python3 tools/check_all.py --require-history
```

Requires a full Git checkout for ancestry. A ZIP has no Git ancestry; omit `--require-history` for content-only provenance and offline tests. Git-object-store and checkout mutation tests explicitly skip when the Git executable is absent; their skip counts remain in the report. With Git installed those regressions run normally, even from an extracted ZIP. The Python-only check is not a substitute for full history acceptance. The command separately reports source-byte and history facts; neither establishes live Bob loading or useful task behavior.

The root `.gitattributes` policy preserves exact committed bytes even when Git is configured with `core.autocrlf=true`. A disposable real-Git checkout regression covers that policy; it is not evidence of native Windows execution. Original source identity, inventories and checksums remain unchanged in the source map and are bound to original Git objects and code-level source anchors. Active evaluations deliberately differ after feature porting: the separate [recorded evaluator fork](reviewed-evals-fork.json) binds its complete file inventory to the exact local port commit and a code-pinned manifest digest. Verification checks that fork ancestry, complete current Git tree and worktree bytes separately; it does not relabel changed files as original source. In a ZIP, the checks establish consistency against code-pinned bundled maps, not independent Git history proof. Future accepted evaluator changes require a new explicitly recorded fork revision/map and code-digest review.

## Remaining gates

1. Independent review of the combined tree and intended user journey; correct any confirmed defects.
2. Verify the combined locally ported stack and final archive. Deliberately defective fixtures and historical evidence remain preserved. Evals #5's old internal-result-placement defect is corrected by #6 in the accepted final source tree; the defective intermediate is not an accepted/shipped build. Disposition of the still-open external PRs is a later publication/merge decision.
3. Obtain approval to publish the preparation branch/PR. Refresh full GitHub CI at that exact head; local Linux results do not establish new macOS/Windows CI success.
4. Separately qualify Bob loading and a bounded task on named client versions. Repository consolidation does not establish live client access or qualification.
5. Obtain explicit main-merge/release approval. Only then propose transition notices on old repositories; archiving, deletion and repository renames remain separate decisions.

The existing public [roadmap issue](https://github.com/Saqlain1999/bob-workflow-kit/issues/3) remains the intended discussion record. This preparation does not create a competing public issue or post updates without publication approval.
