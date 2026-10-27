# One-product consolidation preview

Status: local preparation, not publication or a release. The canonical product is **Bob Workflow Kit**: one checkout, one installation, one first-use guide and one intended issue tracker. This branch does not change Bob's proprietary client or the installed alpha.4 payload.

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

Only each repository's current `main` was imported. Existing open PR branches are **not silently included or merged**. Their exact heads, original bases and proposed destination prefixes are listed in the [open-PR map](open-pr-map.json). This includes the newly discovered evaluator #9, which was not part of the original saved eight-PR evaluation inventory; it needs its own review. Older successful CI remains head-specific evidence, not approval of a new consolidated head.

The imported Markdown, nested CI files and contribution instructions are source snapshots, not competing entrypoints. Only root `.github/workflows/` workflows are active in the proposed canonical repository. Original relative links within each subtree remain valid. Root documentation uses the integrated layout.

## Verification

```sh
python3 tools/check_all.py --require-history
```

Requires a full Git checkout for ancestry. A ZIP has no Git ancestry; omit `--require-history` for content-only provenance and offline tests. The command separately reports source-byte and history facts; neither establishes live Bob loading or useful task behavior.

The root `.gitattributes` policy preserves exact committed bytes even when Git is configured with `core.autocrlf=true`. A disposable real-Git checkout regression covers that policy; it is not evidence of native Windows execution. The byte-preservation check intentionally freezes the imported baseline during this preparation. Later ported fixes must record an explicit reviewed delta and fresh verification; do not overwrite original source attribution to make an altered snapshot look unchanged.

## Remaining gates

1. Independent review of the combined tree and intended user journey; correct any confirmed defects.
2. Review and port outstanding stack changes, prerequisite-first, to their new paths. Keep deliberately defective fixtures defective and preserve historical evidence. Evals #5 has a known result-placement defect at its old head; #6 contains its correction. Do not ship that intermediate defect.
3. Obtain approval to publish the preparation branch/PR. Refresh full GitHub CI at that exact head; local Linux results do not establish new macOS/Windows CI success.
4. Separately qualify Bob loading and a bounded task on named client versions. Repository consolidation does not establish live client access or qualification.
5. Obtain explicit main-merge/release approval. Only then propose transition notices on old repositories; archiving, deletion and repository renames remain separate decisions.

The existing public [roadmap issue](https://github.com/Saqlain1999/bob-workflow-kit/issues/3) remains the intended discussion record. This preparation does not create a competing public issue or post updates without publication approval.
