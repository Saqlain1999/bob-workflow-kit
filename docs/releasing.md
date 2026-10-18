# Maintaining and releasing this alpha

Public repository: [Saqlain1999/bob-workflow-kit](https://github.com/Saqlain1999/bob-workflow-kit). Current package: **0.1.0-alpha.3**, with the included MIT license. A GitHub release is separate from repository publication. No package-registry name or Marketplace listing is claimed.

## Release gate

1. Review the exact diff, project scope, license, and public-facing examples. Preserve the failing Tiny Ledger baseline and all historical evidence labels.
2. Run `python3 -m unittest discover -s tests -v` from the source to be released. Validate local documentation links and JSON after material documentation changes.
3. Commit the reviewed source. Inspect all six jobs of **Offline validation** for that exact commit: Linux, macOS and Windows with Python 3.10 and 3.12. A workflow definition or a green result for another commit is insufficient.
4. Create the version tag at that tested commit. Build a source archive from the commit, not from an uncommitted working directory. Attach its SHA-256 checksum.
5. Publish a GitHub **prerelease**, with the tag, full commit, CI link, observed check counts, update/removal instructions, and [Try the alpha](try-alpha.md).
6. Keep unexecuted client/OS combinations untested. Live loading can be gathered during a clearly labelled alpha; stable compatibility claims need evidence and a maintenance commitment.

Tag names use `v` plus the content of `VERSION`. Do not reuse a published tag for changed source. Alpha.3 adds a managed skill and changes the payload. The installer still refuses an in-place version change, so users inspect/uninstall from their old checkout and then install from the new one.

## Reproduce the source archive

From a checkout containing the exact tested commit, create `dist/` and use the actual commit SHA in place of `TESTED_COMMIT`:

```sh
python3 -c "from pathlib import Path; Path('dist').mkdir(exist_ok=True)"
git archive --format=zip --prefix=bob-workflow-kit-0.1.0-alpha.3/ --output=dist/bob-workflow-kit-0.1.0-alpha.3.zip TESTED_COMMIT
python3 -c "import hashlib,pathlib; p=pathlib.Path('dist/bob-workflow-kit-0.1.0-alpha.3.zip'); print(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name)" > dist/SHA256SUMS.txt
```

The archive includes the complete checked-in guide, payload, installer/tests, prompts, fixture, and validation records. Open the archive and check `VERSION` and expected paths before upload. Record the Git version if byte-for-byte archive reproduction is required; archive tooling may change serialization across versions. SHA-256 verifies the supplied file's bytes, not publisher identity or Bob compatibility.

Release validation links refer to the commit under the tag. Later documentation may record the completed release, but cannot retroactively change the tagged source or its historical validation record.

## Distribution and feedback

Use the kit as the front door. Keep its description concrete, add relevant GitHub topics, and link [Try the alpha](try-alpha.md) from announcements. The [demo and launch guide](demo-and-launch.md) supplies a real-trial storyboard and a draft announcement for human review. It does not establish that a video, outside message, or community post was published.

Credit existing tools through [alternatives and coexistence](alternatives.md). The contribution is a small usable setup and reproducible evidence, not ownership of general context/checkpoint practices. The exact offering called Propel SDLC for IBM Bob remains unresolved until its primary link is identified.

## Maintenance focus

When Bob changes discovery or extension behavior, review primary documentation and then test the affected mechanism. Keep offline tests, native client loading, task correctness, and human-observed recovery separate. Add exact-version reports rather than a blanket compatibility badge.

Prioritize reproducible installation failures and missed or stale verification over growing the number of skills. Before adding runner or marketplace machinery, complete the [build-versus-adopt decision](https://github.com/Saqlain1999/bob-workflow-runner/blob/main/ROADMAP.md). The companion repositories' implementation status must remain visible.
