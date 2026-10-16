# BugProof MVP specification

Scope: approved by the participant. Testing boundary: approved.
Execution: **HELD — documentation only until the participant explicitly resumes implementation.**
Tracker: GitHub Issues, M-Abdullah07/Bugproof. Issue publication pending. Intended issue label:
`ready-for-agent`; that label never overrides the execution hold.
Date: October 16, 2026, Asia/Karachi.

## Problem Statement

A support engineer receives an API problem report in email. Before handing it to
engineering, they must reconstruct the claim, obtain missing conditions, attempt
reproduction, distinguish observed behavior from an assumption, and communicate
the next step. A polished summary alone does not establish what happened.

The MVP investigates one concrete class of report: duplicate orders after a
failed request is retried with the same retry identifier. The engineer needs
recorded experimental evidence and control over the disposition and external
communication. The system verifies order records, not financial charges.

Public evidence establishes a broader investigation burden. Demand, adoption,
and time savings for this specific support workflow remain unvalidated.

## Solution

A support engineer checks an authorized Gmail intake, receives an automatically
generated and executed bounded experiment against a registered test API, and
reviews the report beside the evidence bundle. The human can correct the expected
behavior, choose the disposition, and edit the proposed communication.

After explicit approval of the exact actions, BugProof uses fastn MCP to create
an engineering issue in GitHub when warranted and reply in the original Gmail
thread. It verifies external results and exposes partial failures rather than
reporting premature success.

The three core demonstrations are a reproducible duplicate order, the same claim
against a corrected service version, and a report requiring clarification.
Synthetic reports and the laboratory service are clearly identified.

## User Stories

1. As a support engineer, I want eligible Gmail reports imported into a case list,
   so that investigation starts in my existing communication channel.
2. As a support engineer, I want repeated inbox checks to preserve a single case,
   so that the same report does not generate duplicate work.
3. As a support engineer, I want to inspect the source message and its provenance,
   so that a generated interpretation can be checked against the report.
4. As a support engineer, I want the claimed and expected behavior separated,
   so that customer statements do not become established facts accidentally.
5. As a support engineer, I want missing conditions named precisely,
   so that I can ask an actionable clarification question.
6. As a support engineer, I want a schema-valid experiment generated automatically,
   so that I do not manually translate every report into request steps.
7. As a support engineer, I want experiments confined to an authorized test service,
   so that investigation does not affect customer production data.
8. As a support engineer, I want independent fixtures for each experiment,
   so that another case cannot contaminate its evidence.
9. As a support engineer, I want actual request, response and order observations,
   so that an LLM explanation cannot substitute for execution.
10. As a support engineer, I want the environment and service version recorded,
    so that the limits of the result are visible.
11. As a support engineer, I want the corrected service replayed with the same claim,
    so that conclusions follow observed behavior rather than the report's wording.
12. As a support engineer, I want non-reproduction distinguished from an execution
    error, so that a broken experiment does not discredit a valid report.
13. As a support engineer, I want to revise the expected behavior,
    so that product judgment remains with a responsible person.
14. As a support engineer, I want to escalate, clarify, or send a qualified reply,
    so that the next step fits the evidence rather than an automatic verdict.
15. As a support engineer, I want editable previews of every outbound action,
    so that the communication and engineering handoff reflect my decision.
16. As a support engineer, I want rejection to create no external writes,
    so that review is a real authorization boundary.
17. As a support engineer, I want changed source or action content to invalidate
    prior approval, so that obsolete permission cannot authorize a new action.
18. As a developer, I want an escalated issue to contain the exact reproduction
    and its limitations, so that I can investigate without reconstructing the email.
19. As a reporter, I want a reply in the original thread with the approved next
    step, so that I know whether engineering needs to act or I need to clarify.
20. As a support engineer, I want external result links and message identities,
    so that I can verify the handoff and reply actually exist.
21. As a support engineer, I want partial publication failures visible and
    recoverable, so that retrying does not duplicate completed actions.
22. As a support engineer, I want completed actions preserved across restarts,
    so that a worker interruption does not resend communication.
