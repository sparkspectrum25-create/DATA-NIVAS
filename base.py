from abc import ABC, abstractmethod

from ..state import State


class Agent(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    def handle(self, text: str, consent: bool, state: State) -> dict:
        """Handle a text command. Must never perform destructive actions on its own."""
