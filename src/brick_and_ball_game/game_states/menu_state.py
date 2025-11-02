from __future__ import annotations
from typing import override

from pyray import (
    draw_text,
    KeyboardKey,
    measure_text,
    Rectangle,
    WHITE,
    YELLOW,
)

from brick_and_ball_game.core.game_state import GameState
from brick_and_ball_game.components.player_input_component import PlayerInputComponent
from brick_and_ball_game.game_states.gameplay_state import GameplayState


class MenuState(GameState):
    bounds: Rectangle
    menu: list[str]
    player_input: PlayerInputComponent

    @override
    def load(self) -> None:
        self.bounds = Rectangle(0, 0, 800, 600)
        self.player_input = PlayerInputComponent()
        self.player_input.add_button("Up", KeyboardKey.KEY_UP)
        self.player_input.add_button("Down", KeyboardKey.KEY_DOWN)
        self.player_input.add_button("Select", KeyboardKey.KEY_ENTER)
        self.menu = [
            "Play",
            "Quit"
        ]
        self.selected_option = 0

    @override
    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        if self.player_input.is_button_pressed("Up"):
            self.selected_option = (self.selected_option + 1) % len(self.menu)
        elif self.player_input.is_button_pressed("Down"):
            self.selected_option = (self.selected_option - 1) % len(self.menu)

        if self.player_input.is_button_pressed("Select"):
            key: str = self.menu[self.selected_option]
            match self.selected_option:
                case 0:
                    # play
                    self.state_manager.push(GameplayState(self.state_manager))
                case _:
                    self.state_manager.pop()

    def draw(self) -> None:
        font_size: int = 30
        cur_y: int = 100
        for i, text in enumerate(self.menu):
            width: int = measure_text(text, font_size)
            cur_x: int = int((self.bounds.width / 2) + (width / 2))
            draw_text(
                text,
                cur_x,
                cur_y,
                font_size,
                YELLOW if i == self.selected_option else WHITE,
            )
            cur_y += font_size + 10  # vertical padding
