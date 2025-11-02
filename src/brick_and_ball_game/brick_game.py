from brick_and_ball_game.core.app import App

from brick_and_ball_game.game_states.gameplay_state import GameplayState
from brick_and_ball_game.game_states.menu_state import MenuState


class BrickGame(App):
    def on_init(self) -> None:
        self.state_manager.push(MenuState(self.state_manager))
