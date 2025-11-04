from typing import override

from pyray import Color, draw_text

from brick_and_ball_game.game_states.menu_state import MenuState
from brick_and_ball_game.game_states.gameplay import GameplayState


class MainMenu(MenuState):
    def __init__(self) -> None:
        super().__init__(["Play", "Quit"])

    def load(self) -> None:
        super().load()
        self.sound_manager.load_bgm(
            "Main Menu",
            r"assets\bgm\DavidKBD - Pink Bloom Pack - 01 - Pink Bloom.ogg",
            volume=0.75,
        )
        self.sound_manager.play_bgm("Main Menu")

    @override
    def select(self, selected_option: int) -> None:
        match selected_option:
            case 0:
                # play
                self.state_manager.push(GameplayState())  # push gameplay
            case _:
                # quit
                self.state_manager.pop()  # pop main main (empty states = quit)


class PauseMenu(MenuState):
    def __init__(self) -> None:
        super().__init__(["Resume", "Main Menu"])

    @override
    def select(self, selected_option: int) -> None:
        match selected_option:
            case 0:
                # resume
                self.state_manager.pop(resume=True)  # pop pause menu

            case _:
                self.state_manager.pop()  # pop pause menu
                self.state_manager.pop()  # pop gameplay


class GameOverMenu(MenuState):
    has_won: bool
    score: int

    def __init__(self, has_won: bool, score: int) -> None:
        super().__init__(["Continue" if has_won else "Try Again", "Main Menu"])
        self.has_won = has_won
        self.score = score

    @override
    def select(self, selected_option: int) -> None:
        match selected_option:
            case 0:
                self.state_manager.pop()  # pop game over menu
                if self.has_won:
                    # continue
                    self.state_manager.pop()  # pop gameplay
                    # todo: push next level
                else:
                    # try again
                    self.state_manager[-1].unload()
                    self.state_manager[-1].load()

            case _:
                # goto main menu
                self.state_manager.pop()  # pop gameover menu
                self.state_manager.pop()  # pop gameplay

    @override
    def draw(self) -> None:
        if self.has_won:
            draw_text("You Win!", 0, 0, 40, Color(255, 255, 255, 255))
            draw_text(f"Score: {self.score}", 0, 40, 30, Color(255, 255, 255, 255))
        else:
            draw_text("You lose.", 0, 0, 40, Color(255, 255, 255, 255))

        super().draw()
