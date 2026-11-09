"""EDITH: defensive audit of your own devices. Reads the permission list a device reports
and flags the risky ones. It does not scan other people's devices or networks."""

from .base import Agent
from ..state import State

RISKY = {
    "CAMERA": "high",
    "RECORD_AUDIO": "high",
    "ACCESS_FINE_LOCATION": "high",
    "READ_SMS": "high",
    "READ_CONTACTS": "medium",
    "READ_CALL_LOG": "medium",
    "POST_NOTIFICATIONS": "low",
}


def audit_permissions(permissions: list[str]) -> dict:
    findings = []
    for p in sorted(set(permissions)):
        short = p.split(".")[-1]
        if short in RISKY:
            findings.append({"permission": short, "risk": RISKY[short]})
    level = "high" if any(f["risk"] == "high" for f in findings) else (
        "medium" if findings else "low"
    )
    return {"overall_risk": level, "findings": findings}


class Edith(Agent):
    name = "edith"
    description = "Defensive audit of your own devices (send permissions to /audit/permissions)"

    def handle(self, text: str, consent: bool, state: State) -> dict:
        return {"agent": self.name, "note": "Send a permission list to /audit/permissions."}
