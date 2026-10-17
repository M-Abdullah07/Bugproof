"""Read-only MCP discovery. Credentials stay in .env; raw metadata stays ignored."""

import asyncio
import json
import logging
from pathlib import Path
from urllib.parse import urlsplit

import httpx2
from dotenv import dotenv_values
from mcp import Client
from mcp.client.streamable_http import streamable_http_client


async def main():
    values = dotenv_values(".env")
    if not values.get("FASTN_API_KEY"):
        print(json.dumps({"configured": False}))
        return 2
    endpoint = values.get("FASTN_MCP_URL") or "https://mcp.live.fastn.ai/shttp"
    parsed = urlsplit(endpoint)
    if (parsed.scheme != "https" or not parsed.hostname
            or not (parsed.hostname == "fastn.ai" or parsed.hostname.endswith(".fastn.ai"))
            or parsed.username or parsed.password or parsed.query or parsed.fragment):
        print(json.dumps({"configured": True, "configuration_error":
                          "Use an HTTPS fastn.ai MCP endpoint without URL credentials or query secrets"}))
        return 2
    headers = {"Authorization": "Bearer " + values["FASTN_API_KEY"]}
    if values.get("FASTN_PROJECT_ID"):
        headers["x-project-id"] = values["FASTN_PROJECT_ID"]
    logging.disable(logging.CRITICAL)
    phase = "connect"
    try:
        async with asyncio.timeout(35):
            async with httpx2.AsyncClient(headers=headers, timeout=20) as http:
                transport = streamable_http_client(
                    endpoint, http_client=http
                )
                async with Client(transport, read_timeout_seconds=20, mode="legacy") as client:
                    phase = "list_tools"
                    tools = await client.list_tools()
                    discovery = {"tools": tools.model_dump(mode="json")}
                    names = [tool.name for tool in tools.tools]
                    project_tool = next((tool for tool in tools.tools if tool.name == "list_projects"), None)
                    if project_tool and not project_tool.inputSchema.get("required"):
                        phase = "list_projects"
                        result = await client.call_tool("list_projects", {})
                        discovery["projects"] = result.model_dump(mode="json")
                    path = Path(".tools/fastn-discovery.json")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(discovery, indent=2), encoding="utf-8")
                    print(json.dumps({"authenticated_session": True,
                                      "protocol": client.protocol_version,
                                      "tool_names": names,
                                      "project_discovery_attempted": "projects" in discovery,
                                      "metadata_path": str(path)}))
                    return 0
    except Exception as exc:
        def leaf_errors(error):
            if isinstance(error, BaseExceptionGroup):
                return [item for child in error.exceptions for item in leaf_errors(child)]
            data = getattr(error, "data", None)
            message = str(error) + (" | " + json.dumps(data, default=str) if data is not None else "")
            for name, value in values.items():
                if value and any(part in name for part in ("KEY", "SECRET", "PASSWORD", "TOKEN")):
                    message = message.replace(value, "[REDACTED]")
            return [{"type": type(error).__name__, "code": getattr(error, "code", None),
                     "message": message[:900]}]
        print(json.dumps({"authenticated_session": False, "phase": phase, "errors": leaf_errors(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
