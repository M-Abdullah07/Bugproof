# BugProof MVP specification

Scope: approved by the participant. Testing boundary: approved.
Execution: **RESUMED October 17, 2026 by direct participant instruction (DEC-16).**
Local authenticated foundation and seven tests exist; account/deployment checks
are pending. Stop for material ambiguity; notify the user
when a new account is needed. The October 16 review below preserves historical
hold statements and decisions; they do not override this explicit resume.
Tracker: GitHub Issues, M-Abdullah07/Bugproof. Participant chose no spec issue. Future issue label if requested:
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

Use a unique durable action identity and a short SQLite transaction to claim
exclusive ownership before an external call. Commit the claim before making
network requests; never hold the SQLite write transaction across provider I/O.
Competing requests observe the existing attempt instead of issuing another call.
Timeouts and interrupted ownership require reconciliation before another send;
expiry of an ownership claim alone is not evidence that the provider did nothing.
Recheck approval and case revision at the claim boundary. This mechanism does
not claim to make the local transaction atomic with the external provider.

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

- Delegated agents without direct participant authorization and account creation
  on the participant's behalf without their instruction.
- Arbitrary repositories, generated code execution, browser reproduction,
  production services, payment processing and automatic code fixes.
- Race-condition reproduction, universal API onboarding, unsupported incident
  classes, multi-tenant enterprise administration and broad monitoring.
- Trello, a second engineering queue, dashboards, agent swarms, automatic
  severity scores and automatic dismissal of non-reproduced reports.
- Measured commercial adoption, guaranteed time savings, claims of global
  uniqueness, independent vulnerability validation or guaranteed judging outcomes.

## Further Notes

Implementation resumed under DEC-16; scope labels alone never authorize it.
The repository
currently contains tooling, documents and the local authenticated/storage foundation
with seven passing tests. The investigation/publication workflow and deployment
remain unimplemented/unverified. Git
origin and GitHub Issues are configured for M-Abdullah07/Bugproof. Public issue
publication was explicitly declined after an automatic approval review rejection.
Keep the specification in Git; create no issue unless the participant changes
that decision. No remote specification issue exists.

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

## Engineering review — October 16, 2026

Target and report destination: `docs/specs/bugproof.md`.
Context: `docs/designs/bugproof.md` and `GLOSSARY.md`.
Finding/question line citations below refer to the pre-review specification at
commit 544a08f; approved additions above shift current line numbers.
This appended review preserves the specification above. Pending proposals do
not amend its contract. Implementation remains HELD.

### Scope Challenge

Feature answers: retain the previously approved complete workflow; no cuts proposed.
Structure: D1, user selected "Original arrangement (Recommended) — retain the
five responsibility boundaries and isolated lab target; physical file layout
remains flexible. Small module overhead, clearer authority and recovery
ownership; implementation stays paused."
Accepted scope: five responsibility boundaries and isolated lab target, without
requiring separate deployments or a fixed file count.
Pending remedies at the D1 answer: none.
Result: scope accepted as-is. Mode: FULL_REVIEW.

Existing solutions: FastAPI supplies HTTP routing and server-rendered integration;
SQLite supplies transactions and uniqueness constraints. fastn is the approved
provider boundary. No first-party application, tests or deployment exists.
The local tools serve development only and do not implement the product.
Minimum work: the approved intake, actual experiment, human review, exact-action
approval, verified issue/reply and recovery path. Scheduled polling remains
optional; no additional queues, agent personas, analytics or automatic fixes.
Complexity: two logical services (application and lab target); five application
responsibilities. Proposed physical file/class counts are unspecified, not measured.
History: initial documentation/tooling commit 544a08f; no prior implementation
or reverts for the named specification/design paths. No TODOS.md exists.
Distribution: later deployment on Alternate Clouds and persistent storage remain
unverified gates. This review does not perform account or deployment changes.
Scope findings: no new scope changes needed. Dispositions: retain prior approvals.

Research before building: prefer standard SQLite transactions and constraints
[Layer 1], not a new broker. SQLite permits a single writer at a time; an external
HTTP call should not hold that write transaction open. Claim briefly, commit,
then call the provider and record/reconcile the result.
Sources: https://www.sqlite.org/isolation.html and
https://www.sqlite.org/conflict.html. FastAPI worker processes have separate
memory: https://fastapi.tiangolo.com/deployment/concepts/.
These sources support the mechanism, not a claim that BugProof implements it.

### Architecture review — in progress

