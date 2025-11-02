from abc import ABC, abstractmethod

from pyray import (
    begin_drawing,
    BLACK,
    clear_background,
    close_window,
    end_drawing,
    get_frame_time,
    init_window,
    KeyboardKey,
    set_exit_key,
    window_should_close,
)

from brick_and_ball_game.core.game_state import StateManager


class App(ABC):
    window_width: int
    window_height: int
    state_manager: StateManager

    def __init__(self, window_width: int, window_height: int, title: str) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.window_title = title
        self.state_manager = StateManager()

    @abstractmethod
    def on_init(self) -> None:
        raise NotImplementedError

    def _update(self, delta_time: float) -> None:
        self.state_manager.update(delta_time)

    def _draw(self) -> None:
        begin_drawing()
        clear_background(BLACK)
        self.state_manager.draw()
        end_drawing()

    def _load(self) -> None:
        init_window(self.window_width, self.window_height, self.window_title)
        set_exit_key(KeyboardKey.KEY_NULL)
        self.on_init()

    def _unload(self) -> None:
        self.state_manager.unload()
        close_window()

    def run(self) -> None:
        self._load()
        try:
            while not window_should_close():
                if self.state_manager.is_empty():
                    break
                self._update(delta_time=get_frame_time())
                self._draw()
        finally:
            self._unload()
