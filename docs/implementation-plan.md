# BugProof implementation plan

Prepared October 17, 2026, Asia/Karachi. **Implementation resumed by the participant
on October 17 (DEC-16).** Local M1 foundation implemented/tested; first deployment
and M0/M2 account checks remain unfinished. Stop for material ambiguity and account needs.
This plan does not authorize delegated agents or account creation on the user's behalf.

Behavior comes from the [specification](specs/bugproof.md); rationale from
[Decisions.md](../Decisions.md); ownership from [Architecture.md](../Architecture.md).
Track actual proof in [ACCEPTANCE.md](../ACCEPTANCE.md), not in optimistic checkboxes.
The [judge scorecard](judge_scorecard.md) defines the competition priorities.

## 1. What we are building, in ordinary language

A support engineer receives: "My order request failed, so I retried and got two
orders." BugProof turns that account into a controlled experiment, sends real
HTTP requests to a labeled test API, and records the resulting order IDs. The
human compares the claim, expectation and observations and decides the next step.
Only after reviewing exact outbound content can they authorize an engineering
issue and a reply in the original email thread.

The faulty API actually stores two orders. The corrected API stores one. An
incomplete report asks for information rather than inventing evidence. These
three different outcomes must follow behavior and available facts, not canned
responses selected by report wording.

```text
Email -> case -> grounded AI plan -> bounded HTTP experiment -> evidence
                                                              |
                                                       HUMAN decision
                                                              |
                         verified GitHub issue <- approval -> Gmail reply
                                   |                            |
                                   +--- durable action records -+
```

For escalation, create/read back the issue before sending its link in the reply.
For clarification or a qualified observation, send only the approved reply.
We finish a support investigation/handoff; we do not fix code or verify payments.

## 2. How an agent follows this plan

Work sequentially. The word "agent" describes a future executor, not permission
to launch additional agents. The participant may have two human teammates work
on disjoint pieces after they agree interfaces; no such assignment is made here.

For each milestone:

1. Read AGENTS.md, this milestone, its dependencies, and affected spec sections.
   Load only the relevant source/tests; exclude tool/vendor trees from routine searches.
2. Confirm implementation has actually resumed and the submission freeze has not
   passed. Inspect existing work before creating anything; resume rather than rebuild.
3. Write or extend the smallest meaningful test for the milestone's observable
   behavior, implement the vertical slice, and run the targeted checks.
4. Save redacted run evidence, update affected acceptance IDs and actual commands
   in README, and record unexpected constraints. Plans/fixtures alone are not passes.
5. Commit a coherent verified slice under the existing Git authorization. Rebuild
   and deploy explicitly when needed; Git push alone is not deployment.
6. Hand off: commit, changed files, commands/results, evidence IDs, known blockers,
   and the next milestone. Stop only the dependent branch on a real blocker.

Use statuses NOT_STARTED / IN_PROGRESS / BLOCKED / DONE in the progress table.
DONE requires the stated exit check. Record partial progress without promoting
unrun acceptance tests. A resumed agent reads this table and the evidence before acting.

## 3. Milestones and deadline budget

The noon target and 12:45 PM PKT freeze are **today, October 17**. A clock check
during planning was 06:37 PKT, leaving about six hours to the official cutoff.
Recheck actual time before execution. The budgets below are prioritization
timeboxes, not validated duration estimates or a promise of completion.

