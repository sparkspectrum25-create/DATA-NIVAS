import os

os.environ["FRIDAY_TOKEN"] = "test-token"

from fastapi.testclient import TestClient  # noqa: E402

from app.config import settings  # noqa: E402
from app.main import app  # noqa: E402
from app.state import state  # noqa: E402

client = TestClient(app)
H = {"Authorization": "Bearer test-token"}


def setup_function():
    state.devices.clear()
    state.ultron_awake = False


def test_health_is_open():
    assert client.get("/health").json() == {"ok": True}


def test_protected_route_rejects_missing_token():
    assert client.get("/agents").status_code == 401


def test_fails_closed_without_server_token(monkeypatch):
    monkeypatch.setattr(settings, "token", "")
    assert client.get("/agents", headers=H).status_code == 503


def test_vision_requires_consent():
    r = client.post("/command", json={"agent": "vision", "text": "look"}, headers=H)
    assert r.json()["status"] == "consent_required"


def test_ultron_stays_dormant_without_wake_phrase():
    r = client.post("/command", json={"agent": "ultron", "text": "hello"}, headers=H)
    assert r.json()["status"] == "dormant"


def test_ultron_wakes_on_exact_phrase():
    r = client.post("/command", json={"agent": "ultron", "text": "Wake up, ultron"}, headers=H)
    assert r.json()["status"] == "awake"


def test_device_register_heartbeat_and_list():
    client.post("/devices/register", json={"device_id": "d1", "name": "phone"}, headers=H)
    client.post("/devices/d1/heartbeat", json={"battery": 80}, headers=H)
    r = client.post("/command", json={"agent": "friday"}, headers=H).json()
    assert r["devices"][0]["last_status"] == {"battery": 80}


def test_edith_flags_risky_permissions():
    client.post("/devices/register", json={"device_id": "d1", "name": "phone"}, headers=H)
    r = client.post(
        "/audit/permissions",
        json={"device_id": "d1", "permissions": ["android.permission.CAMERA"]},
        headers=H,
    ).json()
    assert r["overall_risk"] == "high"


def test_dume_plans_but_does_not_act():
    r = client.post("/repair/plan", json={"free_mb": 1000, "cache_mb": 900}, headers=H).json()
    actions = [s["action"] for s in r["steps"]]
    assert "clear_app_cache" in actions
