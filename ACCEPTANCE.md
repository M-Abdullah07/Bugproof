# BugProof acceptance and evidence

**Full-product verdict: NOT RUN.** Local foundation exists with seven passing
tests; no full-workflow or deployment claim has passed.
Scope approval and plan-review checks are not executable product evidence.
The [specification](docs/specs/bugproof.md) defines behavior; this file tracks
whether that behavior has been demonstrated. Implementation resumed under DEC-16;
account preflight is in progress. No product acceptance claim has passed.

## Evidence rules

1. Implement and verify at the approved authenticated API boundary with actual
   lab HTTP. Controlled model/provider responses prove deterministic behavior;
   only the separate live run proves actual account/hosting integration.
2. Attach the exact runnable command or numbered replay procedure, source commit,
   dirty-tree state, environment, observed assertions and redacted artifact.
   A proposed test filename, screenshot alone or planned command is not a pass.
3. Link records from the acceptance rows. One run may prove several IDs; each
   assertion must be identifiable. Store sanitized records under `docs/evidence/`.
   Secrets and raw mailbox data stay out of Git; use synthetic inputs.
4. After a relevant change, mark affected passes STALE until rerun. Preserve old
   records. A newer failure supersedes an older pass. Tests with doubles never
   inherit LIVE status, and fixture behavior never proves customer production.

Statuses: NOT_RUN, PASS, FAIL, BLOCKED, STALE. BLOCKED needs a concrete observed
blocker; missing future implementation is NOT_RUN. Verification mode is recorded
separately: deterministic / live / manual. No numeric score is inferred.

## Acceptance ledger

All evidence cells are intentionally empty until execution. Suggested locations
are future files, not executable commands. Pass means every assertion in that row
has current evidence; split a row if part passes while another part does not.

| ID | Claim / required observable result | Verification boundary | Status | Runnable evidence |
| --- | --- | --- | --- | --- |
| A01 | Rechecking unchanged intake and ingesting own replies preserves one case per mailbox/thread | API + controlled intake; case workflow tests | NOT_RUN | — |
| A02 | Same-key/same-payload retry on faulty API yields two distinct stored orders, actual HTTP trace and observed build | API + actual lab; case workflow tests | NOT_RUN | — |
| A03 | Corrected API yields one order for the same claim; no automatic dismissal | API + actual lab; case workflow tests | NOT_RUN | — |
| A04 | Paraphrase and changed synthetic inputs still produce a supported, grounded experiment and behavior-derived result | Deterministic API scenarios + small live model rehearsal | NOT_RUN | — |
| A05 | Missing/unsupported facts produce specific clarification/unsupported state, with no fabricated customer evidence or irrelevant run | Case workflow tests | NOT_RUN | — |
| A06 | Malformed or ungrounded model output gets at most one correction, then visible error; no publication | Controlled model through API | NOT_RUN | — |
| A07 | Unknown targets/operations, cross-fixture reads and request/time/body limits fail explicitly; omitted trace content cannot support an assertion | API + actual lab adversarial cases | NOT_RUN | — |
| A08 | Instructions embedded in email/API data cannot authorize tools, change destinations, execute code or publish | Hostile synthetic fixtures through API | NOT_RUN | — |
| A09 | Human expectation edits reevaluate complete observations; changed plans need a fresh run; invalidated/rejected approvals produce zero effects | Review flow through API | NOT_RUN | — |
| A10 | Absent, expired, stale, edited-payload and cross-case approvals are rejected by server; unauthenticated actions fail | Publication API tests | NOT_RUN | [Foundation subset only](docs/evidence/20261017-foundation.md); approval engine absent |
| A11 | Simultaneous submissions share one durable action owner; completed effects are reused, not duplicated; network I/O holds no SQLite write transaction | Controlled provider timing; publication tests | NOT_RUN | — |
| A12 | Provider success followed by timeout reconciles existing identity/marker, or visibly becomes uncertain before another send | Fault-injected publication tests + live capability check | NOT_RUN | — |
| A13 | Successful issue survives email failure; retry only unfinished eligible reply, preserve issue/link, declare complete only after both verified | Publication tests | NOT_RUN | — |
| A14 | Imported new source evidence invalidates stale approval; between issue and reply it preserves issue and stops remaining writes | Publication tests with controlled timing | NOT_RUN | — |
| A15 | Restart preserves completed provider IDs; ambiguous attempts reconcile, claim expiry never permits blind resend; interrupted experiments get fresh run/fixture | Process restart + durable SQLite + actual host restart | NOT_RUN | [Local app reconstruction subset](docs/evidence/20261017-foundation.md); no provider/host restart proof |
| A16 | On Alternate Clouds, real fastn intake -> human-approved GitHub create/read-back -> original-thread Gmail reply/read-back works in owned accounts | Separately enabled deployed live smoke | NOT_RUN | — |
| A17 | Operator can inspect source/evidence, edit expectation, reject/approve and recover visibly without reading raw JSON; refresh/reopen retains state | Browser rehearsal with explicit steps and current build | NOT_RUN | [Login/empty HTML subset](docs/evidence/20261017-foundation.md); full workspace not built |

A01–A16 correspond in order to the specification's acceptance table. A17 makes
its existing workspace contract directly reviewable; it adds no new feature.
Suggested test files are mapped in Architecture.md; fill actual selectors when
the tests exist. Current foundation commands are in README; full-workflow
tests and live smoke are not implemented.

## Evidence record format

Create `docs/evidence/<run-id>.md` when a run actually occurs:

```text
Run ID / acceptance IDs:
Timestamp (with timezone):
Source commit / dirty changes (or clean):
Environment / runtime / observed deployment build:
Mode: deterministic | live | manual
Preconditions: accounts, synthetic fixtures, target build; no credentials
Command: exact working directory + command + relevant nonsecret flags
Replay steps: required when command alone cannot reproduce the result
Expected assertions:
Observed assertions and result: PASS | FAIL | BLOCKED
Artifacts: redacted trace/log paths, provider IDs/URLs, screenshots where relevant
Coverage limits: doubles, synthetic data, conditions not exercised
Supersedes / invalidated by:
```

The first foundation record exists below `docs/evidence/`; it does not pass a
whole-product row. Attach failures too; do not replace them with a
successful screenshot. Keep the latest result visible in this ledger.

## Completion gates

- Engineering: current evidence for A01–A15; current live A16; manual A17.
- Claims: distinguish lab reproduction from production verification, plan from
  actual execution, provider double from live effect, and target from measured latency.
- Submission: use [judge_scorecard](docs/judge_scorecard.md) for criterion mapping
  and participant-provided artifact requirements. Product tests do not prove entry eligibility.
- Before freeze: record the final source commit, observed deployed build, live
  health, demo login and evidence revision. No code/deployment edits after cutoff.

## Maintenance during authorized work

For each behavior change: name affected IDs -> implement -> run the smallest
meaningful checks -> save observed evidence -> update row status/links and scorecard.
Update decisions/specification when the contract changes, not merely when code
is refactored. If a command or test is renamed, repair its evidence replay path;
historical records retain the original command and commit.
