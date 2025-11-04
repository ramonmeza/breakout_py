from __future__ import annotations
from abc import abstractmethod
from typing import override

from pyray import (
    Color,
    draw_text,
    KeyboardKey,
    measure_text,
    Rectangle,
)

from brick_and_ball_game.core.game_state import GameState
from brick_and_ball_game.components.player_input_component import PlayerInputComponent


class MenuState(GameState):
    bounds: Rectangle
    menu_items: list[str]
    current_selected_i: int
    player_input: PlayerInputComponent

    def __init__(self, menu_items: list[str]) -> None:
        super().__init__()
        self.menu_items = menu_items

    @override
    def load(self) -> None:
        self.bounds = Rectangle(0, 0, 800, 600)
        self.player_input = PlayerInputComponent()
        self.player_input.add_button("Up", KeyboardKey.KEY_UP)
        self.player_input.add_button("Down", KeyboardKey.KEY_DOWN)
        self.player_input.add_button("Select", KeyboardKey.KEY_ENTER)
        self.current_selected_i = 0
        self.sound_manager.load_sfx("Click", r"assets\sfx\switch4.ogg", volume=0.5)
        self.sound_manager.load_sfx("Clack", r"assets\sfx\switch5.ogg", volume=0.5)
        self.sound_manager.load_sfx("Select", r"assets\sfx\switch31.ogg", volume=0.5)

    @override
    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        if self.player_input.is_button_pressed("Up"):
            self.current_selected_i = (self.current_selected_i + 1) % len(
                self.menu_items
            )
            self.sound_manager.play_sfx("Click")
        elif self.player_input.is_button_pressed("Down"):
            self.current_selected_i = (self.current_selected_i - 1) % len(
                self.menu_items
            )
            self.sound_manager.play_sfx("Clack")

        if self.player_input.is_button_pressed("Select"):
            self.sound_manager.play_sfx("Select")
            self.select(self.current_selected_i)

    def draw(self) -> None:
        font_size: int = 30
        vpadding: int = 10
        cur_y: int = int(
            self.bounds.y
            + (self.bounds.height / 2)
            - (
                ((len(self.menu_items) * font_size) + (len(self.menu_items) * vpadding))
                / 2
            )
        )
        for i, text in enumerate(self.menu_items):
            text_width: int = measure_text(text, font_size)
            cur_x: int = int(self.bounds.x + (self.bounds.width / 2) - (text_width / 2))
            draw_text(
                text,
                cur_x,
                cur_y,
                font_size,
                (
                    Color(255, 255, 0, 255)
                    if i == self.current_selected_i
                    else Color(255, 255, 255, 255)
                ),
            )
            cur_y += font_size + vpadding

    @abstractmethod
    def select(self, selected_option: int) -> None:
        raise NotImplementedError