F1 [P1] (confidence: 8/10), reviewer: primary agent.
`docs/specs/bugproof.md:223–226`: "Persist each action intent and stable identifier
before its network call" and "Repeated approvals and retries reconcile completed
actions rather than repeat them."
`docs/specs/bugproof.md:283`: "Retry and concurrent submission" requires stable
identities to prevent duplicate completed issues/replies.
Plan gap: durable identity and post-call reconciliation alone do not explain
who owns an action while its first provider call is still in flight. Two
requests can both observe no completed result and send concurrently. This is a
planning ambiguity, not an observed application bug. The previously approved
concurrency guarantee stands; only its coordination mechanism is being selected.

## Decision ledger

### R1: Publication ownership mechanism

Finding: F1, P1, confidence 8/10; primary agent; specification lines 223–226, 283.
Plan baseline: stable action identities, concurrency-safe publication and
restart reconciliation are approved in the assembled MVP and testing boundary.
No action-ownership mechanism has been selected. Implementation is paused.
Runtime evidence: unknown; no application or provider calls exist.

| Choice | Current | A | B |
| --- | --- | --- | --- |
| R1 mechanism | Unspecified | Durable SQLite claim per action | Leave mechanism to implementation, require proof before publishing |
| Duplicate prevention | Approved | Preserved | Preserved |
| Unknown send result | Manual reconciliation, no blind resend | Preserved | Preserved |
| Recovery | Persist and reconcile | Preserved | Preserved |
| Feature boundaries | D1 original arrangement | Preserved | Preserved |
| Execution permission | HELD | HELD | HELD |

Question D2:
D2 — Prevent two simultaneous sends.
Project/branch/task: BugProof, main, architecture review of docs/specs/bugproof.md.
ELI10: Two clicks can start the same email before either request records success.
The spec already requires preventing duplicates, but has not chosen who owns a
send while it is running. This selects that mechanism, not a new feature.
Stakes if we pick wrong: duplicate customer replies or engineering issues despite
valid human approval (spec lines 223–226, 283).
Recommendation: A because SQLite already provides the durable coordination we
need without another service. A short transaction claims the action; the provider
call happens after commit. Restart or timeout reconciles the existing attempt
before any new claim can send again.
Note: options differ in kind, not coverage — no completeness score.
Net: specify the small coordination mechanism now, or leave it open while
retaining the same mandatory concurrency and recovery proof. Neither resumes implementation.
Header: Send ownership
Options:
A) SQLite claim (Recommended)
✅ Uses the existing database without adding a queue service.
✅ Gives simultaneous requests one durable action owner.
❌ Adds transactional state handling and concurrency tests.
Effort: estimated 1–2 human engineering hours or 20–40 agent minutes once implementation resumes; not a delivery promise.
B) Decide during build
✅ Keeps the approved duplicate-prevention contract intact.
✅ Allows the builder to choose an equally proven mechanism.
❌ Leaves a critical architecture detail and its effort unresolved.
Effort: no design change now; implementation must still prove exclusive ownership, timeout reconciliation and restart recovery before live publishing.

State: approved
Actual answer: D2 user reply, "recommended option but keep in mind we need to
make sure we optimize for the hackathon and winning it and winning it
effectively/comprehensively."
Accepted scope: SQLite durable action ownership, short claim transaction,
provider call after commit, and reconciliation before retry after timeout or
restart. Preserve every existing feature and the implementation hold. Optimize
execution for a complete, demonstrable hackathon workflow; no additional scope.
History: none.

Approval readiness: PASS. D1 retains the approved structure; D2 approves R1.
No other new remedy or product policy is accepted by this review.

## Engineering review findings and execution plan

### Architecture review — complete

One issue: F1, publication ownership ambiguity. Disposition: accepted under D2;
the publication contract now specifies a durable exclusive claim and
reconciliation. Claim expiry never authorizes a blind resend. This is planned
behavior; implementation and verification remain outstanding.

Data/authority boundaries survive review: the LLM proposes; the runner validates
and executes within the registered contract; the human chooses and approves;
only the publisher can access configured external destinations. Source excerpts
and captured API observations remain separate. Provider text cannot grant authority.
SQLite transactions coordinate local state, not atomic delivery across providers.
Deployment durability, credentials and connector capabilities remain build gates.

### Code quality review — complete

No additional issues found in the proposed module organization. There is no
application code to audit, and generated/third-party skills are not first-party
callers. No shared helper extraction is justified. Use five responsibility
boundaries from D1 and keep physical files flexible. Explicitly represent action
states and outcomes rather than scattering boolean success flags. That is an
implementation expression of the existing visible partial/uncertain-state contract.
Dispositions: retain approved boundaries; no new abstraction or remedy proposed.

