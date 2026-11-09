from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from .agents.dume import cleanup_plan
from .agents.edith import audit_permissions
from .agents.registry import AGENTS
from .auth import require_token
from .state import state

app = FastAPI(title="FRIDAY server", version="0.2.0")


class Command(BaseModel):
    agent: str
    text: str = ""
    consent: bool = False


class DeviceRegister(BaseModel):
    device_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=100)


class Heartbeat(BaseModel):
    battery: int | None = Field(default=None, ge=0, le=100)
    notes: str | None = Field(default=None, max_length=300)


class PermissionReport(BaseModel):
    device_id: str
    permissions: list[str] = Field(max_length=500)


class StorageReport(BaseModel):
    free_mb: int = Field(ge=0)
    cache_mb: int = Field(ge=0)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/agents", dependencies=[Depends(require_token)])
def list_agents():
    return {name: a.description for name, a in AGENTS.items()}


@app.post("/command", dependencies=[Depends(require_token)])
def command(cmd: Command):
    agent = AGENTS.get(cmd.agent)
    if agent is None:
        raise HTTPException(status_code=404, detail="unknown agent")
    return agent.handle(cmd.text, cmd.consent, state)


@app.post("/devices/register", dependencies=[Depends(require_token)])
def register_device(body: DeviceRegister):
    state.devices[body.device_id] = {"name": body.name, "status": {}}
    return {"device_id": body.device_id, "registered": True}


@app.post("/devices/{device_id}/heartbeat", dependencies=[Depends(require_token)])
def heartbeat(device_id: str, body: Heartbeat):
    device = state.devices.get(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="device not registered")
    device["status"] = body.model_dump(exclude_none=True)
    return {"device_id": device_id, "ok": True}


@app.post("/audit/permissions", dependencies=[Depends(require_token)])
def audit(body: PermissionReport):
    if body.device_id not in state.devices:
        raise HTTPException(status_code=404, detail="device not registered")
    return {"device_id": body.device_id, **audit_permissions(body.permissions)}


@app.post("/repair/plan", dependencies=[Depends(require_token)])
def repair_plan(body: StorageReport):
    return cleanup_plan(body.free_mb, body.cache_mb)