23. As a demo reviewer, I want authenticated access to a deployed, resettable
    demonstration, so that I can distinguish a working workflow from a recording.
24. As a participant, I want measured rehearsal results and an honest scope,
    so that the submission claims only behavior the deployed system demonstrates.

## Implementation Decisions

### Application and integration boundaries

Use one Python/FastAPI application, a compact server-rendered support workspace,
and SQLite persistence. A single structured-output LLM proposes interpretations,
request plans and communication; a fixed executor controls effects. Additional
agent personas, a vector database and a separate message broker are unnecessary.

Modules have five responsibilities: case orchestration/persistence; structured
AI proposals; bounded experiment execution and evidence; review/authorization;
and fastn-backed publication/reconciliation. Their boundaries follow ownership
of state and authority rather than one function per workflow step.

fastn MCP is the core integration layer for Gmail and GitHub. Actions must be
proved against the connected accounts before feature development is treated as
feasible. Provider credentials remain in server configuration. The model has
neither credentials nor a general-purpose publication tool.

The first vertical slice may start through an explicit authenticated "Check
inbox" action. Scheduled polling is optional and must not delay the complete
workflow. Gmail intake uses a configured label and controlled mailbox; exclude
the application's own outbound messages to prevent recursive case creation.

### Case identity and source revisions

A case belongs to an authorized mailbox and Gmail thread. Retain message IDs,
the eligible inbound message snapshot and a monotonically increasing source
revision. Reimporting unchanged inbound messages is idempotent. A new eligible
reporter message updates the source revision, preserves prior history and
invalidates stale drafts/approvals. Application-sent replies do not count as new
reporter evidence. Do not silently merge unrelated threads.

Persist the case, source revisions, interpretations, experiment plans/runs,
evidence bundles, human dispositions, action previews, approvals and publication
attempts. Evidence and previous approvals remain inspectable after revision.

### Structured interpretation and experiment contract

An interpretation identifies the claim, reported steps/conditions, source
excerpts, missing facts, and whether the claim fits the supported API contract.
Excerpts must resolve to the imported source. An invalid or ungrounded proposal
does not progress to execution. Allow at most one schema-correction attempt;
subsequent failure becomes a visible proposal error.

An experiment contains a registered target reference, fixture reference,
permitted operation sequence, synthetic inputs, expected observation/assertion
and evidence links. The model may select supported operations and parameters,
but cannot provide an arbitrary URL, HTTP headers containing credentials, shell
commands or executable code. Generated synthetic inputs are labeled as such;
they are not attributed to the original customer.

For the lab, the configured expectation is that identical sequential order
requests with the same retry identifier and payload resolve to one order.
Missing information that prevents choosing a justified experiment results in a
clarification proposal, not an invented reproduction or a negative verdict.
Unsupported claims such as duplicate payment charges remain unsupported.

### Bounded runner and lab service

Register one trusted JSON API contract with isolated per-run order fixtures,
order creation and fixture-scoped order inspection. The faulty build commits the
first order but returns a simulated failure; an identical retry creates another
order. The corrected build preserves retry identity and returns the original
order. Exercise actual HTTP behavior and state, not a stored answer keyed by the
report or service version.

The runner enforces target, operation and fixture boundaries server-side. Initial
limits are eight HTTP requests per experiment, 30 seconds elapsed runtime,
16 KiB request bodies and 64 KiB captured response bodies. Exceeding a limit is
an explicit execution error; truncated captures are marked and cannot support
assertions that depend on omitted content. Fixture setup/reset requires internal
or authenticated authority. These limits are implementation defaults, not
additional product capabilities.

Record the immutable request sequence, sanitized responses, status codes,
relevant order records, retry identifiers, fixture identity, timestamps,
assertion outcome and observed service build identity. Redact credentials and
unnecessary personal data before logs, model context or publication.

Use distinct outcomes: reproduced discrepancy; not reproduced under stated
conditions; insufficient information; unsupported claim; execution error.
An LLM cannot manufacture an execution result or promote a partial run to proof.

### Human review and case transitions

The workspace presents a case list and a single case review view: source,
claim/expectation/observation, trace, disposition, editable outbound previews,
publication control and external result status. Essential controls work without
reading raw JSON; the detailed trace remains expandable. No chat UI or analytics
dashboard is needed.