### Test review — complete

No application test framework or test suite exists. The API-level boundary,
actual lab service, controlled provider responses and separate live smoke are
already approved; this review installs nothing and chooses no new framework.
All paths below are PLANNED, currently untested. No coverage percentage is claimed.

```text
PROPOSED EXECUTION                                  OPERATOR FLOW / PROOF
Authenticated Check inbox                          [GAP -> E2E] empty/inbox/recheck
  -> fastn read -> source validation + identity
     | failure -> visible intake error, no case loss
     | same inbound snapshot -> reuse case
     | new inbound -> revision++, invalidate approval
     ` own outbound -> ignore
  -> grounded structured interpretation             [GAP -> EVAL] valid/paraphrase
     | malformed -> one correction -> visible error
     | missing -> clarification review              [GAP -> E2E] missing facts
     | unsupported -> unsupported review
     ` supported -> validate target/fixture/limits
        | rejected -> explicit runner error
        ` actual HTTP lab -> immutable evidence     [GAP -> E2E] faulty/corrected
           | timeout/truncation -> qualified error
           ` complete -> assertion + observed build
  -> human review / editable expectation             [GAP -> E2E] edit/reject
     | expectation edit -> reevaluate + invalidate
     | plan/target edit -> fresh run + invalidate
     ` disposition -> exact previews -> approval
        | invalid/stale/expired/cross-case -> no write
        ` SQLite claim -> one action owner          [GAP -> E2E] simultaneous clicks
           | already completed -> reconcile/reuse
           | in flight/uncertain -> no second send
           ` escalate -> issue -> read-back -> reply
              | issue fails -> visible failure, no reply
              | reply fails -> keep issue, reply pending
              | source changes -> stop remaining writes
              | timeout -> reconcile or manual uncertainty
              ` verified effects -> complete        [GAP -> LIVE] actual accounts
Clarify/qualified disposition -> approved reply only
Restart -> durable attempts -> reconcile; interrupted run gets new fixture
```

The expanded flow covers all 16 acceptance rows in Testing Decisions. Their
implementation is absent; these are required proofs, not green tests. Extend the
existing concurrency row with two requests reaching the ownership boundary
together, plus a process stop after claim/provider success but before completion
is saved. Assert one provider call, or uncertainty requiring reconciliation;
never treat elapsed claim time as permission to send again. These assertions
prove the already approved duplicate/restart contract and D2 mechanism.

Proposed test organization, not fixed public API or required file layout:
`tests/test_case_workflow.py` for intake, proposal, lab and review;
`tests/test_publication.py` for authorization, concurrency, timeout and restart;
`tests/test_live_smoke.py` for separately enabled real connections. No obsolete
tests exist. The QA artifact carries observable assertions and value cards.
Browser rehearsal covers the same operator flow, including refresh/navigation
during a run, simultaneous submissions, expired session and visible recovery.
No separate browser automation suite is imposed by this review.
Dispositions: required proof of prior approved contracts plus D2; no new test scope.

### Performance review — complete

No additional blocking issue found for the bounded demonstration workload.
The existing eight-request, 30-second, body/capture limits bound experiments;
actual LLM/provider latency and input volumes are unknown. Record measured
end-to-end rehearsal timing; the runner budget is not a whole-workflow SLA.
Avoid network I/O inside SQLite write transactions under D2. Case/action
identity uniqueness is required by approved idempotence; do not add a cache or
broker before measuring a demonstrated bottleneck. Inbox pagination and provider
limits must follow the real connector capability, presently unverified.
Dispositions: no new performance guarantee or numerical limit proposed.

### Premises and reality checks

| Premise | Receipt | Verdict |
| --- | --- | --- |
| Scope and meaningful human control approved | D1, D2 and specification Approval and publication contract | Confirmed participant decisions |
| No application implemented | Git tree at 544a08f, tooling/docs only | Verified locally |
| fastn can perform required account actions and reconciliation | specification:105–108, 228–232 at 544a08f | Unverified |
| Alternate Clouds provides usable durable storage | specification:251–255 at 544a08f | Unverified |
| Model credentials and controlled Gmail accounts are ready | specification dependency gates, Further Notes | Unverified |
| Specific buyer demand/time savings | specification:21–22 at 544a08f | Unverified |

unverified=4. These are explicit future gates/limits, not assumed successes.

