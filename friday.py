from .base import Agent
from ..state import State


class Friday(Agent):
    name = "friday"
    description = "Device management: lists registered devices and their last status"

    def handle(self, text: str, consent: bool, state: State) -> dict:
        return {
            "agent": self.name,
            "devices": [
                {"device_id": d_id, "name": d["name"], "last_status": d.get("status", {})}
                for d_id, d in state.devices.items()
            ],
        }
