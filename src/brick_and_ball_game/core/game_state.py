from __future__ import annotations
from abc import ABC, abstractmethod


class GameState(ABC):
    state_manager: StateManager

    def __init__(self, state_manager: StateManager) -> None:
        super().__init__()
        self.state_manager = state_manager

    def load(self) -> None:
        pass

    def unload(self) -> None:
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError


class StateManager:
    states: list[GameState]

    def __init__(self) -> None:
        self.states = []

    def push(self, state: GameState) -> None:
        # unload previous state
        if not self.is_empty():
            self.states[-1].unload()

        self.states.append(state)
        self.states[-1].load()

    def pop(self) -> GameState | None:
        if not self.is_empty():
            state: GameState = self.states.pop()
            state.unload()
            return state
        return None

    def update(self, delta_time: float) -> None:
        if not self.is_empty():
            self.states[-1].update(delta_time)
        
    def draw(self) -> None:
        if not self.is_empty():
            self.states[-1].draw()

    def unload(self) -> None:
        while not self.is_empty():
            self.pop()

    def is_empty(self) -> bool:
        return len(self.states) == 0
