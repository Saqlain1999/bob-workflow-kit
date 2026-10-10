# Contributing

Help make Bob setup and substantial coding work easier to understand, resume, and verify. Small reproducible improvements are welcome.

## Good first contributions

- Record an exact IDE/Shell version and fresh-session loading result.
- Improve a confusing setup or recovery instruction.
- Add a realistic public fixture with clear acceptance criteria.
- Reproduce an installer conflict using disposable directories.
- Add a tested stack-specific recipe without changing the global rule for everyone.

Keep contributions scoped. The core uses Python 3.10+ and its standard library; new dependencies need a concrete benefit. Keep the always-loaded rule concise and put details in on-demand references.

## Verification

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

Every test that invokes the installer must select an explicit temporary Bob home. Do not change real home environment variables, call a live model, or alter active Bob configuration during tests. The Tiny Ledger demonstration intentionally has a failing baseline and belongs outside the normal passing installer suite.

For a workflow change, include the actual prompt, a sanitised fixture, the result, and what the check demonstrates. Separate offline tests from live Bob execution. Do not report model performance percentages from a single task.

## Pull requests

Explain the concrete problem, changed behaviour, and relevant validation. Preserve unrelated files. Cite the official product documentation when changing paths, fields, commands, or compatibility statements. Attribute copied material and retain its licence; linked projects are not implicitly part of this repository.

AI-assisted contributions are welcome. The contributor remains responsible for reviewing the diff and reporting the checks that actually ran. Do not fabricate outputs, signatures, support promises, or benchmark results.

## Discussion and reporting

Be specific, considerate, and evidence-based. Critique the behaviour and proposed change, not the person. Use sanitised examples; do not upload private code, tokens, customer data, or confidential logs. See [SECURITY.md](SECURITY.md) for sensitive reports.
