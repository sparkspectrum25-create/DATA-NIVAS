from .base import Agent
from .consent_agents import Location, Vision
from .dume import DumE
from .edith import Edith
from .friday import Friday
from .jarvis import Jarvis
from .ultron import Ultron

AGENTS: dict[str, Agent] = {
    a.name: a
    for a in [Jarvis(), Friday(), Edith(), DumE(), Vision(), Location(), Ultron()]
}
