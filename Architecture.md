# BugProof architecture

Status: **planned, not implemented**. Execution is HELD (DEC-01).
Read the [specification](docs/specs/bugproof.md) for full behavioral contracts,
[Decisions.md](Decisions.md) for rationale and [ACCEPTANCE.md](ACCEPTANCE.md)
for proof obligations. This map explains ownership; it adds no product scope.

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

## Planned code ownership

Paths below are a proposed layout to establish when implementation resumes.
They do **not** currently exist. Keep five responsibility boundaries; files may
split when a concrete dependency or readability need justifies it.

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
| `tests/test_publication.py` | Approval, concurrency, partial failure and restart proof | Dependence on private helper names |
| `tests/test_live_smoke.py` | Explicitly enabled real integration/deployment smoke | Uncontrolled recipients, repositories or effects |

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

No application manifest, startup command, test command, container, environment
example or deployed URL exists yet. Add the smallest runnable slice after resume,
then put actual commands in the root README and executable project configuration.
Keep this document about boundaries rather than copying command inventories.

Hosting must honor platform PORT and explicit Alternate Clouds Rebuild -> Deploy.
Prove storage survival on that host. Provider capabilities, credentials and
reconciliation must be checked before dependent feature investment. All run and
deployment claims need current evidence in ACCEPTANCE.md.