Imported cases progress to investigation or clarification review. Successful
investigation yields evidence ready for human review; execution errors remain
errors until retried or dispositioned explicitly. The human can escalate,
request clarification, or send a qualified observation without escalating.
Not reproduced never automatically closes or dismisses the report.

Changing expected behavior reevaluates the assertion against existing complete
observations. A changed request plan, target build or fixture requires a new
experiment. Both changes invalidate affected previews and approvals. Retain
history rather than overwriting the old result.

### Approval and publication contract

The authenticated human approves the exact disposition, destinations and
payloads after viewing them. Approval binds to the case/source revision,
effective expectation, plan/evidence identity, observed target build and action
payload fingerprint. It records the reviewer and time. Enforce a configurable
approval lifetime, initially 15 minutes; content/version changes invalidate it
regardless of age. Recheck at each external write. A claim from the email, model
or browser client cannot create authorization.

Publication actions are generated from the approved disposition:

| Disposition | GitHub action | Gmail action | Completion |
| --- | --- | --- | --- |
| Escalate | Create one evidence-backed issue in the configured owned repository | Reply in the original thread with the resulting issue link | Both actions verified |
| Clarify | None | Send the approved specific question in the original thread | Reply verified; case awaits information |
| Qualified observation | None unless the human changes to escalation | Send the approved, environment-qualified observation | Reply verified; human records the case outcome |

Do not allow the model to choose a repository or recipient. During the demo,
publication is restricted to configured team-controlled accounts and recipients.
The GitHub issue includes the claim, expected/observed behavior, environment,
minimal request sequence, supporting observations and limits of inference.
Replies make no unsupported fix, root-cause or customer-production claim.

The engineering issue URL is unknown before creation. Approval previews a typed
issue-link placeholder; the server may substitute only the URL returned for that
same approved issue action. Any other reply change needs new approval. Create
and verify the issue before sending the escalation reply.

Persist each action intent and stable identifier before its network call. Record
provider IDs and verify the issue/commented content or sent-message identity
afterward. Repeated approvals and retries reconcile completed actions rather
than repeat them. Retry only unfinished actions whose approval is still valid.

A network timeout can follow a successful remote write. Reconcile with a stable
issue marker or sent-message identity before retrying. If the connector cannot
establish whether a send occurred, mark the action uncertain and require manual
reconciliation; do not claim unconditional exactly-once delivery or blindly
resend. This is a connector feasibility check, not a simulated success path.

If a new source revision arrives between issue creation and email sending, stop
remaining writes for renewed review. Preserve the created issue and its link;
do not silently create a replacement or delete external records. Partial and
uncertain states remain visible until resolved.

### Authentication, restart and deployment

Authenticate the support workspace and every action endpoint. Keep experiment
execution credentials separate from human publication authority. Reject direct,
stale, changed-content and cross-case publication requests at the server.

Persist before acknowledging transitions. After restart, reconcile publication
attempts and preserve completed provider IDs. An interrupted experiment can
restart with a fresh fixture and a new run identity; it cannot silently continue
as if the previous trace were complete. In-process background work is acceptable
only with durable state and these recovery semantics.

Deploy on Alternate Clouds, bind to the configured PORT, verify the health check,
and establish persistent storage before calling restart guarantees complete. If
durable SQLite storage is unavailable, resolve the storage dependency before
claiming restart recovery. Configure secrets, then explicitly Rebuild → Deploy;
do not assume a GitHub push updates the running deployment.

## Testing Decisions

The participant approved one primary seam: drive the entire case workflow
through the application's authenticated API, use the actual bounded lab service,
and provide controlled model/provider responses for repeatable adverse cases.
Use a small separate live fastn/Gmail/GitHub smoke run to prove real account
connections. There is no existing application or test suite to reuse.

Good tests assert observable evidence, authorized effects and recovery outcomes.
Avoid tests that mirror helper methods, private module structure or prompt
wording. Provider doubles exercise outcomes and timeouts; they do not constitute
proof of a live integration. Real model output gets a small live rehearsal,
while deterministic proposal fixtures keep the behavioral suite repeatable.