REALITY: premise-table pass Four unverified premises are explicit docs/specs/bugproof.md:318
REALITY: already-done pass Initial tree contains documents/tooling, no repeated application implementation 544a08f
REALITY: surface-check finding Future fastn and hosting surfaces are not verified; no app routes exist docs/specs/bugproof.md:105
REALITY: binding-decisions pass D1 and D2 preserve the execution hold and authority boundary docs/specs/bugproof.md:407
REALITY: numbers pass Runner and approval numbers are participant-approved design defaults, not measured performance docs/specs/bugproof.md:160
REALITY: deferred-asks pass No approved product feature cut; participant chose no public specification issue docs/specs/bugproof.md:318
REALITY: pr-count pass No split proposed; one MVP and no implementation PR created by this review docs/specs/bugproof.md:350
REALITY: prior-art pass Adopt standard SQLite transactions and constraints; no patched runtime dependency proposed docs/specs/bugproof.md:385
REALITY: transaction-semantics pass D2 claims briefly; no provider I/O while holding a write transaction docs/specs/bugproof.md:228
REALITY: contract-assumptions finding fastn read/send/reconcile and persistent hosting remain unverified build gates docs/specs/bugproof.md:105
REALITY: dependency-fallback pass With missing integration or storage capability, stop and revise; never substitute simulated completion docs/specs/bugproof.md:318
REALITY: obligation-tiers pass Must complete approved workflow and evidence; polling and analytics remain outside critical build docs/specs/bugproof.md:110

### What already exists

Reuse the specification, glossary, approved design, local tools and GitHub project
configuration. There is no existing application, lab service, first-party test
suite or deployment. Reuse FastAPI, SQLite and fastn; do not invent substitutes.
The currently configured project issue tracker is separate from the future
controlled repository where BugProof publishes demonstration escalations.

### NOT in scope

Keep the existing Out of Scope list. No automatic fixes, production access,
payments, generic browser runner, extra queue or dashboard. Scheduled polling
is optional and may not delay the complete workflow. Commercial validation is
not established by a synthetic demonstration. Additional review skills and
independent agents are not authorized by this invocation.

### Failure modes and proof

| Path | Realistic failure | Required visible behavior and proof |
| --- | --- | --- |
| Intake | Credential failure or duplicate import | Visible error or one case; intake acceptance row |
| Interpretation | Invented facts or malformed output | Reject ungrounded plan, bounded correction; proposal acceptance rows |
| Execution | Wrong fixture, timeout or oversized trace | Explicit error, no unsupported assertion; isolation/limits rows |
| Review | Stale tab, altered payload or changed source | Zero unauthorized effects; approval and editing rows |
| GitHub | Write succeeds before timeout | Reconcile marker/ID or show uncertainty; no duplicate issue |
| Gmail | Issue succeeds, reply fails | Keep issue URL; resume only eligible reply; partial publication row |
| Concurrency | Two approved submits race | One durable owner/provider attempt; D2 and concurrency row |
| Restart | Stop between remote write and local completion | Reconcile existing attempt; no blind resend; restart row |
| Hosting | Lost SQLite volume | Durability gate fails visibly; no recovery claim before verification |

Critical gaps with both no handling and no planned test: zero. All proof is
future work; this is not a reliability certification.

### Hackathon execution order — only after explicit resume

| Step | Modules touched | Depends on | Review/acceptance purpose |
| --- | --- | --- | --- |
| 1. Verify dependency surfaces and deploy skeleton | fastn adapter, configuration, persistence, hosting | Explicit resume | Existing feasibility gates; fail early on blocked credentials/storage |
| 2. Prove HTTP evidence | runner/lab, persistence | Step 1 | Faulty build yields two orders; corrected build one |
| 3. Close one full escalation | case workflow, AI proposals, review, publisher | Steps 1–2 | Gmail report to approved issue and verified thread reply |
| 4. Prove judgment and recovery | same workflow and publisher | Step 3 | Incomplete report, expectation correction, no-send rejection, partial failure, D2 race/restart |
| 5. Rehearse and prepare submission | workspace, deployed integration, participant artifacts | Step 4 | Measured short demo, login, evidence, video and PDF before freeze |

Sequential implementation, no parallelization opportunity for autonomous agents
under the user's no-delegation instruction. No worktrees or agents launched.
Two human teammates may divide independent lab and provider-verification work
after agreeing shared contracts; this review does not assign them work.
The authority/state boundary is shared: sequence changes there to avoid conflict.
One primary automated lane; other parallel lanes are not scheduled.

