"""Authenticated operator workspace. No provider effects are implemented yet."""

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


def create_app(settings: Settings | None = None):
    settings = settings or Settings.from_environment()
    storage = Storage(settings.database_path)
    assets = Path(__file__).parent
    templates = Jinja2Templates(directory=assets / "templates")

    @asynccontextmanager
    async def lifespan(app):
        storage.initialize()
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
            context={"cases": storage.list_cases(), "csrf": csrf_token(request), "build": settings.build_ref},
        )

    @app.get("/api/cases")
    def case_list(request: Request):
        if not request.session.get("operator"):
            return JSONResponse({"detail": "Authentication required"}, status_code=401)
        return {"cases": storage.list_cases()}

    return app
