# Fidelity check for technical text

Use this reference when an edit could change behavior, obligations, or evidence. Compare the source and revision side by side.

## Exact tokens

Confirm every value and literal token:

- numbers, signs, decimal points, ranges, units, dates, durations, and versions;
- file paths, URLs, commands, flags, environment-variable names, API fields, and error codes;
- capitalization or punctuation when it is part of an identifier or exact message.

Do not “correct” an exact token unless the task includes verifying it against its authoritative source.

## Meaning and force

Check each source statement for:

- actor and affected object;
- action, state, or prohibition;
- precondition and postcondition;
- scope, exception, and sequence;
- certainty and requirement strength;
- evidence source and whether the statement is observed, reported, or inferred.

Pay special attention to small words that change behavior: **not**, **only**, **unless**, **before**, **after**, **at least**, **at most**, **may**, **can**, **should**, and **must**.

## Procedures

Keep prerequisite checks before destructive or irreversible actions. Keep rollback and recovery instructions with the action they protect. Never omit an approval boundary, credential warning, backup requirement, or stop condition to make a procedure shorter.

If two steps can run independently, say so only when the source or implementation establishes that fact. If the order is unknown, retain the original order.

## Final comparison

For each source claim, locate its equivalent in the revision. For each revision claim, locate its source. Resolve any unmatched item before delivery, or disclose it as an intentional addition, deletion, or unresolved ambiguity.
