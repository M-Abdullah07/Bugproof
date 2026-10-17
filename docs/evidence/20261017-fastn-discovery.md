# Fastn discovery: blocked before session establishment

Date: October 17, 2026, approximately 09:00 PKT.
Source parent: af36148; discovery/dependency changes were uncommitted when run.
Mode: live read-only protocol discovery. No emails, issue writes or mailbox
content reads were performed. Keys were loaded privately from `.env` and not printed.

## Replay

From the repository root with the locked dependencies installed and a saved
`FASTN_API_KEY` in `.env`:

```powershell
.venv\Scripts\python.exe scripts/check-fastn-access.py
```

Endpoint tested: `https://mcp.live.fastn.ai/shttp`, the hosted endpoint documented
by [fastn's MCP repository](https://github.com/fastn-ai/fastn-mcp).
Client: official MCP Python SDK 2.3.0 with authenticated HTTPS transport.
Both automatic negotiation and explicit legacy handshake returned MCP error
`-32603`, message `Server returned an error response`. Final instrumented run
reported phase `connect`, exit code 1, before tool/project listing.

## Meaning and limit

Saved credential presence is verified; authenticated session, project selection,
connected Gmail/GitHub tools and publication/read-back capabilities are NOT.
The provider error alone does not prove an invalid key or a valid key. The
organization slug is not treated as a project ID. No discovered metadata file
exists from a successful session, and no acceptance row passes from these attempts.

Required clarification: the workspace's actual generated MCP connection URL
(without credentials/query secrets), and whether Gmail/GitHub connections are ready.
Keep the current provider gate blocked pending this; do not route around fastn
with unrelated connector access or replace it with mocked success.

## Local regression check after SDK installation

```powershell
.venv\Scripts\python.exe -m pytest -q -m "not live" --tb=short
.venv\Scripts\python.exe -m pip check
```

Observed: `7 passed in 0.90s`; dependency consistency passed. Tests used local
temporary data and no external services. The SDK installs httpx2, removing the
previous TestClient compatibility warning in this run. The lock preserves a
Windows marker for pywin32 so it is not required on Linux. The Docker build and
deployed storage remain unverified.
