"""Authenticated operator workspace and explicit human-authorized workflow routes."""

import hmac
import secrets
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from bugproof.config import Settings
from bugproof.storage import Storage
from bugproof.integrations.fastn import Fastn
from bugproof.proposals import Gemini
from bugproof.experiments import Runner
from bugproof.workflow import Workflow
from bugproof.publication import Publisher
from bugproof.review import fingerprint, revise
from bugproof_lab.api import router as lab_router


def create_app(settings: Settings | None = None, *, integrations=None, proposer=None, runner=None):
    settings = settings or Settings.from_environment()
    storage = Storage(settings.database_path)
    assets = Path(__file__).parent
    templates = Jinja2Templates(directory=assets / "templates")
    integrations = integrations or Fastn(settings)
    workflow = Workflow(storage,settings,integrations,proposer or Gemini(settings))
    publisher = Publisher(storage,integrations,settings)
    runner = runner or Runner(f"http://127.0.0.1:{settings.port}",settings.lab_secret)

    @asynccontextmanager
    async def lifespan(app):
        storage.initialize()
        for item in storage.list_cases():
            case=storage.case(item["id"])
            if case["state"].get("status")=="investigating":
                storage.save_state(case["id"],{"status":"execution_error","error":"Investigation interrupted by restart. Run again with a fresh fixture."},case["version"],"restart")
        yield

    app = FastAPI(title="BugProof", lifespan=lifespan)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.session_secret,
        session_cookie="bugproof_session",
        max_age=3600,
        same_site="lax",
        https_only=settings.secure_cookies,
    )
    app.mount("/static", StaticFiles(directory=assets / "static"), name="static")
    app.include_router(lab_router(storage,settings.lab_secret))
    app.state.storage=storage

    def csrf_token(request):
        if "csrf" not in request.session:
            request.session["csrf"] = secrets.token_urlsafe(32)
        return request.session["csrf"]

    def valid_csrf(request, candidate):
        expected = request.session.get("csrf")
        return bool(
            isinstance(candidate, str)
            and isinstance(expected, str)
            and hmac.compare_digest(candidate.encode(), expected.encode())
        )

    @app.get("/healthz")
    def health():
        try:
            if not storage.health():
                raise sqlite3.DatabaseError("Schema unavailable")
        except (sqlite3.Error, OSError, TypeError):
            return JSONResponse({"status": "unavailable", "build": settings.build_ref}, status_code=503)
        return {"status": "ok", "build": settings.build_ref, "storage": "ready"}

    @app.get("/", include_in_schema=False)
    def home():
        return RedirectResponse("/cases", status_code=303)

    @app.get("/login", response_class=HTMLResponse)
    def login_page(request: Request):
        if request.session.get("operator"):
            return RedirectResponse("/cases", status_code=303)
        return templates.TemplateResponse(
            request=request, name="login.html", context={"csrf": csrf_token(request), "error": None}
        )

    @app.post("/login")
    async def login(request: Request):
        form = await request.form()
        if not valid_csrf(request, form.get("csrf_token")):
            return JSONResponse({"detail": "Invalid form token. Reload the login page."}, status_code=403)
        password = form.get("password")
        if not isinstance(password, str) or not hmac.compare_digest(
            password.encode(), settings.demo_password.encode()
        ):
            return templates.TemplateResponse(
                request=request, name="login.html",
                context={"csrf": csrf_token(request), "error": "Incorrect password."}, status_code=401,
            )
        request.session.clear()
        request.session.update(operator="demo-operator", csrf=secrets.token_urlsafe(32))
        return RedirectResponse("/cases", status_code=303)

    @app.post("/logout")
    async def logout(request: Request):
        form = await request.form()
        if not request.session.get("operator") or not valid_csrf(request, form.get("csrf_token")):
            return JSONResponse({"detail": "Authentication and valid form token required"}, status_code=403)
        request.session.clear()
        return RedirectResponse("/login", status_code=303)

    @app.get("/cases", response_class=HTMLResponse)
    def cases(request: Request):
        if not request.session.get("operator"):
            return RedirectResponse("/login", status_code=303)
        return templates.TemplateResponse(
            request=request, name="cases.html",
            context={"cases": [storage.case(c["id"]) for c in storage.list_cases()], "csrf": csrf_token(request), "build": settings.build_ref,"configured":bool(settings.mailbox and settings.gemini_key),"repository":settings.repository,"notice":request.session.pop("notice",None)},
        )

    @app.get("/api/cases")
    def case_list(request: Request):
        if not request.session.get("operator"):
            return JSONResponse({"detail": "Authentication required"}, status_code=401)
        return {"cases": storage.list_cases()}

    @app.get("/api/session")
    def session(request: Request):
        if not request.session.get("operator"):
            return JSONResponse({"detail":"Authentication required"},status_code=401)
        return {"csrf":csrf_token(request),"build":settings.build_ref}

    @app.get("/api/cases/{case_id}")
    def case_json(case_id: str, request: Request):
        if not request.session.get("operator"):
            return JSONResponse({"detail":"Authentication required"},status_code=401)
        try:
            return storage.case(case_id)
        except ValueError as exc:
            return JSONResponse({"detail":str(exc)},status_code=404)

    @app.get("/cases/{case_id}",response_class=HTMLResponse)
    def case_page(case_id: str, request: Request):
        if not request.session.get("operator"):
            return RedirectResponse("/login",status_code=303)
        try:
            case=storage.case(case_id)
        except ValueError:
            return JSONResponse({"detail":"Case not found"},status_code=404)
        return templates.TemplateResponse(request=request,name="case.html",context={"case":case,"csrf":csrf_token(request),"fingerprint":fingerprint(case),"notice":request.session.pop("notice",None),"approval":request.session.get("approval:"+case_id),"build":settings.build_ref})

    async def input_data(request):
        if not request.session.get("operator"):
            raise PermissionError("Authentication required")
        body=await request.body()
        if len(body)>65536:
            raise ValueError("Request exceeds 64 KiB")
        values=await request.json() if "application/json" in request.headers.get("content-type","") else dict(await request.form())
        if not valid_csrf(request,request.headers.get("x-csrf-token") or values.get("csrf_token")):
            raise PermissionError("Invalid form token; reload the page")
        return values

    @app.post("/api/intake")
    @app.post("/intake")
    async def intake(request: Request):
        try:
            await input_data(request)
            result={"cases":await workflow.intake()}
        except PermissionError as exc:
            return JSONResponse({"detail":str(exc)},status_code=403)
        except Exception as exc:
            message=str(exc) if isinstance(exc,(ValueError,RuntimeError)) else type(exc).__name__
            if request.url.path.startswith("/api/"):
                return JSONResponse({"detail":message},status_code=409)
            request.session["notice"]=message
            return RedirectResponse("/cases",status_code=303)
        if request.url.path.startswith("/api/"):
            return result
        request.session["notice"]=f"Inbox checked: {len(result['cases'])} eligible thread(s)."
        return RedirectResponse("/cases",status_code=303)

    @app.post("/api/cases/{case_id}/{operation}")
    @app.post("/cases/{case_id}/{operation}")
    async def operate(case_id: str, operation: str, request: Request):
        try:
            values=await input_data(request)
            case=storage.case(case_id)
            if operation in ("investigate","review","approve","reject") and values.get("fingerprint")!=fingerprint(case):
                raise ValueError("This page is stale. Reload before changing or approving the case.")
            if operation=="investigate":
                result=await workflow.investigate(case_id,values.get("build","faulty"),runner)
            elif operation=="review":
                state=revise(case,settings,values)
                storage.save_state(case_id,state,case["version"],"human_review")
                result=storage.case(case_id)
            elif operation=="approve":
                preview=case["state"].get("preview")
                if not preview or case["state"].get("status") not in ("ready_for_review","execution_error"):
                    raise ValueError("Review the case before approval")
                if "reply" in values and revise(case,settings,values)["preview"]!=preview:
                    raise ValueError("Unsaved edits detected. Save edits, inspect the updated preview, then approve.")
                approval=storage.add_approval(case,fingerprint(case),preview,request.session["operator"],settings.approval_seconds)
                request.session["approval:"+case_id]=approval
                result={"approval_id":approval,"expires_in":settings.approval_seconds}
            elif operation=="publish":
                approval=values.get("approval_id") or request.session.get("approval:"+case_id) or ""
                result=await publisher.publish(case_id,approval)
            elif operation=="reconcile":
                result=await publisher.reconcile(case_id)
            elif operation=="reject":
                state={**case["state"],"status":"rejected"}
                storage.save_state(case_id,state,case["version"],"human_rejection")
                request.session.pop("approval:"+case_id,None)
                result={"status":"rejected","external_writes":0}
            else:
                raise ValueError("Unknown operation")
        except PermissionError as exc:
            return JSONResponse({"detail":str(exc)},status_code=403)
        except Exception as exc:
            message=str(exc) if isinstance(exc,(ValueError,RuntimeError)) else type(exc).__name__
            if request.url.path.startswith("/api/"):
                return JSONResponse({"detail":message},status_code=409)
            request.session["notice"]=message
            return RedirectResponse(f"/cases/{case_id}",status_code=303)
        if request.url.path.startswith("/api/"):
            return result
        request.session["notice"]=result.get("detail") or ("Saved. Review the result below." if operation!="publish" else "Publication: "+result.get("status","unknown"))
        return RedirectResponse(f"/cases/{case_id}",status_code=303)

    return app