| Check | Required observable result |
| --- | --- |
| Intake replay and own replies | One case per thread; unchanged imports and application replies create no duplicates |
| Faulty service | Same retry identifier and payload yield two distinct recorded orders with an actual trace |
| Corrected service | Identical claim yields one recorded order; no automatic false-report verdict |
| Paraphrase and changed input | Experiment still follows the supported contract and observed state |
| Missing/unsupported conditions | Specific clarification, no invented customer evidence or irrelevant execution |
| Malformed AI output | Bounded correction or visible proposal error; no external write |
| Runner limits and isolation | Unknown targets/operations, cross-fixture reads and exhausted budgets fail explicitly |
| Prompt instructions in report | No authority to change targets, run code, approve or publish |
| Human editing and rejection | Edited expectation is reevaluated; rejected publication produces zero writes |
| Approval enforcement | Missing, expired, stale, changed-content and cross-case approval fail at the API boundary |
| Retry and concurrent submission | Stable action identities prevent duplicate completed issues/replies |
| Provider success then timeout | Reconciliation finds the write or exposes uncertainty before another attempt |
| Partial publication | Issue remains linked; reply is pending and only that action is eligible to resume |
| New evidence during publication | Completed write is preserved; remaining writes await fresh approval |
| Restart | Completed external actions survive; interrupted runs never masquerade as complete evidence |
| Live deployed smoke | Real intake, issue creation/read-back and controlled thread reply are visible through fastn on Alternate Clouds |

Completion of escalation requires verified issue and reply. Completion of a
clarification action requires a verified reply while the case remains awaiting
information. Provider errors and uncertain outcomes must remain visible in the
workspace. Record measured rehearsal timing; a sub-minute investigation is a
target, not a promised or established performance claim.

## Out of Scope

- Application implementation, dependency installation, account changes, live
  tests, email sending and deployment during the current documentation-only hold.
- Arbitrary repositories, generated code execution, browser reproduction,
  production services, payment processing and automatic code fixes.
- Race-condition reproduction, universal API onboarding, unsupported incident
  classes, multi-tenant enterprise administration and broad monitoring.
- Trello, a second engineering queue, dashboards, agent swarms, automatic
  severity scores and automatic dismissal of non-reproduced reports.
- Measured commercial adoption, guaranteed time savings, claims of global
  uniqueness, independent vulnerability validation or guaranteed judging outcomes.

## Further Notes

Implementation remains explicitly held despite approved scope and the intended
tracker label. Resume only on a direct participant instruction. The repository
currently contains tooling and documents, not application code or tests. Git
origin and GitHub Issues are configured for M-Abdullah07/Bugproof. Public issue
publication remains pending explicit approval following an automatic approval
review rejection; local creation is not claimed as remote issue publication.

Dependency gates for a future authorized build: fastn/Gmail/GitHub actions and
reconciliation capability; model key/provider; Alternate Clouds deployment and
durable storage; controlled source/reply accounts and owned repository; demo
reviewer authentication. Verify these before investing in UI. If an action is
unavailable, revise the design explicitly rather than replacing it with a fake.

The participant confirms organizer development permission. fastn requirements
remain unclear; conservatively retain fastn MCP centrally and mandatory Alternate
Clouds hosting. Target readiness is October 17, noon PKT, with an official
12:45 PM PKT code/deployment freeze and deployment running until closing.
Prepare the 2–3 minute video and exact five-minute presentation; finalist slides
are due before 4 PM. Participants write their own LinkedIn/Twitter content;
only grammar assistance is allowed. Include the handbook's remaining identity,
repository, deployment, Discord and submission evidence requirements.

Judging rationale: actual observations and recovery support reliability (25);
an actionable handoff and reporter reply support usefulness (20); human
interpretation and server-enforced publication support the theme (15); bounded
evidence-to-action execution is the proposed creative contribution (15); fastn
intake, execution and verified follow-through support automation depth (15);
one clear case view and a complete short demo support UX/presentation (10).
These are design intentions, not awarded scores or validated market impact.