Demo spine: one inbox report -> actual duplicate-order trace -> human adjusts or
approves disposition -> issue + reply read-back. Briefly show corrected-version
replay and missing-information clarification. Show one recoverable partial
failure in rehearsal/video if time permits; the required adverse-case tests remain.
Preserve time for Alternate Clouds rebuilds, the 2–3 minute video and submission
PDF. Claim measured behavior and limits, not guaranteed judging scores or adoption.

## Implementation Tasks

All execution remains HELD. This list contains review-derived work only; the
execution table above orders the already approved MVP rather than expanding it.

- [ ] T1 (P1) — publisher/persistence — Implement D2 exclusive action claims.
  - Surfaced by: architecture F1, missing ownership during in-flight publication.
  - Proposed paths: publication/persistence modules; `tests/test_publication.py`.
  - Verify: concurrent approvals, success-before-timeout, interrupted claim and
    post-provider restart produce one write or explicit uncertainty, never blind resend.
  - Effort: estimated 1–2 human engineering hours or 20–40 agent minutes, excluding
    credentials/provider delays; same uncertain estimate as D2, not measured.
  - Depends on: verified connector reconciliation and durable storage, plus resume.

No new tasks from Code Quality, Test or Performance beyond required proof of T1
and the existing specification. No new TODO proposals; TODOS.md is not created.

### Outside Voice

Unavailable: AGENTS.md explicitly prohibits subagents without direct user
authorization. No independent reviewer or external review CLI was launched.
This review has one primary reviewer and claims no cross-model confirmation.
The missing outside coverage is non-blocking under the skill's unavailable route.

### Suppressed findings

Input volume, connector quotas and provider latency remain unmeasured. They are
rehearsal/capability unknowns; there is insufficient evidence for an additional
numeric resource policy or performance defect. No invented benchmark is reported.

### Completion summary

- Scope Challenge: scope accepted as-is (D1), FULL_REVIEW.
- Reality rows: `PLAN_REALITY: phase=eng rows=12/12 missing=none verdict=complete`;
  4 unverified premises, documented as capability/market gates rather than facts.
- Architecture: 1 issue, F1 accepted via D2; implementation proof outstanding.
- Code Quality: 0 additional issues.
- Tests: proposed flow diagram and 16 acceptance rows mapped; all currently unimplemented.
  One ownership proof elaboration belongs to F1; no separate uncovered approved contract found.
- Performance: 0 additional demonstrated issues; actual latency remains unknown.
- NOT in scope, existing solutions and failure modes: written.
- TODOS.md: 0 new proposals. Critical silent/unhandled/unplanned-test gaps: 0.
- Unresolved engineering decisions: 0. Feasibility gates are unverified work, not approvals.
- Outside voice: unavailable, no delegation authorization; no independent coverage.
- Parallelization: one sequential automated lane, no agents launched.
- Lake Score: N/A; D1/D2 compare arrangements/mechanisms, not coverage cuts.
- Navigation: existing implementation hold remains binding; no new skill or build launched.
- QA artifact saved and read back at
  `.tools/gstack-state/projects/M-Abdullah07-Bugproof/1122admin1-main-eng-review-test-plan-20261016-154016.md`.
  It is local tool state and excluded from Git; the specification's acceptance
  table and this review preserve the tracked test requirements.
- Task JSONL aggregation: NOT PERSISTED because jq is unavailable. T1 above is
  the complete task output; install/configure aggregation separately if needed.
  No application dependency was installed to satisfy review tooling.
- Dashboard: Eng ISSUES OPEN (1 accepted task, no unresolved decision); outside
  unavailable; CEO, Design and DX not run. This is a plan review, not runtime clearance.

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
| --- | --- | --- | --- | --- | --- |
| CEO Review | Not run here | Product strategy | 0 | Not evaluated | Earlier design is context, not a logged CEO clearance |
| Outside Review | No authorized delegation | Independent opinion | 0 | Unavailable | No outside coverage |
| Eng Review | /plan-eng-review | Architecture and tests | 1 | ISSUES OPEN | 1 accepted architecture issue; proof outstanding |
| Design Review | Not run here | UI/UX | 0 | Not evaluated | No application/UI exists |
| DX Review | Not run here | Developer experience | 0 | Not evaluated | No application exists |

**OUTSIDE COVERAGE:** unavailable; one primary reviewer only.
**VERDICT:** plan review complete with one accepted implementation task; eng review
required before claiming runtime clearance. Implementation remains HELD and live
connector/storage feasibility is unverified. Review log persistence is verified separately.
NO UNRESOLVED DECISIONS
