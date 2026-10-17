# BugProof competition scorecard

Rubric and event constraints below were supplied by the participants; they are
not independently reconfirmed here. Total: **100 points**. No score is awarded
or predicted. Current product evidence: NOT_RUN; implementation resumed under DEC-16.
Use [ACCEPTANCE.md](../ACCEPTANCE.md) for current results and runnable evidence,
not a second copy of the pass/fail ledger.

## Criteria -> behavior -> proof

| Criterion | Weight | Concrete case for BugProof | Evidence required | Short-demo proof |
| --- | ---: | --- | --- | --- |
| Technical execution / reliability | 25 | Actual HTTP observations; durable state; no duplicate effects; honest partial/uncertain outcomes | A02–A03, A06–A07, A10–A16 | Show distinct order IDs, actual trace/build, then verified issue/reply; recover one partial failure in rehearsal |
| Usefulness / real-world impact | 20 | Support engineer converts a vague report into actionable evidence and a specific reporter response | A01–A05, A13, A16; measured rehearsal timing; demand remains unvalidated | Open the original report, finish the handoff, show exactly what engineering/reporter received |
| Theme: Human + AI | 15 | AI proposes and investigates; human changes expectation/disposition or rejects publication; server enforces that choice | A09–A10, A14, A17 | Change an expectation or choose clarification; show that rejection causes zero external writes |
| Creativity / uniqueness | 15 | Distinguish claim, expectation and observed state; replay corrected behavior without an automatic false-report verdict | A02–A05, A09 | Same claim, different observed API behavior; missing facts lead to an actual clarification path |
| Automation depth / integration | 15 | fastn Gmail intake -> structured plan -> bounded run -> human authorization -> GitHub issue -> original-thread reply -> read-back | A01–A02, A12–A16 | Trace one complete connected case; doubles alone cannot establish this criterion |
| UX / presentation | 10 | Source, evidence, human decision and result are understandable in one case workspace | A17; timed video/presentation rehearsal | Progressive trace detail, clear partial/error states, concise narration and visible final links |

Creative contribution is a proposed workflow distinction, not a global uniqueness
claim. Lab evidence supports a demonstrated workflow, not proven commercial
adoption, guaranteed time savings or production diagnosis.

## Build priority under the deadline

1. Verify fastn account actions/read-back and durable Alternate Clouds deployment.
2. Prove faulty/corrected actual API behavior, then finish one escalation end to end.
3. Prove meaningful human rejection/editing, missing-information reply and recovery.
4. Rehearse, record and submit. Extra features do not outrank a complete reliable path.

Demo video: **2–3 minutes**. Start with the support report, spend most time on
evidence and human judgment, finish with the actual issue and thread reply.
Use brief corrected/missing-information replays; supporting adverse-case evidence
can be linked rather than narrated in full. Finalist presentation is **exactly
five minutes**: problem/value, implementation/authority, demo/proof, limits/result.

## Eligibility and submission evidence

All items below are currently unverified/not prepared unless linked later.
These participant artifacts are separate from product acceptance passes.

| Requirement supplied by participants | Required artifact / check | Current evidence |
| --- | --- | --- |
| Two-student team | Team name; both names, emails and registered Discord usernames; one WhatsApp contact | — |
| Mandatory Alternate Clouds | Accessible live deployment and deployment screenshot; run until closing | — |
| fastn discrepancy | Retain fastn centrally; organizer clarification still outstanding | — |
| Submission PDF | Project/pitch, problem/users, meaningful human step, stack, live URL, accessible repository or n8n export | — |
| Demo access and video | Dedicated login if needed; accessible 2–3 minute video link | — |
| Discord evidence | Both memberships, required names/event channel; watch submission instructions and updates | — |
| Social evidence | Participant-written English original LinkedIn post plus teammate reshare; required hashtags below | — |
| Credit and secrets | Third-party credits; repository/artifacts contain no credentials | — |
| Final freeze | Submit by October 17, 2026, 12:45 PM PKT; target noon; record final source/deployment; no subsequent code/deploy edits | — |
| Finalist slides | Prepare beforehand; PDF before 4 PM October 17; top ten expected around 3:30 PM | — |

Required hashtags: `#AgentikaAIHackathon #AIAutomation #AIHackathon #BuildInPublic`.
Participants write LinkedIn/Twitter text themselves; assistance is grammar-only.
English communication is required under supplied rules. Confirm the separate
referenced "handoff doc" and submission destination from organizers; neither is
resolved by this repository. The October 16, 9 PM PKT check-in was listed in
the opening slides; participants should follow current organizer updates.

## Update discipline

Link current acceptance records and participant artifacts; do not invent scores.
After a scope change, re-evaluate which criterion loses proof before adding work.
When a claim is not supported, narrow the narration or obtain evidence. Verify
links/access from the judge's perspective before the submission freeze.
