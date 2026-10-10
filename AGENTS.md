# Working on Bob Workflow Kit

This repository distributes instructions for IBM Bob and a small offline Python installer. It does not contain Bob's proprietary implementation.

- Keep source-compatible with Python 3.10+ and the standard library. Run `python3 -m unittest discover -s tests -v` from the repository root for installer tests.
- Every installation test must pass an explicit temporary Bob home. Never write test data to the real user's Bob configuration or call a live model.
- Preserve the intentionally failing Tiny Ledger exercise. Work on disposable copies when demonstrating a fix. Its baseline is separate from the installer suite.
- Keep global rule content short. Put repository facts in repository/task templates, and load detailed skill references only when needed.
- Check current official Bob docs before changing paths, fields, tool names, or hook assumptions. Distinguish documentation, offline validation, and live Bob evidence.
- Keep the installer's managed scope narrow. Preserve unrelated files and local edits; no automatic auth, permission, settings, or MCP changes.
- Update user documentation and validation records when behaviour changes. Do not add a release badge or compatibility claim for an unexecuted test.
- Use original examples and retain licences when incorporating external material.