| ID | Milestone | Depends on | Timebox | Status / evidence |
| --- | --- | --- | ---: | --- |
| M0 | Resume and preflight | Direct participant resume | 5 min | IN_PROGRESS / account access clarification pending |
| M1 | Runnable authenticated foundation and first deployment | M0 | 25 min | IN_PROGRESS / [local foundation](evidence/20261017-foundation.md); deployment pending |
| M2 | Prove integrations and persistent storage | M1 | 35 min | NOT_STARTED / — |
| M3 | Actual faulty/corrected lab and bounded runner | M2 | 40 min | NOT_STARTED / — |
| M4 | Gmail intake and grounded AI investigation | M3 | 40 min | NOT_STARTED / — |
| M5 | Human review and exact-action approval | M4 | 30 min | NOT_STARTED / — |
| M6 | Close the real issue + reply workflow | M5 | 45 min | NOT_STARTED / — |
| M7 | Prove concurrency, partial failure and restart | M6 | 30 min | NOT_STARTED / — |
| M8 | Deployed acceptance and operator rehearsal | M7 | 20 min | NOT_STARTED / — |
| M9 | Video, PDF, access checks and freeze record | M8 for final proof; prepare artifact structure earlier | 40 min | NOT_STARTED / — |

Total execution budget: 310 minutes, excluding this planning, external access
delays and unexpected defects. It is tight. Prepare submission identity fields,
participant-written social content and slide structure while infrastructure is
building if the humans are available. Record only actual project results later.

If M2 exceeds its budget, stop investing in dependent features, name the missing
capability and obtain a specific scope decision. If later milestones slip, cut
polish, polling and extra scenarios outside the approved three; preserve the
approved authority/recovery guarantees or explicitly revise scope with the user.
Never claim a test passed to fit a deadline. Reserve the official cutoff margin
for submission problems, not a planned last-minute deployment.

## 4. Shared contracts to establish during M1

These are proposed implementation names, not existing APIs. Keep the approved
five responsibility boundaries; avoid creating empty abstraction layers in advance.

### Source and records

| Record | Minimum identity/content | Owner |
| --- | --- | --- |
| Case | Case ID, configured mailbox/thread, current source revision, visible workflow state | workflow/storage |
| Source revision | Eligible inbound message IDs, immutable text/excerpts, provenance, revision | workflow/storage |
| Interpretation | Claim, steps, expected behavior, missing facts, support status, resolving source excerpts | proposals |
| Experiment plan | Registered target, fixture, permitted operations/inputs, expected assertion, source/plan revision | proposals -> experiments |
| Run/evidence | Run ID, actual sequence/responses/orders, budgets, timestamps, target build, completion/outcome | experiments/storage |
| Preview/approval | Disposition, configured destinations, exact payloads, typed issue-link placeholder, source/expectation/evidence fingerprints, reviewer/time/expiry | review/storage |
| Publication action | Stable action ID, case/intent, payload identity, claim ownership, attempt state, provider identity/result | publication/storage |

Use strict structured schemas, immutable snapshots and explicit outcome enums.
The model cannot supply authorization fields or provider credentials. SQLite
owns uniqueness and atomic transitions; model output and browser forms do not.
Choose table organization for these records without requiring one table/class
for every noun. Version schema initialization so restarts preserve existing data.

Keep investigation outcome separate from publication state. For example,
"reproduced discrepancy" can coexist with "reply pending"; "not reproduced"
never means the report is false. Publication needs persisted intent, in-flight,
verified, failed-before-effect, or uncertain states with enough detail to recover.

### Narrow interfaces

- Workflow: import eligible source -> case/revision; investigate case -> reviewable
  result or explicit error. Reimports preserve identity; revisions invalidate stale work.
- Model adapter: source + registered contract -> validated structured proposal.
  Configured model/provider is selected from available credentials during M2.
- Runner: validated plan -> immutable actual observations and assertion outcome.
- Review: current case/evidence + human edits -> preview; exact current preview -> approval.
- Publisher: approved case/action -> verified external identity, visible failure,
  or uncertainty. It never fabricates success or accepts a client approval flag.
- fastn adapter: list/read eligible thread, create/read issue, send/read thread reply,
  find/reconcile effects where supported. Actual tool names/arguments must come
  from the connected fastn tool inventory, never from guessed API names.

### Proposed HTTP surface

