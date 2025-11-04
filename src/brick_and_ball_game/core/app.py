from abc import ABC, abstractmethod

from pyray import (
    begin_drawing,
    Color,
    clear_background,
    close_window,
    draw_fps,
    end_drawing,
    get_frame_time,
    init_window,
    KeyboardKey,
    set_exit_key,
    set_target_fps,
    window_should_close,
)

from brick_and_ball_game.core.game_state import StateManager
from brick_and_ball_game.core.sound_manager import SoundManager
from brick_and_ball_game.core.texture_manager import TextureManager


DRAW_FPS: bool = True
TARGET_FPS: int = 165


class App(ABC):
    window_width: int
    window_height: int
    state_manager: StateManager
    sound_manager: SoundManager
    texture_manager: TextureManager

    def __init__(self, window_width: int, window_height: int, title: str) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.window_title = title
        self.sound_manager = SoundManager()
        self.texture_manager = TextureManager()
        self.state_manager = StateManager(self.sound_manager, self.texture_manager)

    @abstractmethod
    def on_init(self) -> None:
        raise NotImplementedError

    def _update(self, delta_time: float) -> None:
        self.state_manager.update(delta_time)

    def _draw(self) -> None:
        begin_drawing()
        clear_background(Color(0, 0, 0, 255))
        self.state_manager.draw()
        if DRAW_FPS:
            draw_fps(self.window_width - 85, 5)
        end_drawing()

    def _load(self) -> None:
        init_window(self.window_width, self.window_height, self.window_title)
        set_target_fps(TARGET_FPS)
        self.sound_manager.initialize()
        self.texture_manager.initialize()
        set_exit_key(KeyboardKey.KEY_NULL)
        self.on_init()

    def _unload(self) -> None:
        self.state_manager.unload()
        self.sound_manager.unload()
        self.texture_manager.unload()
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
