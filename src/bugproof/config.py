"""Validated server configuration; secrets never enter browser session data."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import dotenv_values


@dataclass(frozen=True)
class Settings:
    demo_password: str = field(repr=False)
    session_secret: str = field(repr=False)
    database_path: Path = Path(".data/bugproof.sqlite3")
    build_ref: str = "development"
    secure_cookies: bool = False
    port: int = 8000
    gemini_key: str = field(default="", repr=False)
    model: str = "gemini-3.8-flash"
    mailbox: str = ""
    repository: str = "M-Abdullah07/Bugproof"
    oauth_path: Path = Path(".data/fastn-oauth.json")
    oauth_json: str = field(default="", repr=False)
    lab_secret: str = field(default="", repr=False)
    approval_seconds: int = 900

    def __post_init__(self):
        if len(self.demo_password) < 12:
            raise ValueError("Configure BUGPROOF_DEMO_PASSWORD with at least 12 characters")
        if len(self.session_secret) < 32:
            raise ValueError("Configure BUGPROOF_SESSION_SECRET with at least 32 characters")
        if not 1 <= self.port <= 65535:
            raise ValueError("PORT must be between 1 and 65535")

    @classmethod
    def from_environment(cls):
        values = {**dotenv_values(".env"), **os.environ}
        return cls(
            demo_password=values.get("BUGPROOF_DEMO_PASSWORD") or "",
            session_secret=values.get("BUGPROOF_SESSION_SECRET") or "",
            database_path=Path(values.get("BUGPROOF_DATABASE_PATH") or ".data/bugproof.sqlite3"),
            build_ref=values.get("BUGPROOF_BUILD_REF") or "development",
            secure_cookies=values.get("BUGPROOF_ENV") == "production",
            port=int(values.get("PORT") or 8000),
            gemini_key=values.get("GEMINI_API_KEY") or "",
            model=values.get("BUGPROOF_MODEL") or "gemini-3.8-flash",
            mailbox=values.get("BUGPROOF_MAILBOX") or "",
            repository=values.get("BUGPROOF_REPOSITORY") or "M-Abdullah07/Bugproof",
            oauth_path=Path(values.get("BUGPROOF_FASTN_OAUTH_PATH") or ".data/fastn-oauth.json"),
            oauth_json=values.get("BUGPROOF_FASTN_OAUTH_JSON") or "",
            lab_secret=values.get("BUGPROOF_LAB_SECRET") or values.get("BUGPROOF_SESSION_SECRET") or "",
        )
