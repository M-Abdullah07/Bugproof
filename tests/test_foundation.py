import sqlite3
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from bugproof.config import Settings
from bugproof.web import create_app


@pytest.fixture
def settings(tmp_path):
    return Settings(
        demo_password="test-password-for-local-tests",
        session_secret="test-session-secret-at-least-32-characters",
        database_path=tmp_path / "test.sqlite3",
        build_ref="foundation-test",
    )


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings)) as value:
        yield value


def csrf(client):
    page = client.get("/login")
    return page.text.split('name="csrf_token" value="')[1].split('"')[0]


def login(client, settings):
    return client.post(
        "/login",
        data={"password": settings.demo_password, "csrf_token": csrf(client)},
        follow_redirects=False,
    )


def test_health_reports_observed_build_and_live_storage(client, settings):
    assert client.get("/healthz").json() == {
        "status": "ok", "build": "foundation-test", "storage": "ready"
    }
    with sqlite3.connect(settings.database_path) as connection:
        connection.execute("DROP TABLE schema_version")
    assert client.get("/healthz").status_code == 503


def test_private_pages_and_api_require_authentication(client):
    assert client.get("/cases", follow_redirects=False).status_code == 303
    assert client.get("/api/cases").status_code == 401


def test_wrong_password_and_missing_csrf_never_authenticate(client):
    assert client.post("/login", data={"password": "wrong"}).status_code == 403
    response = client.post(
        "/login", data={"password": "wrong", "csrf_token": csrf(client)}
    )
    assert response.status_code == 401
    assert client.get("/api/cases").status_code == 401


def test_login_shows_honest_empty_workspace_and_logout_revokes_access(client, settings):
    assert login(client, settings).status_code == 303
    page = client.get("/cases")
    assert page.status_code == 200
    assert "No reports imported yet" in page.text
    assert "not connected" in page.text
    assert client.get("/api/cases").json() == {"cases": []}
    assert client.post("/logout", data={"csrf_token": "tampered"}).status_code == 403
    token = page.text.split('name="csrf_token" value="')[1].split('"')[0]
    assert client.post("/logout", data={"csrf_token": token}, follow_redirects=False).status_code == 303
    assert client.get("/api/cases").status_code == 401


def test_database_identity_and_case_state_survive_application_restart(settings):
    with TestClient(create_app(settings)) as first:
        login(first, settings)
        with sqlite3.connect(settings.database_path) as connection:
            installation_id = connection.execute(
                "SELECT value FROM app_metadata WHERE key='installation_id'"
            ).fetchone()[0]
            connection.execute(
                "INSERT INTO cases(id, mailbox_id, thread_id, source_revision, source_json, created_at) "
                "VALUES ('case-1','test-mailbox','test-thread',1,'{}','2026-10-17T00:00:00Z')"
            )
    with TestClient(create_app(settings)) as second:
        login(second, settings)
        assert second.get("/api/cases").json()["cases"][0]["id"] == "case-1"
        with sqlite3.connect(settings.database_path) as connection:
            assert connection.execute(
                "SELECT value FROM app_metadata WHERE key='installation_id'"
            ).fetchone()[0] == installation_id


def test_configuration_fails_without_operator_secrets():
    with pytest.raises(ValueError, match="BUGPROOF_DEMO_PASSWORD"):
        Settings(demo_password="", session_secret="x" * 32)
    with pytest.raises(ValueError, match="BUGPROOF_SESSION_SECRET"):
        Settings(demo_password="safe-test-password", session_secret="short")


def test_production_session_is_secure_and_not_sent_over_plain_http(settings):
    with TestClient(create_app(replace(settings, secure_cookies=True)), base_url="https://testserver") as client:
        response = login(client, settings)
        cookie = response.headers["set-cookie"].lower()
        assert "secure" in cookie and "httponly" in cookie and "samesite=lax" in cookie
        assert client.get("/api/cases").status_code == 200
        assert client.get("http://testserver/api/cases").status_code == 401
