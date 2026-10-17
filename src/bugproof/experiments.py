"""A fixed executor, never model-authored code or arbitrary network destinations."""
import asyncio
import json
import time
from uuid import uuid4

import httpx


def evaluate(evidence, expected_count):
    if not evidence.get("complete"):
        return "execution_error"
    return "reproduced_discrepancy" if len(evidence["orders"]) != expected_count else "not_reproduced_under_stated_conditions"


class Runner:
    def __init__(self, base_url, secret, *, max_requests=8, seconds=30, request_limit=16384, response_limit=65536):
        self.base_url=base_url
        self.secret=secret
        self.max_requests=max_requests
        self.seconds=seconds
        self.request_limit=request_limit
        self.response_limit=response_limit

    async def run(self, plan, build):
        if plan.get("target") != "orders-lab" or plan.get("operations") != ["create","retry","inspect"] or build not in ("faulty","corrected"):
            raise ValueError("Unknown target, build or operation sequence")
        item=plan.get("synthetic_item")
        quantity=plan.get("synthetic_quantity")
        if not isinstance(item,str) or not 1 <= len(item) <= 60 or type(quantity) is not int or not 1 <= quantity <= 10:
            raise ValueError("Invalid synthetic input")
        run_id=uuid4().hex
        result={"run_id":run_id,"target":"orders-lab","synthetic":True,"trace":[],"complete":False,"started":time.time(),"orders":[]}
        try:
            async with asyncio.timeout(self.seconds):
                async with httpx.AsyncClient(base_url=self.base_url,headers={"x-lab-secret":self.secret},timeout=min(self.seconds,10),follow_redirects=False) as client:
                    async def request(method,path,payload=None,key=None):
                        if len(result["trace"]) >= self.max_requests:
                            raise ValueError("Request budget exceeded")
                        if payload is not None and len(json.dumps(payload).encode()) > self.request_limit:
                            raise ValueError("Request body limit exceeded")
                        headers={"idempotency-key":key} if key else {}
                        async with client.stream(method,path,json=payload,headers=headers) as response:
                            captured=bytearray()
                            async for chunk in response.aiter_bytes():
                                captured.extend(chunk)
                                if len(captured)>self.response_limit:
                                    result["trace"].append({"method":method,"path":path,"status":response.status_code,"truncated":True})
                                    raise ValueError("Response capture limit exceeded; omitted content is not evidence")
                            data=json.loads(captured)
                            result["trace"].append({"method":method,"path":path,"request":payload,"retry_key":key,"status":response.status_code,"response":data,"at":time.time(),"truncated":False})
                            return response.status_code,data
                    status,fixture=await request("POST","/lab/fixtures",{"build":build})
                    if status!=200:
                        raise ValueError("Fixture setup failed")
                    result.update(fixture=fixture["fixture"],build=fixture["build"])
                    path=f"/lab/fixtures/{fixture['fixture']}/orders"
                    payload={"item":item,"quantity":quantity}
                    key="demo-"+run_id
                    first,_=await request("POST",path,payload,key)
                    second,_=await request("POST",path,payload,key)
                    status,observed=await request("GET",path)
                    if first!=503 or second!=200 or status!=200 or observed.get("fixture")!=result["fixture"] or observed.get("build")!=result["build"]:
                        raise ValueError("Unexpected API response; cannot support a completed experiment")
                    orders=observed["orders"]
                    if not orders or any(order.get("retry_key")!=key or order.get("item")!=item or order.get("quantity")!=quantity for order in orders) or len({order["id"] for order in orders})!=len(orders):
                        raise ValueError("Observed orders do not belong to the generated fixture/key/payload")
                    result.update(orders=orders,complete=True,retry_key=key)
        except (ValueError,httpx.HTTPError,TimeoutError,KeyError) as exc:
            result["error"]=str(exc) if isinstance(exc,ValueError) else type(exc).__name__
        result["elapsed_seconds"]=round(time.time()-result["started"],3)
        result["outcome"]=evaluate(result,1)
        return result
