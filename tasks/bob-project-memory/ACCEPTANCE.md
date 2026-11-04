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
