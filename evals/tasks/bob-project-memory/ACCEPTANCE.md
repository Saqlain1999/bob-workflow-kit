# Acceptance checklist

- [ ] The prepared baseline reproduced only the named expected failures.
- [ ] Fresh-process recall returned the current Project Alpha decision.
- [ ] Identical keys in Alpha and Beta remained isolated.
- [ ] Cross-project promotion was explicit, sanitized, and provenance-bearing.
- [ ] D2 superseded D1 while ordered history remained available.
- [ ] A changed source hash made the older record visibly stale.
- [ ] A stale expected revision was refused without losing the current value.
- [ ] An interrupted temporary write did not corrupt committed state.
- [ ] Hostile instruction-like content remained untrusted data.
- [ ] Deletion removed direct, historical, and indexed retrieval.
- [ ] Backend outage reported unavailable and pointed to repository evidence.
- [ ] Only `memory_adapter.py` and `MEMORY_HANDOFF.md` changed.
- [ ] The handoff distinguishes offline checks from live Bob and production evidence.

Passing public checks does not prove durable concurrency, backup erasure,
multi-process safety, live-client discovery, or a third-party backend's behavior.

## Corrected automatic gate and remaining manual boundaries

The automatic gate now includes distinct, sequential writer and reader Python
processes sharing only a retained state directory. The original fresh-object
check remains a narrower same-process check. Neither is live Bob/backend recall.

Identifiers use exactly the three scopes in `contract.json`: `project-alpha`,
`project-beta`, and `shared-lessons`. All key-based operations reject unknown
scopes and colon-delimited ambiguous keys, as well as the existing unsafe path
segments; listing validates its scope. Same-key writes and listings remain isolated.

Save recovery is checked by injecting a partial `Path.write_text` failure during
an actual `put`, and separately a `Path.replace` failure. Both must propagate the
error, preserve the exact previous committed bytes and fresh-object readability,
and remove failed temporary output. This is a path-specific local JSON fixture
contract, not a generic backend fault injector. The original orphan-temp check
only proves that an unrelated malformed temporary file is ignored on load.
No process-kill, power-loss, fsync, disk-full, or durable transaction claim follows.

A stale independent instance must refuse an outdated expected revision after a
completed sequential write by another instance, preserving committed bytes.
Reload-before-check in the repaired control does **not** make the check and write
atomic across processes or threads. Concurrent writers, stale independent delete
and promotion interleavings, and general CAS/transaction safety remain unqualified.

Manual checklist items are not automatically closed by a green helper:

- `source_hash` values are caller-supplied opaque freshness tokens. Equality and
  mismatch signaling are tested; hashing current evidence and binding it to an
  ingested record are not implemented and require independent review.
- Promotion checks only explicit caller-provided summary bytes and a trust label.
  It does not establish sanitizer effectiveness, authorization, or originating
  project/key/revision provenance. The provenance-bearing checklist item is manual.
- Outage checks simulate a Boolean-disabled **recall** and its evidence-path
  exception. The control additionally refuses `put`; history/list/delete/promotion
  are not qualified as a coherent outage surface. No real connection failure or
  actual fallback evidence read is tested.
- Hostile bytes remain inert record data in these examples; no model/tool executor
  is exercised. Deletion checks local logical retrieval, not backups/raw erasure.
- Handoff phrase checks cannot validate a handoff's truth; inspect it manually.

Public checks, manual acceptance, external asset verification, backend runtime
qualification, and live Bob observation are separate evidence layers. The last
three remain **NOT RUN**, not implied by fixture green. The helper is cooperative
verification, not an adversarial sandbox; use an independently approved isolated
executor and a nonsecret allowlisted environment for unknown candidate code.
