from brick_and_ball_game.core.app import App

from brick_and_ball_game.game_states.menus import MainMenu


class BrickGame(App):
    def on_init(self) -> None:
        self.state_manager.push(MainMenu())
