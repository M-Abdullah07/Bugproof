# Alternate Clouds deployment verification

Latest application image: `55121985153118d1b605a4991674d170d54da25c`.
See [UI redeployment/recovery record](20261017-ui.md) for current cases, issue #3,
and the observed provider-migration data-loss limit. The initial run below is historical.

Date: October 17, 2026, approximately 10:00–10:20 PKT. Status: PASS.
Project: BugProof. Active deployment target: BugProof Live,
service `cmvbxi3v5197nbs1u2rwc0lxc`.

## Build evidence

The original Alternate Clouds GitHub build failed before application execution:
its Fly builder cache volumes were full/busy (HTTP 412 after six allocation
attempts). Application code was not implicated by that failure.

Fallback keeps mandatory hosting on Alternate Clouds: build the existing image
in GitHub Actions, then deploy it through the platform's Docker Image option.
No local Docker installation or new registry account was required.

- [Successful image build](https://github.com/M-Abdullah07/Bugproof/actions/runs/39004689891)
- Image: `ghcr.io/m-abdullah07/bugproof:22fa58e80581b7b149cff6a4385a30556d759c70`
- Packaging imports, absent `/app/.env`, dependency check and mounted-volume HTTP
  startup passed on Linux. First CI attempt exposed a read-only health-probe
  startup race; retrying all transient curl connection errors fixed the check.
- Anonymous GHCR manifest pull returned HTTP 200: no registry secret needed.

## Configured deployment

One CPU, 1 GiB memory, 10 GiB ephemeral storage; 1 GiB persistent volume named
`bugproof-data` mounted at `/data`. HTTP mapping container 8000 to public 80.
Probe `/healthz`, port 8000, expected 200. Total service spend capped at $4.50
within the participant's reported $5 credit; no duration auto-stop selected.
Automatic failover is disabled for this stateful service.

Replacement credentials imported through guarded file selection; their values
were not displayed. Local app/probes stopped before cloud credential handoff.
Observed UI: Active, 1/1 running, $0.0029/hour. The unused, never-deployed
GitHub-build service was permanently deleted after explicit participant approval;
only BugProof Live remains. No runtime cases were deleted.

## Deployed replay and observations

URL: https://alternate-graceful-plain-7359-docker-app.alternatefutures.ai

HTTPS `/healthz` returned 200, status `ok`, storage `ready`, build
`22fa58e80581b7b149cff6a4385a30556d759c70`. `/login` returned 200;
unauthenticated `/api/cases` returned 401. Browser login, source/evidence inspection
and completed issue link worked. Credentials remain private.

From the repository root, using the private operator password from `.env`:

```powershell
.venv/Scripts/python.exe scripts/live-smoke.py --base-url https://alternate-graceful-plain-7359-docker-app.alternatefutures.ai --allow-live --publish
.venv/Scripts/python.exe scripts/live-smoke.py --base-url https://alternate-graceful-plain-7359-docker-app.alternatefutures.ai --allow-live --scenario missing --publish
.venv/Scripts/python.exe scripts/live-smoke.py --base-url https://alternate-graceful-plain-7359-docker-app.alternatefutures.ai --allow-live --scenario paraphrase --build corrected
```

- Retry case `1087433b26574b69b73ec8e6cafb83d1`: actual HTTP statuses
  `[200,503,200,200]`, two distinct stored orders, reproduced discrepancy.
  [Demo issue #2](https://github.com/M-Abdullah07/Bugproof/issues/2) and the
  original-thread Gmail reply were read back and verified; delivery complete.
- Missing case `3fea0da6b3f241229e603c9597137675`: insufficient information,
  zero orders/no experiment trace; verified clarification reply, no issue.
- Paraphrase case `1869e9ee48c545b7a938c706828fb99a`: corrected API yielded one
  stored order; not reproduced under stated conditions; still awaiting human review.

These use actual Gemini, fastn MCP, Gmail and GitHub in controlled accounts.
Scripted approval is preauthorized connectivity proof; the separate browser
rehearsal establishes human editing/rejection usability.

## Hosted process restart (A15)

1. Record the completed retry case's version (3), two completed action IDs,
   provider IDs and a current approval using the authenticated API.
2. In Alternate Clouds Terminal, inspect `/proc/1/stat`: Python PID 1 start ticks
   `24525536`. Run `kill -TERM 1` for this container only.
3. Observe terminal session end and HTTPS health recover to 200. Reconnect:
   Python PID 1 now has start ticks `24561602`, proving process replacement.
4. Read the same case and publish with its existing approval. Observed:
   `durable_actions_preserved=true`, `existing_approval_survived=true`,
   `replay_status=complete`, `action_count=2`, `provider_ids_unchanged=true`.

Private capture helpers/IDs remain ignored under `.tools/`; the public replay
procedure above uses the app API and cloud Terminal. The additional deterministic
interrupted-investigation test proves a visible interrupted state and a fresh
run/fixture on replay. Latest suite: **36 passed in 24.80s**; app source matches
the image above, with only that test and documentation added afterward.

Limits: this proves container process restart on the actual host and persistent
volume, not physical provider reboot, provider migration or commercial demand.
Timeout/concurrency adverse cases use controlled providers in the separate
[workflow record](20261017-workflow.md). No production customer/payment data used.

## Screenshots

- [Deployed case workspace](images/bugproof-app.png)
- [Active deployment/network](images/alternate-clouds.png)
- [Only live service after approved cleanup](images/alternate-clouds-cleanup.png)
