"""Interactive fastn OAuth preflight; never prints tokens or reads mailbox data."""

import asyncio
import json
import logging
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import webbrowser

import httpx2
from mcp import Client
from mcp.client.auth import AuthorizationCodeResult, OAuthClientProvider
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.auth import OAuthClientMetadata


ENDPOINT = "https://mcp.fastn.dev"
CALLBACK = "http://127.0.0.1:8765/callback"
PRIVATE = Path(".data/fastn-oauth.json")


from bugproof.integrations.oauth import PrivateStorage


async def main():
    logging.disable(logging.CRITICAL)
    result = asyncio.get_running_loop().create_future()

    async def callback(reader, writer):
        try:
            request = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 5)
            first = request.split(b"\r\n", 1)[0].decode("ascii")
            method, target, _ = first.split(" ", 2)
            parsed = urlsplit(target)
            params = parse_qs(parsed.query)
            valid = method == "GET" and parsed.path == "/callback" and "code" in params and "state" in params
            body = b"Return to Codex. Authentication will be verified there." if valid else b"Invalid callback. Return to Codex."
            writer.write(b"HTTP/1.1 " + (b"200 OK" if valid else b"400 Bad Request") + b"\r\nContent-Type: text/plain\r\nCache-Control: no-store\r\nConnection: close\r\nContent-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body)
            await writer.drain()
            if valid and not result.done():
                result.set_result(AuthorizationCodeResult(code=params["code"][0], state=params["state"][0], iss=params.get("iss", [None])[0]))
        except (ValueError, UnicodeError, TimeoutError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    async def redirect(url):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.hostname != "connect.fastn.dev":
            raise ValueError("Unexpected authorization destination")
        # Authorization URL has PKCE/state, not an access token. Keep it out of logs.
        Path(".tools").mkdir(exist_ok=True)
        Path(".tools/fastn-authorization-url.txt").write_text(url, encoding="utf-8")
        opened = webbrowser.open(url)
        print(json.dumps({"awaiting_browser_sign_in": True, "browser_open_requested": opened}), flush=True)

    async def receive():
        return await asyncio.wait_for(asyncio.shield(result), 600)

    storage = PrivateStorage()
    auth = OAuthClientProvider(
        server_url=ENDPOINT,
        client_metadata=OAuthClientMetadata(
            client_name="BugProof local preflight", redirect_uris=[CALLBACK],
            token_endpoint_auth_method="none", scope="mcp",
        ),
        storage=storage, redirect_handler=redirect, callback_handler=receive,
    )
    try:
        async with await asyncio.start_server(callback, "127.0.0.1", 8765, limit=16384):
            async with asyncio.timeout(660):
                async with httpx2.AsyncClient(auth=auth, timeout=30) as http:
                    async with Client(streamable_http_client(ENDPOINT, http_client=http), read_timeout_seconds=650, mode="legacy") as client:
                        tools = await client.list_tools()
                        Path(".tools/fastn-discovery.json").write_text(json.dumps(tools.model_dump(mode="json"), indent=2), encoding="utf-8")
                        token = await storage.get_tokens()
                        print(json.dumps({"authenticated_session": True, "tool_names": [tool.name for tool in tools.tools], "refresh_token_present": bool(token and token.refresh_token)}), flush=True)
        return 0
    except Exception as exc:
        # Provider exceptions can contain OAuth codes or tokens; print types only.
        print(json.dumps({"authenticated_session": False, "error_type": type(exc).__name__}), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
