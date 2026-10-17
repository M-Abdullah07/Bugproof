"""Official SDK OAuth storage; private credentials never enter case records."""
import json
import os
import time
from pathlib import Path
from urllib.parse import urlsplit

import httpx2
from mcp.client.auth import OAuthClientProvider
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken, OAuthMetadata, ProtectedResourceMetadata

ENDPOINT = "https://mcp.fastn.dev"
CALLBACK = "http://127.0.0.1:8765/callback"


class PrivateStorage:
    def __init__(self, path=Path(".data/fastn-oauth.json"), bootstrap=""):
        self.path = Path(path)
        if bootstrap and not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            value = json.loads(bootstrap)
            self._write(value)

    def read(self):
        return json.loads(self.path.read_text()) if self.path.exists() else {}

    def _write(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        with os.fdopen(os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as stream:
            json.dump(data, stream)
        temporary.replace(self.path)

    def save(self, field, value):
        data = self.read()
        data[field] = value
        self._write(data)

    async def get_tokens(self):
        record = self.read().get("tokens")
        if not record:
            return None
        token = dict(record["value"])
        if token.get("expires_in") is not None:
            # Zero means unknown lifetime in this SDK: keep an expired value negative.
            token["expires_in"] = max(-1, token["expires_in"] - int(time.time() - record["saved_at"]))
        return OAuthToken.model_validate(token)

    async def set_tokens(self, tokens):
        self.save("tokens", {"saved_at":time.time(),"value":tokens.model_dump(mode="json")})

    async def get_client_info(self):
        value = self.read().get("client")
        return OAuthClientInformationFull.model_validate(value) if value else None

    async def set_client_info(self, client_info):
        self.save("client", client_info.model_dump(mode="json"))


class PersistentOAuthProvider(OAuthClientProvider):
    async def _initialize(self):
        await super()._initialize()
        # SDK 2.3 loads tokens but does not restore their expiry or discovery
        # metadata. Otherwise refresh falls back to the resource host's /token.
        # Load only the verified resource/issuer metadata, with no credentials.
        async with httpx2.AsyncClient(timeout=15) as http:
            resource_response=await http.get(ENDPOINT+"/.well-known/oauth-protected-resource")
            resource_response.raise_for_status()
            resource=ProtectedResourceMetadata.model_validate(resource_response.json())
            if str(resource.resource).rstrip("/")!=ENDPOINT or [str(u).rstrip("/") for u in resource.authorization_servers]!=["https://connect.fastn.dev"]:
                raise ValueError("Unexpected fastn authorization server; sign-in configuration must be reviewed")
            metadata_response=await http.get("https://connect.fastn.dev/.well-known/oauth-authorization-server")
            metadata_response.raise_for_status()
            metadata=OAuthMetadata.model_validate(metadata_response.json())
            if str(metadata.issuer).rstrip("/")!="https://connect.fastn.dev" or any(urlsplit(str(url)).scheme!="https" or urlsplit(str(url)).hostname!="connect.fastn.dev" for url in (metadata.token_endpoint,metadata.authorization_endpoint)):
                raise ValueError("Unexpected fastn OAuth metadata")
        self.context.protected_resource_metadata=resource
        self.context.oauth_metadata=metadata
        self.context.auth_server_url="https://connect.fastn.dev"
        if self.context.current_tokens:
            self.context.update_token_expiry(self.context.current_tokens)


def provider(storage, **handlers):
    return PersistentOAuthProvider(
        server_url=ENDPOINT,
        client_metadata=OAuthClientMetadata(client_name="BugProof local preflight",redirect_uris=[CALLBACK],token_endpoint_auth_method="none",scope="mcp"),
        storage=storage, **handlers,
    )
