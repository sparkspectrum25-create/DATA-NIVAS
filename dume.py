"""DUM-E: suggests cleanup steps. It only returns a plan. The device runs the steps
through its own allowed APIs, and the server never deletes anything itself."""

from .base import Agent
from ..state import State


def cleanup_plan(free_mb: int, cache_mb: int) -> dict:
    steps = []
    if cache_mb >= 500:
        steps.append({"action": "clear_app_cache", "reason": f"{cache_mb} MB cache"})
    if free_mb < 2048:
        steps.append({"action": "review_large_files", "reason": f"only {free_mb} MB free"})
    if not steps:
        steps.append({"action": "none", "reason": "storage looks healthy"})
    return {"steps": steps}


class DumE(Agent):
    name = "dum-e"
    description = "Cleanup suggestions (send storage report to /repair/plan)"

    def handle(self, text: str, consent: bool, state: State) -> dict:
        return {"agent": self.name, "note": "Send storage numbers to /repair/plan."}
