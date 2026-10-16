# BugProof: support reports to verified engineering handoffs

Status: SCOPE APPROVED. Implementation explicitly paused by the participant.
The implementation contract is `docs/specs/bugproof.md`; this document preserves
the design rationale. No application code exists.
Mode: hackathon / builder. Date: October 16, 2026, Asia/Karachi.
Supersedes the workflow proposal in `docs/CANDIDATE-REVIEW.md`.

## Product and operator

BugProof investigates an API bug report received by customer support, gives the
support engineer recorded experimental evidence, and carries out the human's
approved engineering handoff and customer reply.

Pitch: "A support report becomes evidence a developer can act on."

The primary operator is a support engineer. The proposed value is less manual
reconstruction and clarification, with a better engineering handoff and a
traceable reply to the reporter. Actual customer adoption and time savings are
unvalidated. Public maintainer accounts support the broader investigation burden,
not proof of demand for this product or its exact market segment.

The demonstration concerns duplicate orders after retrying a failed request.
Order duplication is directly observable; the system does not verify charges.

## Confirmed decisions and premises

- Gmail intake and replies; GitHub for engineering issues. Trello was removed
  because a second engineering queue had no clear purpose.
- Bounded experiments run automatically on a pre-authorized test service.
- Human interpretation and exact publication approval are mandatory. The human
  can correct expected behavior, request clarification, or decline escalation.
- One supported JSON API contract, isolated synthetic fixtures, and a known
  faulty/corrected pair of service versions. No arbitrary repository execution,
  browser agent, production access, automated fix, or payment processing.
- Organizer development approval is confirmed by the participant. fastn remains
  unclear, so fastn MCP is central to both live integrations. Alternate Clouds
  remains mandatory.
- Demonstration accounts, records, and API are owned/controlled by the team.
  No external customer or company partnership has been established.
- Target ready-to-submit time: Oct 17, noon PKT. Official code/deployment freeze:
  12:45 PM PKT. Keep deployment running through closing.

## Complete workflow and why each step survives

| Step | Result | Why it earns its cost |
| --- | --- | --- |
| Read eligible Gmail reports through fastn | Persist source message/thread identity and text | Starts in an actual support channel; usefulness and integration depth |
| Extract claim and required conditions | Structured claim with source evidence, or named missing information | AI interprets unstructured reports; clarity and technical execution |
| Form a bounded experiment | Schema-valid request sequence against the registered contract | Converts a claim into a test; automation depth and distinctive demonstration |
| Execute and record observations | HTTP trace, order records, fixture and service version | Establishes what happened independently of the LLM's explanation; reliability |
| Human chooses disposition | Escalate, clarify, or reply with a qualified observation | Human supplies product judgment and context; theme alignment |
| Preview exact actions and approve | Version-bound approval of issue body/labels and email reply | Meaningful control with reviewable consequences; theme and UX |
| Execute through fastn and read back | GitHub issue link where required and verified Gmail sent-message identity | Completes the handoff and communication; reliability and usefulness |

The first build may use an explicit "Check inbox" trigger. The remainder is an
automated pipeline. Scheduled polling is optional polish, not a critical feature.
Use an intake label and exclude the agent's own outbound messages to prevent
reply loops. Persist source IDs so repeated checks do not repeat work.

Insufficient or unsupported reports bypass the runner and propose a precise
clarification. Missing customer facts must stay missing. Fresh synthetic test
inputs may be generated and explicitly identified as experimental inputs, rather
than falsely described as the customer's original records.

## What completion means

- For escalation: the approved evidence-backed GitHub issue exists, and the
  approved reply linking that issue was sent to the original test reporter.
- For clarification: the approved question was sent in the original thread;
  the case remains awaiting information. Do not create an engineering issue.
- For a result that does not reproduce the claim: the human may request more
  evidence or send a carefully qualified reply. No automatic dismissal/closure.
- If GitHub succeeds but email fails, show "issue created; reply pending" and
  retry only the remaining action. Partial success is not complete success.

This is completion of a support investigation/handoff, not a promise of a fix.

## Human judgment and authorization

The evidence view separates the reporter's claim, configured expectation,
observed behavior, and proposed disposition. A reproduced discrepancy is not an
automatic root-cause finding or proof that the same result occurred in the
customer's environment. Changing an expectation requires reevaluating the
assertion; changing the request plan requires a fresh run.

The human edits the disposition, issue, and reply before one final publication
approval. Approval binds to the current source, experiment/evidence, environment
identity, and exact external payloads. Changed content invalidates approval.
An AI-generated instruction to skip approval cannot grant authority.

Keep provider credentials in the server integration layer. The model returns a
typed proposal, and a fixed executor validates it; it does not receive a general
execute-tool capability with publication authority. Approved publication uses a
separate authenticated server endpoint and persisted action ledger.

The support workspace requires authentication even for the demo. A dedicated
reviewer login is included in submission materials if needed.

## Experiment boundary

The trusted lab API supports isolated runs, order creation with a retry identifier,
and reading that run's orders. The faulty version can commit an order and return
a simulated failure; repeating the same request creates another order. The
corrected version preserves the retry identity and returns the original order.

