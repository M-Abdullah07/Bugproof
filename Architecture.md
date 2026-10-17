# BugProof architecture

Status: **workflow deployed and verified on Alternate Clouds**. Execution resumed under DEC-16.
Hosting/storage and container restart evidence: [deployment record](docs/evidence/20261017-deployment.md).
Read the [specification](docs/specs/bugproof.md) for full behavioral contracts,
[Decisions.md](Decisions.md) for rationale and [ACCEPTANCE.md](ACCEPTANCE.md)
for proof obligations. This map explains ownership; it adds no product scope.
For ordered implementation cards and operator explanations, use the
[implementation plan](docs/implementation-plan.md). Its proposed routes and commands
become executable references only when implemented and verified.

## Workflow and authority

```text
Gmail --fastn--> source snapshot / case revision
                       |
                  AI proposal (no effect authority)
                       |
          missing/unsupported ----> human clarification review
                       |
                 validate bounded plan
                       |
             runner --actual HTTP--> isolated lab API
                       |
                immutable evidence
                       |
          HUMAN: expectation / disposition / exact action approval
                       |
          revalidate revision + approval; SQLite exclusive claim
                       |
          fastn --> GitHub issue --> read-back --> Gmail reply --> read-back
                       |
             complete / partial / uncertain (persisted)
```

The model proposes structured data; a fixed runner chooses permitted effects.
Source text, API responses and model output are untrusted data. Registered
targets, recipients and repositories come from server configuration. The model
cannot choose arbitrary destinations, run generated code or authorize publication.

## Code ownership

The application, five workflow boundaries, fastn/OAuth adapter and lab now exist.
The table maps their ownership. Tests for workflow and publication currently share
`tests/test_case_workflow.py`; a separate publication file is unnecessary. Keep
five responsibility boundaries; split files only for concrete readability/dependency needs.

| Planned location | Owns | Must not own |
| --- | --- | --- |
| `src/bugproof/workflow.py` | Case orchestration, source revisions and persisted transitions | Provider-specific transport or human authorization policy |
| `src/bugproof/proposals.py` | Grounded interpretation, structured plans and draft communication | Credentials, arbitrary execution or publication authority |
| `src/bugproof/experiments.py` | Plan validation, budgets, fixture isolation, HTTP trace and assertions | Human approval or external customer effects |
| `src/bugproof/review.py` | Expectation/disposition edits, exact previews and approval validation | Bypassing publisher ownership/reconciliation |
| `src/bugproof/publication.py` | Action intents, exclusive claims, ordered effects and reconciliation | Inventing evidence or changing approved payloads |
| `src/bugproof/integrations/fastn.py` | Typed provider operations and normalized provider errors | Workflow decisions, model instructions or authorization |
| `src/bugproof/storage.py` | SQLite schema, transactions, identity constraints and persisted records | HTTP/provider calls inside write transactions |
| `src/bugproof/web.py`, `templates/` | Authenticated routes and server-rendered views | Trusting browser-supplied approval flags |
| `src/bugproof_lab/` | Synthetic order state, faulty/corrected behavior, authenticated fixture reset | Production data or canned results selected by report wording |
| `tests/test_case_workflow.py` | Main authenticated API acceptance scenarios with actual lab HTTP | Claims of live provider acceptance from doubles |
| `tests/test_case_workflow.py` (publication scenarios) | Approval, concurrency, partial failure and restart proof | Dependence on private helper names |
| `scripts/live-smoke.py` | Explicitly enabled real integration/deployment smoke | Uncontrolled recipients, repositories or effects |

Supporting transport/storage/view files are not additional autonomous services.
The lab is a separate authority boundary, not a requirement for another hosting
product. Use actual HTTP even if application and lab share a deployment.

Dependency direction: web -> workflow/review -> proposals/experiments/publication
-> narrow storage/provider contracts. Keep shared records/schemas passive and
credentials in server configuration. The lab never imports workflow or publisher
code to decide its result. Avoid circular imports and a generic catch-all utils module.

## State and recovery

Persist source revisions, interpretations, plans/runs, immutable evidence,
dispositions, previews/approvals, action intents and provider IDs. The
specification defines exact validity and transitions; these are the critical seams:

| Boundary | Invariant | Acceptance |
| --- | --- | --- |
| Intake | One case per authorized mailbox/thread; new inbound evidence revises, own replies do not | A01, A14 |
| Experiment | Actual observed state supports the assertion; limits/uncertainty remain visible | A02–A07 |
| Approval | Bind source/expectation/evidence/build/destinations/payload and reviewer; recheck before effects | A09–A10 |
| Publication | Unique action identity; short atomic ownership claim, then network I/O after commit | A11 |
| Ambiguous effect | Reconcile before retry; expired ownership alone never means the provider did nothing | A12, A15 |
| Partial handoff | Preserve issue URL; resume only eligible unfinished action with valid approval | A13–A15 |

Do not hold SQLite write transactions open during provider calls. Local commits
cannot make GitHub and Gmail atomic. An unresolved send remains uncertain with
manual reconciliation, rather than a blind retry or false success.

## Build and runtime discovery

Manifest, startup, test command, environment example and Dockerfile now exist;
verified commands and the live URL are in README. Foundation and actual-TCP-lab
workflow tests pass; exact proof is in ACCEPTANCE.md. The remote image build,
platform mount, deployed smoke and hosted container restart passed.
Local development runs Python directly (DEC-17). GitHub Actions builds the image;
Alternate Clouds hosts it (DEC-22). Installing Docker locally is not a milestone.

Hosting must honor platform PORT and explicit Alternate Clouds Rebuild -> Deploy.
Prove storage survival on that host. Provider capabilities, credentials and
reconciliation must be checked before dependent feature investment. All run and
deployment claims need current evidence in ACCEPTANCE.md.

## Implemented transport and recovery details

Fastn uses the official MCP SDK OAuth provider, then the workspace executeAction
tool with catalog-discovered public action/connector IDs. It normalizes responses;
no direct Gmail/GitHub bypass exists. The `googleGmail` slug differs from `gmail`.
Private OAuth state is stored separately from cases; one worker serializes refresh.
The cloud bootstrap must use the latest local OAuth file, then the cloud becomes
the sole active token writer. On-disk rotated tokens take precedence over bootstrap.

SQLite stores case state versions, immutable history, approval snapshots, action
ownership/results and action payload snapshots. Read-only reconciliation uses the
original snapshot even after source updates or approval expiry; it cannot resend.
Only an explicit provider rejection can become an eligible failed attempt;
ambiguous attempts remain uncertain if bounded lookup finds no match.

The lab router shares the deployment and SQLite but has separate credentials and
fixture tables. The runner uses loopback HTTP, never in-process canned responses.
Container startup initializes /data ownership then drops to UID 10001.

Operational limit observed during UI deployment: provider migration reset the
case database despite configured volume storage. Container restart survival was
proved separately. Cross-provider durability and deduplication after database loss
are not supported; see docs/evidence/20261017-ui.md.
