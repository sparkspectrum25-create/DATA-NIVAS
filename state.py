import time


class State:
    """In-memory state. Swap for a database before running this for real."""

    def __init__(self) -> None:
        self.started = time.time()
        self.devices: dict[str, dict] = {}
        self.ultron_awake = False


state = State()
