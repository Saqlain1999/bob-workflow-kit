---
name: write-clear-technical-content
description: Draft or revise technical instructions, errors, runbooks, handoffs, API text, and agent messages so they are direct and difficult to misread while preserving every technical fact and level of certainty.
---

# Write clear technical content

Use this skill when the user asks to create, simplify, disambiguate, or review technical text. Do not activate it merely because a coding task includes ordinary conversation. This is a clarity and fidelity workflow, not a claim of compliance with ASD-STE100 or another controlled-language standard.

## Establish the contract

Identify the reader, the action the text must support, and the requested output format. Treat existing repository terminology and documented style rules as authoritative. If the text is contractual, legal, regulated, safety-critical, or quoted from an external specification, do not silently paraphrase authoritative wording.

Before rewriting, make a private fidelity ledger of content that must survive unchanged in meaning:

- numbers, units, dates, thresholds, versions, and time limits;
- paths, commands, identifiers, option names, error codes, and quoted strings;
- negation and requirement strength such as **must**, **must not**, **may**, **should**, and **can**;
- conditions, exceptions, prerequisites, ordering, ownership, and security or safety warnings;
- uncertainty, attribution, and the difference between observed evidence and inference.

Read `references/fidelity-check.md` when the source contains requirements, commands, numerical values, or safety/security conditions. Read `references/writing-patterns.md` when choosing a structure or reviewing a draft. Do not load both references by default for a small rewrite.

## Draft or revise

Use the same term for the same concept. Prefer a direct verb and name the actor when the actor matters. Put one user action in each procedural step. Split long sentences when the split does not change scope or precedence. Use a list for three or more parallel items or ordered actions.

Remove filler, unsupported praise, and repeated conclusions. Keep necessary domain terms, and define an unfamiliar term once when the reader needs the definition. Do not replace exact commands, identifiers, or error text with friendlier approximations.

Shorter is not automatically clearer. Keep a longer sentence when splitting it would detach a condition, exception, or qualifier from the statement it governs.

## Verify fidelity

Compare the revision with the source, not only with memory. Check every fidelity-ledger item. Confirm that the revision did not:

- turn a possibility into a fact or a recommendation into a requirement;
- broaden or narrow who, what, or when the statement covers;
- reorder dependent steps;
- invent a cause, capability, result, or guarantee;
- remove a failure mode, warning, exception, or unresolved limitation.

If the source is ambiguous, preserve the ambiguity only when it is authoritative text that must remain exact. Otherwise, name the ambiguity and request or state the assumption instead of guessing silently.

## Return the requested artifact

By default, return the revised text without a long explanation. If the user requests a review, return concrete findings with the affected passage, the risk of misreading it, and a proposed revision. If fidelity cannot be preserved, identify the exact conflict rather than presenting a lossy rewrite as complete.

Keep evidence labels honest. A style check can find structural patterns; it cannot prove semantic equivalence, technical correctness, regulatory compliance, or successful execution.
