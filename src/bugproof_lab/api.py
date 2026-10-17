import hmac
import json
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse


def router(storage, secret):
    api = APIRouter(prefix="/lab", include_in_schema=False)

    def authorized(request):
        if not secret or not hmac.compare_digest(request.headers.get("x-lab-secret", ""), secret):
            raise HTTPException(403, "Lab authorization required")

    @api.post("/fixtures")
    async def fixture(request: Request):
        authorized(request)
        body = await request.json()
        build = body.get("build")
        if build not in ("faulty", "corrected"):
            raise HTTPException(400, "Unknown build")
        fixture_id = uuid4().hex
        with storage.connection() as c:
            c.execute("INSERT INTO lab_fixtures(id,build) VALUES(?,?)", (fixture_id,build))
        return {"fixture":fixture_id, "build":f"orders-{build}-v1"}

    @api.post("/fixtures/{fixture_id}/orders")
    async def create_order(fixture_id: str, request: Request):
        authorized(request)
        raw = await request.body()
        if len(raw) > 16384:
            raise HTTPException(413, "Body limit")
        body = json.loads(raw)
        key = request.headers.get("idempotency-key", "")
        if not key or len(key) > 100 or set(body) != {"item", "quantity"} or not isinstance(body["quantity"],int) or not 1 <= body["quantity"] <= 10:
            raise HTTPException(400, "Invalid synthetic order")
        with storage.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT * FROM lab_fixtures WHERE id=?", (fixture_id,)).fetchone()
            if not row:
                raise HTTPException(404, "Fixture missing")
            orders = json.loads(row["orders_json"])
            encoded = json.dumps(body,sort_keys=True)
            if row["retry_key"] and (row["retry_key"] != key or row["payload_json"] != encoded):
                raise HTTPException(409, "Fixture belongs to another key/payload")
            if row["build"] == "corrected" and orders:
                return {"order":orders[0], "build":"orders-corrected-v1", "reused":True}
            order = {"id":uuid4().hex, **body, "retry_key":key}
            orders.append(order)
            c.execute("UPDATE lab_fixtures SET retry_key=?,payload_json=?,orders_json=? WHERE id=?", (key,encoded,json.dumps(orders),fixture_id))
        if len(orders) == 1:
            return JSONResponse({"error":"Simulated response failure after commit", "build":f"orders-{row['build']}-v1"},status_code=503)
        return {"order":order,"build":f"orders-{row['build']}-v1"}

    @api.get("/fixtures/{fixture_id}/orders")
    def orders(fixture_id: str, request: Request):
        authorized(request)
        with storage.connection() as c:
            row = c.execute("SELECT * FROM lab_fixtures WHERE id=?", (fixture_id,)).fetchone()
            if not row:
                raise HTTPException(404, "Fixture missing")
            return {"orders":json.loads(row["orders_json"]), "fixture":fixture_id, "build":f"orders-{row['build']}-v1"}
    return api
