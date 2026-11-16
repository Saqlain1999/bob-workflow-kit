# Technical Writing Fidelity fixture

This original, standard-library-only fixture contains a technically complete but
hard-to-scan migration note. The participant rewrites `RUNBOOK.md` without
changing the machine-readable `contract.json` or the public tests.

The trusted tests check a deliberately narrow contract: exact technical tokens,
four commands and their order, requirement strength, negation, retry conditions,
and a minimum runbook structure. They do not prove general semantic equivalence,
technical correctness, readability, ASD-STE100 compliance, or Bob behavior.

Prepare a disposable copy with:

```sh
python3 scripts/evaluate.py prepare --task technical-writing-fidelity --output runs/writing-001
```

The original has eight checks and two intentional structure failures. Preserve
it unchanged; evaluate only a prepared workspace.
