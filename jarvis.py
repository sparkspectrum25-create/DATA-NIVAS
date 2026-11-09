import time

from .base import Agent
from ..state import State


class Jarvis(Agent):
    name = "jarvis"
    description = "Server status and health overview"

    def handle(self, text: str, consent: bool, state: State) -> dict:
        return {
            "agent": self.name,
            "uptime_seconds": int(time.time() - state.started),
            "devices_registered": len(state.devices),
            "ultron": "awake" if state.ultron_awake else "dormant",
        }
