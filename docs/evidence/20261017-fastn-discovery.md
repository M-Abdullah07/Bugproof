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

## Follow-up: participant-supplied endpoint

The participant specified `https://mcp.fastn.dev` with Bearer authentication and
reported Gmail/GitHub connected in that workspace. The approved endpoint was
saved privately and added explicitly to the client's allowed hosts; the
organization slug was not substituted for a project ID.

SDK connection again returned -32603. A direct read-only JSON-RPC initialize
request using the saved key in the Authorization header identified the HTTP
result: **401**, JSON `{"error":"unauthorized"}`. Key-format checks confirmed
the value was not accidentally prefixed with `Bearer ` or `FASTN_API_KEY=`.
No key value was printed. No connection, project listing, Gmail read or GitHub
write was established. The first error was therefore insufficiently diagnostic;
the CLI now records HTTP status codes without logging headers.

Current blocker: verify the credential type, active status, organization and
environment expected by this workspace's MCP endpoint. A separate generated MCP
Bearer credential may be required; that possibility is not yet confirmed.
Use the replay command above with FASTN_MCP_URL set to the participant's endpoint.

## Updated-key retry and authentication discovery

Source identity: `601ccd0`, clean application tree. After the participant saved
a replacement key, the same replay still returned HTTP 401 during `connect`.
No authenticated tool listing occurred. Local checks found one key assignment,
no surrounding/internal whitespace, no accidental Bearer/assignment prefix,
and no populated example-file key. These checks do not establish key validity.

Read-only public GETs returned HTTP 200 for:

- [Official fastn plugin README](https://github.com/fastn-ai/fastn-claude-plugins/blob/main/README.md),
  retrieved through its raw GitHub URL: it registers `https://mcp.fastn.dev`
  and explicitly describes OAuth authentication.
- `https://mcp.fastn.dev/.well-known/oauth-protected-resource`: resource
  `https://mcp.fastn.dev/`, authorization server `https://connect.fastn.dev`.
- `https://mcp.fastn.dev/.well-known/oauth-authorization-server`: authorization,
  token and registration endpoints under `https://connect.fastn.dev/oauth/`;
  authorization-code/refresh-token/client-credentials grants, S256 PKCE,
  and `mcp` scope advertised.

Inference: the current dashboard API-key Bearer setup is mismatched with this
gateway's documented OAuth flow. This does not prove the key is invalid for
other fastn services. OAuth login, token refresh, unattended deployment access,
and connected-app capabilities remain unverified. Asked the participant to
choose OAuth setup for this gateway or a workspace-generated API-key endpoint;
no authentication architecture change or new external effects performed yet.

## OAuth setup started

Added `scripts/connect-fastn-oauth.py` using the installed official SDK's PKCE,
state validation and token-refresh support. Replay from the repository root:

```powershell
.venv\Scripts\python.exe scripts/connect-fastn-oauth.py
```

Observed: syntax compilation passed; `git check-ignore` confirms credential
storage `.data/fastn-oauth.json` and temporary authorization URL under `.tools/`
are ignored. Live start reached the browser authorization step and requested
the system browser successfully. Callback listens only on `127.0.0.1:8765`,
with a ten-minute sign-in timeout. Tokens are local private files, not encrypted
storage; existing machine account permissions apply on Windows.

Human sign-in, successful MCP listing, refresh behavior and deployment credential
provisioning remain pending. This script has no mailbox-read or publication calls.
No acceptance row passes from reaching the sign-in page.

## Gateway OAuth succeeded; workspace connection still pending

After participant browser sign-in, the script exited zero: authenticated MCP
tool listing succeeded and a refresh token was present. A new client session
also authenticated without another sign-in. Refresh was attempted by returning
zero remaining token lifetime from the diagnostic storage wrapper, but no token
endpoint response was observed; this does **not** prove refresh execution.

Read-only `connection(action="list")` reported only Fastn Workspace, default
account **not connected**. Both `list_connectors(scope="org", search="gmail")`
and the GitHub equivalent returned a tool error: `configDb: unavailable on the
data plane (config-free). This code path must run on the control plane.`
These errors do not prove Gmail/GitHub connections are absent in the dashboard.

Requested `connection(action="connect", connector="Fastn Workspace")` and
opened the returned `connect.fastn.dev` authorization link privately in the
system browser. The participant must complete workspace linking before a new
capability check. Gateway authentication is now proven; workspace connection,
Gmail/GitHub operations, refresh execution and deployed access remain unverified.

## Workspace linked; both provider connections active

Participant completed the second browser connection. New authenticated calls:

- `connection(action="list")`: default Fastn Workspace active, no longer
  marked not connected.
- `fastnPlatform__getConnectorConnectionStatus(connector="github")`:
  connected true, connection status ACTIVE.
- `fastnPlatform__getConnectorMethods(id="github")`: includes `createIssue`,
  `getIssue` and issue listing operations. These are catalog capabilities,
  not proof of successful issue execution.
- The guessed `gmail` slug was absent (404). Discovery through
  `search_tools` found `fastnPlatform__listConnectors`; calling that exact tool
  through `run_tool` with `search="mail"` identified **googleGmail**.
- `fastnPlatform__getConnectorConnectionStatus(connector="googleGmail")`:
  connected true, connection status ACTIVE.
- `fastnPlatform__getConnectorMethods(id="googleGmail")`: includes list/read
  threads/messages, getProfile and sendMessage.

The generic gateway `list_connectors` still has a data-plane/configDb error;
workspace-specific catalog operations work and avoid that failing path. Initial
search for Gmail/GitHub tools returned unrelated platform tools: do not use those
as substitutes. The eventual adapter must execute discovered connector actions
through the workspace API, with exact contracts checked first.

No mailbox contents read, emails sent, or GitHub issues created in these checks.
Credential acceptance and connection-status gates are resolved. Actual provider
operation execution, refresh execution, publication recovery and deployment remain
unverified; A16 remains NOT_RUN.