| Route group | Responsibility | Authority |
| --- | --- | --- |
| `/healthz` | Nonsecret health/build identity | Minimal public response |
| `/login`, `/logout` | Single demo operator session | Server-configured identity |
| `/cases`, `/cases/{id}` | List and review case | Authenticated operator |
| `POST /intake/check` | Explicit eligible inbox import | Authenticated operator |
| Case investigate / expectation / preview / approval / publish / reconcile actions | One explicit transition per action, with revision checks | Authenticated operator; exact approval required for writes |
| Protected lab fixture setup/reset; fixture-scoped create/inspect order routes | Actual synthetic API state | Internal/test authority, never arbitrary public reset |

Pick exact case/lab action URLs during the first slice and let OpenAPI/tests/README
be the executable lookup thereafter. Mutations must not be GET requests. Use a
small single-operator login with established auth primitives, secure session
handling and CSRF protection where cookie-authenticated forms require it.

## 5. Build cards

### M0 — Resume and preflight

**You should understand:** this checks that we are allowed and able to begin.

- Confirm direct resume, current time, branch/remote and existing work. Retain
  DEC-14: do not publish the specification as a GitHub issue.
- Read the behavior sections of the spec, architecture map and acceptance rows.
- Check Python, project-local tool readiness, Alternate Clouds account, model
  access, fastn connection and controlled Gmail/GitHub ownership. Do not print secrets.
- Local observation during planning: default `git status` failed while inspecting
  the gstack submodule; `git status --short --ignore-submodules=all` could inspect
  the parent. Diagnose that tooling separately if needed; application work must
  not depend on upgrading gstack or repairing optional browser helpers.

**Exit:** record actual available access and any blocker; no assumptions become
passes. Application execution remains blocked until resume, even if tools exist.

### M1 — Small runnable foundation, auth and early hosting

**You should see:** a login, empty case list and reachable health endpoint on
Alternate Clouds, not a mock screenshot or a locally running app only.

**Touch:** `pyproject.toml`, packaging/lock, app entry/config/storage/web,
minimal templates, `.env.example`, `.gitignore`, deployment/startup configuration,
`tests/conftest.py`, root README. Create only files needed for this slice.

1. Use the supported Python version available locally and on the host; resolve
   compatible FastAPI/Uvicorn, schema, HTTPX, template and test dependencies.
   Prefer stdlib SQLite over introducing another service/ORM for this MVP.
2. Register pytest, including a `live` marker. Defaults must not perform external
   writes; live execution needs explicit opt-in and configured owned destinations.
3. Implement configuration validation, authenticated mutation boundaries, storage
   initialization and a nonsecret build/version health response. Missing required
   credentials must produce a useful configuration error, not a fabricated success.
4. Establish a single app worker initially. If operations run in-process, persist
   their state before scheduling, track them, and recover interrupted work; do not
   mistake a background task object for a durable queue.
5. Bind the host's PORT; use the actual Alternate Clouds startup/deploy interface.
   Configure environment, then explicit Rebuild -> Deploy. Check health and login.

**Verify:** unauthenticated mutations fail; authenticated empty page works;
store/read a harmless synthetic record across local restart. Record the first
deployed build identity. This is only a partial prerequisite for A10/A15–A17.

### M2 — Dependency proof before dependent investment

**You should see:** the real connections work, and a test record survives a real
host restart. This prevents spending hours polishing an ineligible/disconnected app.

**Touch:** `integrations/fastn.py`, model adapter/config, isolated smoke checks,
sanitized capability evidence. Use temporary owned-account test artifacts, not
the project specification issue prohibited by DEC-14.

1. Inspect fastn's actual tools and connected accounts. Map exact inputs/outputs
   into the narrow adapter; record tool names and provider identity/error semantics.
2. Read a labeled synthetic Gmail report. Establish original thread/message IDs
   and a reliable way to distinguish imported inbound messages from our sends.
3. Verify controlled GitHub create/read-back and original-thread Gmail send/read-back
   using exact reviewed smoke content under existing authorization. Store resulting IDs.
