# Local evaluator consolidation-port validation

Recorded by Hermes Agent <hermes@localhost> on 27 October 2026 (UTC),
Linux / Python 3.13.5. This is separately attributed local port evidence, not a
replacement for any historical record in VALIDATION.md and not hosted CI or a
Bob participant result.

## Exact imported candidate

- Preview base: `7695946685fbd10c6b751a28699e9b3c0de7fb8d`.
- Accepted evaluator baseline: `5e2075ab510d947675c3e2e824ff384de899dc1a`.
- Source reconciliation head: `c48c2f8d3e397d8ea5b74bc1fc387444930a82b6`.
- Subtree import commit: `56253a3146add055e044b15fc3a30de515bf53e0`.
- Imported evaluator tree: `ed934492c974a1c4b18f80737d45282718323340`.

The reviewed #3 reconciliation already contains the accepted baseline. Original
reviewed #4, #5, #6, #7, #8 and #9 heads were then merged prerequisite-first in
an isolated local source-layout branch without conflicts, followed by a
history-preserving subtree merge under evals/. All seven supplied reviewed
heads, accepted baseline and preview base are ancestors of the imported branch.
No original candidate commits were rewritten. The imported tree exactly matched
the reconciled source tree before adding this validation document.

Slice #5's intermediate internal-result-placement defect is historical, not
accepted or shipped by this port. The final imported tree includes #6's
correction. The final source state, not the defective intermediate, was tested.

## Executed checks

| Check | Observed result |
| --- | --- |
| Source-layout full helper suite | 104 tests passed, exit 0, no skips; ResourceWarning treated as error |
| Integrated evals/ full helper suite | 104 tests passed, exit 0, no skips; ResourceWarning treated as error |
| All nine tasks: prepare then baseline | All prepared successfully; all reported expected_baseline_failure, exit 0 |
| Reminder implementation independent good control | 10 trusted checks passed; public_tests_passed, exit 0 |
| Reminder implementation internal result, baseline phase | helper_error, exit 2; no result file; workspace unchanged |
| Reminder implementation internal result, repaired candidate phase | helper_error, exit 2; no result file; workspace unchanged |
| Existing external result negative control | helper_error, exit 2; existing result not overwritten |
| Intentional source fixtures | All 82 tracked fixture files byte-identical to reviewed #9 |
| Accepted main pipe/watchdog retention | Bounded-process function AST unchanged; all baseline evaluator test methods retained; inherited-pipe watchdog passed in both full suites |
| Historical accepted-baseline validation | Complete original record retained verbatim after its document heading |
| Static syntax | 43 Python files parsed with Python 3.10 grammar; 3 JSON files parsed |
| Whole-tree local links before this link-free document | 179 links across 139 Markdown files, no errors |
| Root original-byte provenance gate | Expected exit 1: six changed original evaluator files rejected; original source ancestry/inventory/blob checks verified |

Full suites include trusted-test tampering, protected-input mutation, unrelated
candidate files, malformed/skipped evidence, bounded diagnostics, timeout,
known-good task artifacts and intentionally failing baselines. Temporary good
artifacts are software controls, not work by Bob. Correct review or release
handoff artifacts can pass while reporting deliberately unresolved defects and
keeping release blocked.

Checks used an allowlisted provider-free environment and disposable HOME/TMPDIR
under the existing profile scratch root. No network, Bob/model calls, private
histories, credentials, remote writes, publication or default-branch merges were
performed. Root kit payload, documentation, quality tooling and source-map were
not modified. Only evals/ differs from the preview base.

## Remaining boundaries

The original-byte provenance gate remains unchanged and intentionally fails for
CONTRIBUTING.md, README.md, VALIDATION.md, docs/protocol.md,
fixtures/README.md and scripts/evaluate.py under evals/. The parent must record
reviewed fork deltas without changing original source hashes before a combined
provenance pass can be claimed. This port does not claim that pass.

Local Linux helper success establishes neither native Windows/macOS execution,
hosted checks for these new merge commits, hostile-code sandboxing, descendant
containment, manual acceptance, live Bob activation, production readiness nor
release approval. External PRs were not merged, closed or otherwise changed.
