"""Persisted expired credentials refresh at the discovered issuer, without login."""
import asyncio
import json
import time

import httpx2

from bugproof.integrations.oauth import ENDPOINT, PrivateStorage, provider


def test_expired_saved_token_refreshes_at_issuer_before_resource_request(tmp_path,monkeypatch):
    calls=[]
    async def handle(request):
        calls.append((request.url.host,request.url.path))
        if request.url.path=='/.well-known/oauth-protected-resource':
            return httpx2.Response(200,json={'resource':ENDPOINT+'/','authorization_servers':['https://connect.fastn.dev']})
        if request.url.path=='/.well-known/oauth-authorization-server':
            return httpx2.Response(200,json={'issuer':'https://connect.fastn.dev','authorization_endpoint':'https://connect.fastn.dev/oauth/authorize','token_endpoint':'https://connect.fastn.dev/oauth/token','response_types_supported':['code']})
        if request.url.host=='connect.fastn.dev' and request.url.path=='/oauth/token':
            return httpx2.Response(200,json={'access_token':'new-controlled-test-token','refresh_token':'rotated-controlled-test-token','token_type':'Bearer','expires_in':3600})
        assert request.url.host=='mcp.fastn.dev' and request.url.path=='/'
        assert request.headers['authorization']=='Bearer new-controlled-test-token'
        return httpx2.Response(200,json={'ready':True})
    transport=httpx2.MockTransport(handle)
    original=httpx2.AsyncClient
    def client(**kwargs):
        kwargs.setdefault('transport',transport)
        return original(**kwargs)
    monkeypatch.setattr(httpx2,'AsyncClient',client)
    storage=PrivateStorage(tmp_path/'oauth.json',json.dumps({'client':{'client_id':'controlled-client','issuer':'https://connect.fastn.dev','token_endpoint_auth_method':'none'},'tokens':{'saved_at':time.time()-20,'value':{'access_token':'expired-controlled-test-token','refresh_token':'controlled-test-refresh','token_type':'Bearer','expires_in':1}}}))
    async def run():
        async with httpx2.AsyncClient(auth=provider(storage)) as http:
            response=await http.get(ENDPOINT+'/')
            assert response.json()=={'ready':True}
    asyncio.run(run())
    assert ('connect.fastn.dev','/oauth/token') in calls
    assert ('mcp.fastn.dev','/token') not in calls
    assert storage.read()['tokens']['value']['refresh_token']=='rotated-controlled-test-token'