4. Check how ambiguous GitHub/Gmail effects can be found again. If Gmail cannot
   establish whether a send occurred, explicitly support manual uncertainty;
   do not require or invent provider idempotency that the connector lacks.
   Normal successful sends still require verifiable identity/read-back. Manual
   uncertainty is recovery for ambiguous results, not a waiver of successful-send proof.
5. Test the model provider's structured response once and verify the host's durable
   SQLite mount with an actual restart. Record secret names only, never values.

**Exit:** current capability evidence for every dependent action; safe uncertainty
   handling where supported read-back is limited; durable storage verified. Otherwise
mark the relevant gate BLOCKED and stop dependent work for an explicit revision.
These smoke checks alone do not pass full-workflow A16.

### M3 — Make the bug observable, then constrain the runner

**You should see:** the same supported retry experiment creates two orders on the
faulty target and one on the corrected target, with raw observations available.

**Touch:** `src/bugproof_lab/`, `experiments.py`, run/evidence storage,
synthetic fixtures and case-workflow tests. No AI is required to prove the lab itself.

1. Implement actual fixture-scoped order storage. On the first request, commit
   an order and return a simulated failure. On retry with the same identifier
   and payload, faulty behavior creates another; corrected behavior returns the
   original. The HTTP requests and stored records, not a report label, determine it.
2. Protect fixture setup/reset and isolate each run. Expose observed target build
   identity. Never infer the verdict directly from the target's build label.
3. Validate registered target, allowed operations, fixture ownership and strict
   parameters before I/O. Model-provided URLs/headers/code never become requests;
   redirects must not escape the registered target boundary.
4. Enforce the spec's request/runtime/body/capture limits. Capture sanitized
   request/response/order facts. Separate completed non-reproduction from timeout,
   truncated evidence, invalid plan and other execution errors.
5. Exercise the lab over real loopback HTTP in deterministic tests, even when
   the main app is tested through an in-process authenticated ASGI client.
   Start/stop that server reliably and explicitly initialize app lifespan state.

**Exit:** evidence for A02, A03 and A07. The runner can independently produce a
truthful evidence bundle; a stored canned answer cannot satisfy this milestone.

### M4 — Real intake and grounded AI investigation

**You should see:** Check inbox imports the real report once, then prepares and
runs a justified experiment; incomplete information produces a clarification draft.

**Touch:** `workflow.py`, `proposals.py`, source/plan persistence, actual adapter,
controlled model/provider fixtures and case-workflow tests.

1. Import configured labeled threads; persist immutable inbound snapshots and IDs.
   Reimport unchanged messages without new cases/runs; exclude app-sent replies.
   New eligible inbound messages increase revision and invalidate stale approvals.
2. Give the model only source data and the supported contract. Require source
   excerpts resolving to the snapshot, claim/expectation, missing information,
   support status and a strict bounded operation plan when justified.
3. Validate grounding and schema server-side. Permit one correction attempt,
   then a visible proposal error. Reject unsupported payment claims and instructions
   that attempt to change tools, recipients, approval or target authority.
4. For justified plans, call the actual runner automatically and persist the
   result before reporting evidence-ready. For missing information, bypass execution.
   A provider/runner failure remains a visible error, not a negative bug verdict.

**Exit:** A01, A04–A06 and A08 evidence; one real intake can reach review.
Run a small live model rehearsal as well as controlled fixtures; do not conflate them.

### M5 — Human judgment with a real authorization boundary

**You should see:** one case page separating source, claim, expectation and actual
observation. You can change the expectation or choose clarification instead of
escalation, preview exact actions, and reject them without sending anything.

**Touch:** `review.py`, authenticated web actions, case template and approval tests.

1. Show source/provenance, concise evidence, expandable trace, result limitations,
   disposition controls and separate issue/reply previews. Keep primary controls
   usable without JSON knowledge; label laboratory/synthetic data.
