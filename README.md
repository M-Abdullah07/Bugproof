# BugProof

A support report becomes evidence a developer can act on, followed by a
human-approved engineering handoff and reporter reply.

**Implemented locally: the complete controlled workflow.**
Gmail intake through fastn, grounded Gemini interpretation, real HTTP experiments,
human expectation/disposition editing, exact approval, GitHub issue + thread reply,
read-back and durable uncertain/partial recovery now exist.
Local live smoke completed an escalation and clarification; corrected replay
produced one order while the faulty service produced two. Cloud deployment and
host restart proof remain pending. See [acceptance evidence](ACCEPTANCE.md).

## Run locally (Windows / PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.lock
.venv\Scripts\python.exe -m pip install --no-deps -e .
# If .env does not exist, copy .env.example to .env and fill both operator secrets.
.venv\Scripts\python.exe -m bugproof
```

Open http://localhost:8000/login. Set `BUGPROOF_DEMO_PASSWORD` (12+ characters)
and `BUGPROOF_SESSION_SECRET` (32+ random characters) in private `.env` before
starting. A private generated `.env` already exists in the original workspace;
it is intentionally not shared through GitHub. Partners configure their own.
Never paste passwords or API keys into chat or commit them. PORT comes from
environment; use `BUGPROOF_ENV=production` for HTTPS-only session cookies on the host.

```powershell
.venv\Scripts\python.exe -m pytest -q -m "not live"
```

This exercises authenticated workflow scenarios with a real local TCP lab and
controlled AI/provider responses. Windows Codex sandbox restrictions required
the test runner to execute with local escalation; pytest temporary data stays
under `.tools/pytest-tmp`. Provider doubles are not live integration proof.
Local development uses Python directly; Docker Desktop/local builds are skipped.
The existing Dockerfile is retained for remote packaging if needed. Its build
and the real platform storage mount are NOT verified.

## Accounts needed next

- Alternate Clouds: participant reports an account with $5 balance; deployment not tested.
- Gemini: private key and `gemini-3.8-flash` model availability are verified via
  [read-only discovery](docs/evidence/20261017-gemini-model-access.md).
  Generation/structured output and actual free quota remain unverified.
  No Groq account is needed. Model adapter is not implemented yet.
- fastn: OAuth at `https://mcp.fastn.dev` and the linked workspace report active
  `googleGmail` and `github` connections. [Evidence and remaining limits](docs/evidence/20261017-fastn-discovery.md).
  Run `.venv\Scripts\python.exe scripts/connect-fastn-oauth.py` for interactive
  sign-in/tool listing. Private tokens/client registration stay in ignored
  `.data/fastn-oauth.json`; do not commit or share that file. Refresh execution
  and deployed provisioning remain unverified. The older API-key discovery script
  still fails on this OAuth endpoint; it is not the current login route.
- GitHub origin is already configured. No specification issue will be published.

## Start here

| Task | Read |
| --- | --- |
| Agent instructions and permissions | [AGENTS.md](AGENTS.md) |
| Exact behavior and scope | [Specification](docs/specs/bugproof.md) |
| Step-by-step build order, exit checks and explanations | [Implementation plan](docs/implementation-plan.md) |
| Decisions and reasons | [Decisions.md](Decisions.md) |
| Ownership, dependencies and planned source map | [Architecture.md](Architecture.md) |
| Acceptance claims, run status and evidence | [ACCEPTANCE.md](ACCEPTANCE.md) |
| Competition proof and submission | [Judge scorecard](docs/judge_scorecard.md) |
| Domain vocabulary | [GLOSSARY.md](GLOSSARY.md) |

Older candidate/research/design documents preserve context; they do not override
the specification or later explicit participant decisions.

## Repository and tools

GitHub: https://github.com/M-Abdullah07/Bugproof, branch `main`.
The tracker is configured; the participant chose no public specification issue.
Development skills are project-local; tool state/caches are ignored. Gstack
source is a pinned submodule: clone with `--recurse-submodules`, or run
`git submodule update --init .agents/skills/gstack` in an existing clone.
Tool readiness and limitations: [local status](docs/LOCAL-TOOLS-STATUS.md).
Use `scripts/setup-local-gstack.ps1` for its project-local setup; never assume
tool installation means the product is implemented.

Keep verified commands aligned with manifests and use ACCEPTANCE.md for proof.
See [third-party licenses](docs/licenses/).

## Operate the demo

1. Run `python scripts/connect-fastn-oauth.py` inside the virtual environment;
   complete gateway login and the workspace connection when requested.
2. Configure Gemini, a separate lab secret, the connected controlled mailbox,
   operator secrets and owned repository in private `.env` (see `.env.example`).
3. To send the three self-addressed synthetic reports through fastn, explicitly run
   `.venv\Scripts\python.exe scripts/seed-demo.py --allow-live`.
4. Open `/login`, then **Check demo inbox**. Open a report and **Investigate**.
5. Inspect order IDs/trace. Edit expectation or disposition; **Save edits**, then
   approve the exact saved actions. Unsaved changes cannot be approved.
6. **Publish / reconcile approved actions**. A verified issue appears before the
   reply is sent. Use the separate read-only delivery check after an uncertain
   outcome, expired approval or new source. A missing match never permits resend.

Opted-in live API rehearsal (creates demo issue/reply with `--publish`):

```powershell
.venv\Scripts\python.exe scripts/live-smoke.py --allow-live --publish
.venv\Scripts\python.exe scripts/live-smoke.py --allow-live --build corrected
.venv\Scripts\python.exe scripts/live-smoke.py --allow-live --scenario missing --publish
```

These scripts drive the authenticated app. Scripted approval is a preauthorized
connectivity test, not a claim that a human performed a UX rehearsal. Do not run
multiple local/cloud OAuth writers: stop the local server before handing the
latest credentials to the deployment. Cloud SQLite and OAuth files belong on
persistent `/data`; verify a real restart before asserting host durability.
