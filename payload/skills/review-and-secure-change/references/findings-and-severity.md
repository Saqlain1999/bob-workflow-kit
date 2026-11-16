# Findings and severity

## Evidence classes

- **Confirmed defect:** current source or a trusted reproduction demonstrates behavior that violates an accepted criterion or security boundary.
- **Supported risk:** current design and reachable conditions make harm plausible, but the exact failure was not safely reproduced.
- **Coverage gap:** a consequential behavior lacks an adequate trusted check; this is not proof that the behavior is defective.
- **Suggestion:** a non-blocking maintainability or clarity improvement outside the accepted correctness boundary.
- **Unverified hypothesis:** a question that still needs a discriminating check. Do not report it as a defect.

## Severity rubric

Assign severity from the demonstrated or supported consequence, reachability, required access, affected data/users, recoverability, and available mitigation. Include the reasoning; the label alone is not evidence.

- **Critical:** readily reachable compromise or destructive failure with very broad impact and no practical containment. Escalate immediately and avoid publishing sensitive reproduction detail.
- **High:** reachable authorization bypass, cross-user data exposure or corruption, remote code execution, or similarly serious correctness loss in the reviewed path.
- **Medium:** material incorrect behavior, limited data exposure, denial of service, or weakened security that needs ordinary remediation before the next gate.
- **Low:** bounded impact or defense-in-depth issue with a clear precondition and limited consequence.

Repository policy can override these labels. Record the policy source when it does. Never add arbitrary remediation deadlines or compliance claims.

## Minimum finding record

For `REV-###`, record:

1. evidence class, severity, confidence, and why;
2. exact path, symbol, and reviewed state;
3. trigger or prerequisite;
4. observed and expected behavior;
5. consequence and affected boundary;
6. reproduction/check or bounded source evidence;
7. remediation direction and required regression evidence; and
8. whether the finding blocks the next gate.

Redact credentials, tokens, private records, and exploit details that would create unnecessary harm. A recommendation without a demonstrated problem is not a confirmed finding. A fix proposal does not establish that the fix works.