2. Reevaluating expectation uses complete stored observations. Changes to the
   plan, fixture or target require a new run. Preserve old evidence and invalidate
   affected approval/preview versions instead of overwriting history.
3. Build exact previews from server-configured destinations and human-edited
   content. The issue-link placeholder is typed and bound to the same issue action.
4. Store reviewer, time, the spec's initial 15-minute expiry and all relevant
   fingerprints. Rejection creates no publication intent with executable authority.
   Stale or tampered submissions fail server validation.

**Exit:** A09–A10 and initial manual A17 proof. A human choice changes effects;
an Approve button that always produces the same result does not satisfy the theme.

### M6 — Finish the handoff and reply

**You should see:** approving escalation creates a real GitHub issue, verifies
it, sends its verified link in the original Gmail thread and shows both identities.

**Touch:** `publication.py`, atomic storage operations, fastn adapter and publication tests.

1. Persist a stable action identity and approved intent. In a short transaction,
   recheck current authorization and atomically claim that intent. A competing
   request sees the existing owner/result instead of starting another provider call.
2. Commit before network I/O. Create/read back the issue; persist its identity and
   exact observed result. Substitute only this verified issue's URL into the
   approved typed placeholder. Any other edit requires renewed approval.
3. Recheck authorization/source revision before each remaining write. Send/read
   back the original-thread reply, then mark the action verified. Clarification
   and qualified observations create no issue unless disposition is escalation.
4. Match completion to the disposition: both verified effects for escalation;
   verified reply plus awaiting-information state for clarification. Keep qualified
   observation distinct from dismissing the report.

**Exit:** one real full escalation with observed issue and reply, plus A11 behavior
in controlled tests. Record provisional live evidence; full A16 awaits final deployed rehearsal.

### M7 — Make failure recoverable rather than impressive-looking

**You should see:** if sending the email fails after the issue exists, the issue
stays linked. A safe retry sends only the remaining eligible reply.

**Touch:** publisher/recovery transitions and `tests/test_publication.py`.

1. Hold the first attempt at the provider boundary and submit again concurrently.
   Assert one owner and no duplicate call; sequential replay alone is insufficient.
2. Inject provider success followed by lost response. Reconcile using the stable
   marker/message identity, or leave uncertain for explicit manual reconciliation.
   Disable blind retries of non-idempotent effects, including library-level retries.
3. Fail email after issue creation. Preserve completed action IDs; require still-valid
   or renewed approval for unfinished work. Renewing approval must not create a
   replacement issue just because its fingerprint/approval ID changed.
4. Import new source evidence between issue and reply; preserve issue and stop
   remaining stale work. If changed content needs updating an already published
   issue, stop for an explicit approved action rather than silently editing it.
5. Restart after claim and after external success/before local completion. On
   startup inspect durable state, reconcile before another send, and never infer
   non-delivery from expired claim ownership. Interrupted experiments get a new
   run/fixture; incomplete traces cannot become completed evidence.

**Exit:** A11–A15 evidence, including actual process restart. Changes received
after a provider request is already in flight cannot retroactively unsend it;
record the actual sequence and bind claims to imported snapshots, not imaginary
continuous awareness of the mailbox.

### M8 — Final deployed proof and operator rehearsal

**You should see:** a fresh browser session can log in and complete the actual
workflow on Alternate Clouds; the same claim on corrected behavior and an
incomplete report take visibly different, honest paths.

1. Rebuild/deploy the verified commit; compare observed deployment build and health.
   Verify durable records survive a host restart and no completed effects repeat.
2. Run the deterministic suite, then the separately opted-in live deployed smoke
   with actual fastn/model/accounts. The live smoke must traverse the deployed app,
   not merely exercise local code using real provider credentials.
3. Rehearse faulty escalation, corrected qualified response and incomplete
   clarification. Check expectation editing/rejection, slow/error states, refresh,
   expired auth, partial result recovery and exact source/trace inspectability.
