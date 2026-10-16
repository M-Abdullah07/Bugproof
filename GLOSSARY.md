# BugProof

BugProof supports the handoff of reported API problems from customer support to engineering.

## Language

**Reporter**:
The person describing unexpected behavior and asking for help.
_Avoid_: Confirmed bug owner

**Support engineer**:
The person responsible for investigating a report and deciding its next disposition.
_Avoid_: Autonomous judge

**Report**:
A reporter's account of observed and expected behavior. A report is a claim, not proof of a defect.
_Avoid_: Confirmed bug

**Disposition**:
The human decision about how a report should proceed, such as engineering escalation or a request for more information.
_Avoid_: AI verdict

**Reproduction**:
An attempt to observe the reported behavior in a specified test environment.
Failure to observe it does not establish that the reporter's experience was false.
_Avoid_: Proof that no bug exists

**Evidence bundle**:
The recorded experiment inputs, observed responses, relevant order records,
and environment identity supporting a reproduction result.
_Avoid_: Generated explanation alone

**Escalation**:
A support engineer's decision to hand a report and its evidence to engineering.
_Avoid_: Automatic confirmation of root cause
