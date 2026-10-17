# Local authenticated/storage foundation

Date: October 17, 2026, Asia/Karachi.
Mode: deterministic local API tests; no external APIs or paid services invoked.
Source: foundation changes after parent e7f0e3f, dirty tree at execution. The
containing implementation commit identifies the tested source; its hash is not
self-referentially inserted here. `git log --follow -- docs/evidence/20261017-foundation.md`
locates that commit for replay. Subsequent behavior changes require a fresh record.

## Replay

Working directory: repository root. Install `requirements.lock`, then the local
package with `pip install --no-deps -e .` in a Python 3.13 virtual environment.

```powershell
.venv\Scripts\python.exe -m pytest -q -m "not live" --tb=short -o faulthandler_timeout=15
```

Final replay: **7 passed, 1 warning in 1.04s**, exit code 0 (an earlier successful
run took 0.90s). On this Windows Codex
host the command required local escalation: sandbox pytest temp creation first
failed, then a sandbox threaded TestClient run stalled and was interrupted.
Project-local pytest basetemp and an unsandboxed local-only rerun resolved execution.
The earlier runs are not counted as passes. No provider credentials were used.

## Observed assertions

| Test | What was proved |
| --- | --- |
| Health/storage | Current build response; dropping schema makes health return 503 |
| Private pages/API | Unauthenticated browser redirects; API rejects with 401 |
| Bad password/CSRF | Neither invalid form token nor wrong password creates authenticated access |
| Login/logout | Authenticated empty list and honest unconnected state; tampered logout rejected; valid logout revokes access |
| Storage reconstruction | Database installation identity and inserted synthetic case survive app teardown/recreation |
| Configuration | Missing operator password/session secret fails explicitly |
| Production cookies | HTTPS session cookie has Secure/HttpOnly/SameSite; it is not sent on plain HTTP |

These are subsets relevant to A10/A15/A17, not completed acceptance rows. The
restart test reconstructs the application, not the OS process, cloud volume or
provider effects. No claim/evidence review, lab, LLM, Gmail, GitHub write or live
Alternate Clouds deployment is proved. Dockerfile is prepared but not built.
Known warning: current Starlette TestClient deprecates httpx in favor of httpx2;
the compatibility path still passed. No production guarantee follows from the test result.

Real operator secrets were generated privately in Git-ignored `.env` and never
printed. Tests use synthetic credentials and temporary SQLite. No evidence file
contains real passwords, API keys or private messages.

## Real local HTTP smoke

Started `.venv\Scripts\python.exe -m bugproof` from the repository root using
private `.env`. Then executed:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/healthz
Invoke-WebRequest http://127.0.0.1:8000/login
.venv\Scripts\python.exe -m pip check
git check-ignore .env .venv .data
```

Observed health: status `ok`, storage `ready`, build `foundation-working-tree`.
Login returned HTTP 200 and the expected password form. Dependency consistency
check passed. `.env`, `.venv` and `.data` were ignored. This proves local TCP
startup, not container/cloud deployment; the local build label is not a deployed
commit SHA. No private environment contents were printed.
