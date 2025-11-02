from brick_and_ball_game.brick_game import BrickGame


def main() -> int:
    app: BrickGame = BrickGame(800, 600, "Brick & Ball!")
    app.run()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
