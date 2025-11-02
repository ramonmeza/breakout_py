from pyray import (
    begin_drawing,
    BLACK,
    clear_background,
    close_window,
    end_drawing,
    get_frame_time,
    init_window,
    window_should_close,
)

from brick_and_ball_game.core.game_state import GameState


class App:
    window_width: int
    window_height: int
    game: GameState

    def __init__(
        self, window_width: int, window_height: int, title: str, game: GameState
    ) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.window_title = title
        self.game = game

    def _update(self, delta_time: float) -> None:
        self.game.update(delta_time)

    def _draw(self) -> None:
        begin_drawing()
        clear_background(BLACK)
        self.game.draw()
        end_drawing()

    def _load(self) -> None:
        init_window(self.window_width, self.window_height, self.window_title)
        self.game.load()

    def _unload(self) -> None:
        self.game.unload()
        close_window()

    def run(self) -> None:
        self._load()
        try:
            while not window_should_close():
                self._update(delta_time=get_frame_time())
                self._draw()
        finally:
            self._unload()
