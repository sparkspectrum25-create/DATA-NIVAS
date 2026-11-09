"""ULTRON stays dormant. He only wakes on an exact phrase, and stays idle otherwise."""

from .base import Agent
from ..state import State

WAKE_PHRASE = "wake up, ultron"


class Ultron(Agent):
    name = "ultron"
    description = "Dormant. Wakes only on the exact wake phrase."

    def handle(self, text: str, consent: bool, state: State) -> dict:
        cmd = text.strip().lower()
        if not state.ultron_awake:
            if cmd == WAKE_PHRASE:
                state.ultron_awake = True
                return {"agent": self.name, "status": "awake"}
            return {"agent": self.name, "status": "dormant"}
        if cmd == "sleep":
            state.ultron_awake = False
            return {"agent": self.name, "status": "dormant"}
        return {"agent": self.name, "status": "awake", "note": "standing by"}
