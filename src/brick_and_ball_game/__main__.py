from brick_and_ball_game.core import App
from brick_and_ball_game.game_states import GameplayState


def main() -> int:
    app: App = App(800, 600, "Brick & Ball!", GameplayState())
    app.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