4. Update A01–A17 honestly; split partial passes. Measure actual elapsed timing,
   capture sanitized evidence and check every external link as a judge would.

**Exit:** current complete acceptance evidence, current deployment/build identity,
and known limitations. Failing proof remains FAIL/BLOCKED, never narrated as passed.

### M9 — Submission, explanation and freeze

**You should see:** a judge can understand the problem and human decision quickly,
open the app/repository/video, and independently inspect the demonstrated result.

- Use the scorecard's artifact checklist: identities/contact, pitch/problem/user,
  human decision/stack, live URL, accessible repo, demo login, 2–3 minute video,
  Discord/deployment screenshots, credits and participant-written social links.
- Record the support rescue, actual trace and human choice; finish on verified
  issue/reply. Briefly replay corrected/missing-information cases. No production,
  payment, universal uniqueness or guaranteed time-saving claim.
- Prepare the exact five-minute finalist narrative and slide PDF; if selected,
  submit slides before 4 PM. Confirm submission destination and referenced handoff doc.
- Before 12:45 PM PKT, record source commit, observed deployed build, health/access,
  evidence revision and artifact URLs; submit and verify access. After cutoff,
  make no code/deployment changes and keep the app running through closing.

**Exit:** submission artifacts and access are checked, not merely locally generated.
Participants author social content; agents may assist with grammar only.

## 6. Planned commands and evidence handling

The following are **proposed future commands**, not currently executable project
commands and not instructions to run during the hold. M1 must create/verify the
manifest, dependency extras, app factory, markers and entry point first; then put
the actual commands in README and record results in ACCEPTANCE.md.

```powershell
# Example Windows workflow, only after implementation resumes and M1 creates it:
py -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m pytest -m "not live"
.venv\Scripts\python.exe -m pytest tests/test_publication.py -m "not live"
# Live mode additionally needs explicit opt-in, owned destinations and deployed base URL.
# Startup command and live configuration come from the verified M1/M2 deployment.
```

Ignore virtual environments, SQLite files, raw traces and credentials when M1
creates them; preserve committed synthetic fixtures and redacted evidence.
Use temporary databases/fixtures per deterministic test. A frozen source commit
plus exact commands, environment, observed assertions and trace/provider IDs
should let another operator reproduce each claim without guessing.

Framework references: [FastAPI async tests](https://fastapi.tiangolo.com/advanced/async-tests/),
[pytest markers](https://docs.pytest.org/en/stable/example/markers.html),
[SQLite transactions](https://www.sqlite.org/lang_transaction.html).
FastAPI's in-process test transport is useful for the app boundary; it does not
replace the actual HTTP lab or deployed/provider smoke obligations above.

## 7. Copyable agent handoff

```text
Implement BugProof milestone M<N> from docs/implementation-plan.md only after
checking direct resume authorization, current deadline, AGENTS.md and dependencies.
Read the relevant specification sections and affected ACCEPTANCE.md IDs. Inspect
existing code/evidence before adding work. Keep the approved boundaries and scope.
Deliver one working slice with meaningful verification. Record exact replay
commands/results, source/deployment identity and limitations in docs/evidence;
update the acceptance ledger and milestone status. Preserve the no-public-spec-issue
decision. Do not delegate unless directly authorized. Report commit, changed
files, passed/failed/not-run checks, blockers and the next milestone. Do not call
a mock integration live or change implementation scope to hide a failing gate.
```

## 8. Definition of complete

Complete means the approved workflow is deployed on Alternate Clouds, actual
evidence supports A01–A17, the human can change permitted effects, partial/uncertain
states recover honestly, and required submission artifacts are accessible before
freeze. This plan being written, a green unit test, or a polished UI is not that
completion. Current progress: M0/M1 in progress; M2–M9 not started. Independent
local M1 work proceeded while human account setup was pending; no later provider-dependent
milestone is treated as started or complete.
