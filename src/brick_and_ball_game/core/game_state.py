from __future__ import annotations
from abc import ABC, abstractmethod

from brick_and_ball_game.core.sound_manager import SoundManager
from brick_and_ball_game.core.texture_manager import TextureManager


class GameState(ABC):
    state_manager: StateManager
    """Set by StateManager.push()"""

    sound_manager: SoundManager
    """Set by StateManager.push()"""

    texture_manager: TextureManager
    """Set by StateManager.push()"""

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
    sound_manager: SoundManager
    texture_manager: TextureManager

    def __init__(self, sound_manager: SoundManager, texture_manager: TextureManager) -> None:
        self.states = []
        self.sound_manager = sound_manager
        self.texture_manager = texture_manager

    def __getitem__(self, idx: int) -> GameState:
        return self.states[idx]

    def push(self, state: GameState) -> None:
        state.sound_manager = (
            self.sound_manager
        )  # allow access to SoundManager for GameState
        state.texture_manager = (
            self.texture_manager
        )  # allow access to TextureManager for GameState
        state.state_manager = self  # allow access to StateManager for GameState
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
