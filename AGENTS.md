# Working on Bob Workflow Kit

This repository distributes instructions for IBM Bob and a small offline Python installer. It does not contain Bob's proprietary implementation.

- Run `python3 tools/check_all.py` for all offline quality checks; `--require-history` additionally requires preserved source ancestry. Installer-only checks remain `python3 -m unittest discover -s tests -v`.
- Imported evaluation, catalogue and design snapshots are mapped in `docs/consolidation/source-map.json`; preserve original licences and validation attribution. Open PRs are not part of the imported main baseline.
- Keep source-compatible with Python 3.10+ and the standard library.
- Every installation test must pass an explicit temporary Bob home. Never write test data to the real user's Bob configuration or call a live model.
- Preserve the intentionally failing Tiny Ledger exercise. Work on disposable copies when demonstrating a fix. Its baseline is separate from the installer suite.
- Keep global rule content short. Put repository facts in repository/task templates, and load detailed skill references only when needed.
- Check current official Bob docs before changing paths, fields, tool names, or hook assumptions. Distinguish documentation, offline validation, and live Bob evidence.
- Keep the installer's managed scope narrow. Preserve unrelated files and local edits; no automatic auth, permission, settings, or MCP changes.
- Update user documentation and validation records when behaviour changes. Do not add a release badge or compatibility claim for an unexecuted test.
- Use original examples and retain licences when incorporating external material.