Capture actual HTTP calls and state; do not supply a prewritten verdict. Test
paraphrases and changed cart values to check that the pipeline is not a report-ID
lookup. Scope support to sequential retry; races and universal checkout behavior
are deferred.

The runner accepts only known operations against server-configured targets,
with limits on steps, requests, payload size, runtime, and response capture.
It cannot accept arbitrary hosts or execute generated scripts. Each run owns
its fixture; unrelated cases cannot share orders. Fixture endpoints are internal
or authenticated. An experiment failure is distinct from non-reproduction.

All lab observations and outbound demonstration messages are identified as
synthetic/test-service results. Never imply the system tested a real merchant's
production payment flow or repaired an unaffiliated project.

## Small implementation

One Python/FastAPI service, a compact server-rendered support workspace, SQLite
for cases/runs/approvals/action results, and one configured structured-output LLM.
Pin dependencies during implementation using current provider documentation.
fastn MCP connects Gmail and GitHub; its actual account capabilities must be
proved before UI investment. No vector database, agent swarm, graph database,
or separate queue service is justified for this bounded demonstration.

Persist before and after external actions. Use stable case/action identifiers,
provider IDs and reconciliation checks to prevent duplicate issues and replies.
Sending mail can succeed even if the request times out: reconcile the sent
message before retrying. A restart retains completed actions; interrupted
experiments recover or restart in a fresh fixture and remain visibly interrupted
until resolved.

Basic workspace: case list; source email; claimed/expected/observed behavior;
expandable request trace; editable disposition and outbound previews; one
publication control; external result links and a visible partial-failure state.
No analytics dashboard or chat interface is needed.

## Acceptance checks

1. An eligible real test email is imported through fastn and creates one case.
2. The duplicate-order claim produces two distinct recorded orders in the faulty
   service, with matching retry identity and inspectable responses.
3. The same claim against the corrected version produces one order, and is not
   automatically labeled a false report.
4. A missing condition yields a clarification draft without invented evidence.
5. A report containing tool/prompt instructions cannot publish or change targets.
6. Human rejection creates no issue or email. Direct publication without a valid
   current approval fails at the server, regardless of UI state.
7. Altering approved content invalidates approval. Repeated approval submissions
   and inbox checks do not duplicate external actions.
8. GitHub-success/email-failure is visible and recoverable; read-back links and
   provider message IDs substantiate completion.
9. A restart preserves completed external actions and does not report an
   interrupted experiment as completed.
10. The Alternate Clouds deployment works using its configured PORT and stored
    environment variables; evidence is captured from the deployed version.

Measure elapsed investigation and review time during rehearsal. Report the
measured demo result, not a hypothetical industry-wide saving. A sub-minute
bounded run is a target, not a guaranteed claim.

## Alternatives and cuts

- Summary/checklist-only assistant: faster but does not independently observe
  reported behavior; rejected as the central value.
- Bounded API evidence plus approved handoff: selected approach.
- Arbitrary repositories, browser reproduction and autonomous fixes: attractive
  future scope, rejected for deadline, execution complexity and reliability.
- Trello, payments, broad dashboards, automatic severity scoring, autonomous
  customer promises and blanket "no bug" verdicts: removed from the MVP.

## Adversarial review and adjustments

This review is in-host, not an independent reviewer verdict. No subagents were
used because project instructions require explicit delegation authorization.
Native gstack helper readiness is limited by the recorded Windows application
control issue; no native-review success is claimed.

Pass 1, completeness: an issue alone leaves the reporter uninformed. Retain the
approved thread reply and explicit clarification completion path.

Pass 2, consistency: "reproduced" and "confirmed customer bug" are different.
Separate observation, environment, human disposition and root-cause claims.
Keep the corrected-version and missing-information paths.

Pass 3, feasibility: arbitrary execution, duplicate queues and per-run approval
friction undermine the deadline. Restrict the runner, remove Trello, and retain
one consequential publication approval. Integration verification and early
deployment precede feature work. No buyer adoption has been established.

Remaining external dependencies: fastn account actions, Gmail/GitHub authorization,
LLM key, Alternate Clouds account/deployment access and persistence behavior.
Until those are tested, feasibility remains conditional. No fake integrations
may be presented as live.

## Build order and distribution

1. Verify read/send in a controlled Gmail thread and create/read an owned GitHub
   issue through fastn. Obtain secrets through secure configuration, never chat.
2. Deploy a minimal authenticated service to Alternate Clouds and verify health,
   listening PORT and persistence. Follow the event guide's Rebuild → Deploy.
3. Build one vertical path from email to actual evidence, human review, issue,
   and reply. Exercise it on the deployed application.
4. Add the corrected-version/clarification cases and meaningful failure checks.
5. Refine the evidence/decision view and record the 2–3 minute demo video.
6. Prepare the submission PDF and exact five-minute slide presentation. Team
   members write their own LinkedIn post/reshare; grammar help only. Finish by
   noon, preserve the official 12:45 PM freeze, keep deployment running.

Distribution is the Alternate Clouds URL with reviewer login, plus accessible
source repository. Deployment is an explicit rebuild/deploy, not assumed from
a GitHub push. A separate automatic release pipeline is outside MVP scope.

## Final alignment

The participant approved this scope and then explicitly instructed that
implementation must not start yet. Specification synthesis is authorized;
account checks, application development and deployment await a direct resume.
