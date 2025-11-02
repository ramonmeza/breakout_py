from __future__ import annotations
from typing import Callable, override

from pyray import (
    close_window,
    draw_text,
    KeyboardKey,
    measure_text,
    Rectangle,
    WHITE,
    YELLOW,
)

from brick_and_ball_game.core import GameState
from brick_and_ball_game.components import PlayerInputComponent


class MenuState(GameState):
    bounds: Rectangle
    menu: dict[str, Callable[[], None]]
    player_input: PlayerInputComponent

    @override
    def load(self) -> None:
        self.bounds = Rectangle(0, 0, 800, 600)
        self.player_input = PlayerInputComponent()
        self.player_input.add_button("Up", KeyboardKey.KEY_UP)
        self.player_input.add_button("Down", KeyboardKey.KEY_DOWN)
        self.player_input.add_button("Select", KeyboardKey.KEY_ENTER)
        self.menu = {
            "Play": lambda: print("play"),
            "Quit": close_window,
        }
        self.selected_option = 0

    @override
    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        if self.player_input.is_button_pressed("Up"):
            self.selected_option = (self.selected_option + 1) % len(self.menu.keys())
        elif self.player_input.is_button_pressed("Down"):
            self.selected_option = (self.selected_option - 1) % len(self.menu.keys())

        if self.player_input.is_button_pressed("Select"):
            key: str = list(self.menu.keys())[self.selected_option]
            print(key)

    def draw(self) -> None:
        font_size: int = 30
        cur_y: int = 100
        for i, menu_opt in enumerate(self.menu.keys()):
            width: int = measure_text(menu_opt, font_size)
            cur_x: int = int((self.bounds.width / 2) + (width / 2))
            draw_text(
                menu_opt,
                cur_x,
                cur_y,
                font_size,
                YELLOW if i == self.selected_option else WHITE,
            )
            cur_y += font_size + 10  # vertical padding
