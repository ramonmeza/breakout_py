from typing import override

from brick_and_ball_game.game_states.menu_state import MenuState
from brick_and_ball_game.game_states.gameplay import GameplayState


class MainMenu(MenuState):
    def __init__(self) -> None:
        super().__init__(["Play", "Quit"])

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
                self.state_manager.pop()  # pop pause menu
            case _:
                self.state_manager.pop()  # pop pause menu
                self.state_manager.pop()  # pop gameplay
