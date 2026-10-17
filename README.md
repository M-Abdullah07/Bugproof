# BugProof

A support report becomes evidence a developer can act on, followed by a
human-approved engineering handoff and reporter reply.

**Implementation resumed: local foundation works; full workflow is not built.**
Login, case-list/API, health/build reporting and persistent SQLite are implemented.
Seven local tests pass. No fastn/model connections, lab reproduction, publication
or Alternate Clouds deployment is verified. All demo data will be synthetic.

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

This covers only the local foundation. Windows Codex sandbox restrictions required
the test runner to execute with local escalation; pytest temporary data stays
under `.tools/pytest-tmp`. One upstream TestClient/httpx deprecation warning is known.
Local development uses Python directly; Docker Desktop/local builds are skipped.
The existing Dockerfile is retained for remote packaging if needed. Its build
and the real platform storage mount are NOT verified.

## Accounts needed next

- Alternate Clouds: participant reports an account with $5 balance; deployment not tested.
- Gemini: private key and `gemini-3.8-flash` model availability are verified via
  [read-only discovery](docs/evidence/20261017-gemini-model-access.md).
  Generation/structured output and actual free quota remain unverified.
  No Groq account is needed. Model adapter is not implemented yet.
- fastn: create a workspace at https://app.fastn.ai and connect controlled Gmail/GitHub.
  Saved-key discovery currently returns a [connection error](docs/evidence/20261017-fastn-discovery.md).
  Confirm the workspace MCP URL and connected accounts; tool/project mapping remains pending.
  Replay read-only discovery with `.venv\Scripts\python.exe scripts/check-fastn-access.py`.
  `FASTN_MCP_URL` optionally overrides the documented hosted endpoint with a verified
  HTTPS fastn.ai URL; credentials belong in headers, never a URL query.
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
