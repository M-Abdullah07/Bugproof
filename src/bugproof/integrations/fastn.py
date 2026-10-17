"""Narrow operations using discovered fastn workspace action contracts."""
import asyncio
import base64
import json
import logging
from email.message import EmailMessage
from email.utils import parseaddr

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

from bugproof.integrations.oauth import ENDPOINT, PrivateStorage, provider

# Public catalog IDs discovered from the authenticated workspace, not credentials.
CONNECTORS = {"gmail":"ec3c1b4a-e281-4c5e-9a6b-90eb4a59882f","github":"64cbe4f6-7e1e-4859-96e7-7699123aaedc"}
ACTIONS = {
    "profile":("gmail","727b6588-fd72-47de-ba8f-3999457ddfdb"),
    "threads":("gmail","2066e670-4b2b-43e0-8772-34f689ac59f2"),
    "thread":("gmail","d00eb9eb-a8a1-4db9-9405-1f596f18dfdc"),
    "message":("gmail","5439d473-5629-4e9a-933a-f6b2f50c6106"),
    "send":("gmail","8ef24ff3-efa1-40dd-811b-b9bca6730b28"),
    "messages":("gmail","8c4544f2-e9ce-413d-b01d-c824f280afae"),
    "create_issue":("github","dbfcdcbc-633c-4833-b8a0-6505c5d3b540"),
    "issue":("github","f4d572d0-cab9-4085-87a0-3b900bcff76a"),
    "issues":("github","8e4e2daf-bb1a-4cb1-8c3e-3c5984ad6619"),
    "repository":("github","de2a0a81-fe18-4f05-9607-1128e50ef757"),
}


class ProviderError(RuntimeError):
    """May follow a remote write; caller must reconcile, never blindly resend."""


class ProviderRejected(ProviderError):
    """An explicit provider rejection establishes that this attempt was not applied."""


class Fastn:
    def __init__(self, settings):
        logging.getLogger("mcp").setLevel(logging.CRITICAL)
        self.settings = settings
        self.storage = PrivateStorage(settings.oauth_path, settings.oauth_json)
        self.auth = provider(self.storage)
        # One in-process transport/refresh owner. Runtime uses one worker.
        self.lock = asyncio.Lock()

    async def action(self, name, inputs):
        connector, action_id = ACTIONS[name]
        async with self.lock:
            try:
                async with asyncio.timeout(55):
                    async with httpx2.AsyncClient(auth=self.auth,timeout=40) as http:
                        async with Client(streamable_http_client(ENDPOINT,http_client=http),read_timeout_seconds=50,mode="legacy") as client:
                            result = await client.call_tool("fastnPlatform__executeAction", {"id":action_id,"connectorId":CONNECTORS[connector],"connectionName":"default","input":inputs})
                            if result.is_error:
                                raise ProviderError("fastn rejected the action; inspect connection permissions")
                            content = next((part.text for part in result.content if hasattr(part,"text")), "{}")
                            data = json.loads(content).get("data",{})
                            if not data.get("success") or not 200 <= data.get("status",0) < 300:
                                if data.get("status") in (400,401,403,404,422,429):
                                    raise ProviderRejected(f"Provider explicitly rejected request (HTTP {data['status']})")
                                raise ProviderError(f"Provider returned status {data.get('status','unknown')}")
                            return data["response"]
            except ProviderError:
                raise
            except Exception as exc:
                raise ProviderError(f"Connection interrupted ({type(exc).__name__}); outcome may be uncertain") from None

    def repo_args(self):
        owner,repo = self.settings.repository.split("/",1)
        return {"owner":owner,"repo":repo}

    async def intake(self):
        mailbox = self.settings.mailbox
        if not mailbox:
            raise ProviderError("Configure the controlled BUGPROOF_MAILBOX first")
        listing = await self.action("threads", {"q":f'subject:"BugProof Demo" from:{mailbox}',"maxResults":10})
        sources = []
        for thread in listing.get("threads",[]):
            data = await self.action("thread", {"id":thread["id"],"format":"full"})
            messages = []
            for message in data.get("messages",[]):
                headers = {h["name"].lower():h["value"] for h in message.get("payload",{}).get("headers",[])}
                if headers.get("x-bugproof-action") or parseaddr(headers.get("from",""))[1].lower() != mailbox.lower():
                    continue
                text = self.text(message.get("payload",{}))
                # A provider that strips custom headers still cannot ingest our replies.
                if "BugProof delivery marker:" in text:
                    continue
                if len(text.encode()) > 16384:
                    raise ProviderError("Report body exceeds demo intake limit")
                messages.append({"id":message["id"],"text":text,"subject":headers.get("subject",""),"message_id":headers.get("message-id",""),"references":headers.get("references",""),"sender":mailbox})
            if messages:
                sources.append({"thread_id":thread["id"],"messages":messages})
        return sources

    @staticmethod
    def text(payload):
        if payload.get("mimeType") == "text/plain" and payload.get("body",{}).get("data"):
            data=payload["body"]["data"]
            return base64.urlsafe_b64decode(data+"="*(-len(data)%4)).decode("utf-8",errors="replace")
        return "\n".join(Fastn.text(part) for part in payload.get("parts",[]))

    async def create_issue(self, title, body, marker):
        return await self.action("create_issue", {**self.repo_args(),"title":title,"body":body+f"\n\n<!-- {marker} -->","labels":[],"assignees":[]})

    async def get_issue(self, number):
        return await self.action("issue",{**self.repo_args(),"issue_number":number})

    async def find_issue(self, marker):
        for page in range(1,4):
            rows=await self.action("issues",{**self.repo_args(),"state":"all","per_page":100,"page":page})
            for row in rows:
                if marker in (row.get("body") or ""):
                    return row
            if len(rows)<100:
                break
        return None  # Absence in a bounded search never authorizes resend.

    async def send_reply(self, source, text, marker):
        last=source["messages"][-1]
        message=EmailMessage()
        message["From"]=self.settings.mailbox
        message["To"]=self.settings.mailbox
        subject=last["subject"]
        message["Subject"]=subject if subject.lower().startswith("re:") else "Re: "+subject
        message["Message-ID"]=f"<{marker}@bugproof.demo>"
        message["X-BugProof-Action"]=marker
        if last["message_id"]:
            message["In-Reply-To"]=last["message_id"]
            message["References"]=(last["references"]+" "+last["message_id"]).strip()
        message.set_content(text+f"\n\nBugProof delivery marker: {marker}")
        raw=base64.urlsafe_b64encode(message.as_bytes()).decode()
        return await self.action("send",{"raw":raw,"threadId":source["thread_id"]})

    async def get_message(self, message_id):
        return await self.action("message",{"id":message_id,"format":"full"})

    async def find_reply(self, marker):
        # Live Gmail rewrote Message-ID; search the preserved body marker instead.
        rows=await self.action("messages",{"q":f'in:sent "{marker}"',"maxResults":10})
        for row in rows.get("messages",[]):
            data=await self.get_message(row["id"])
            if marker in self.text(data.get("payload",{})):
                return data
        return None
