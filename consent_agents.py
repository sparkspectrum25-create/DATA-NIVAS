"""Vision and Location only act when the caller sets consent=true on the command.
Analyzers are not wired up yet, so they only confirm that consent was given."""

from .base import Agent
from ..state import State


class Vision(Agent):
    name = "vision"
    description = "Camera-based vision help (requires consent=true on each request)"

    def handle(self, text: str, consent: bool, state: State) -> dict:
        if not consent:
            return {"agent": self.name, "status": "consent_required"}
        return {"agent": self.name, "status": "accepted", "note": "no vision analyzer configured yet"}


class Location(Agent):
    name = "location"
    description = "Location-aware context (requires consent=true on each request)"

    def handle(self, text: str, consent: bool, state: State) -> dict:
        if not consent:
            return {"agent": self.name, "status": "consent_required"}
        return {"agent": self.name, "status": "accepted", "note": "no location provider configured yet"}
