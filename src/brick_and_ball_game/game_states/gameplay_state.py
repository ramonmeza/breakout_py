from typing import override

from pyray import Rectangle, Vector2, vector2_normalize
from pyray import (BLUE, GREEN)

from brick_and_ball_game.core.game_state import GameState
from brick_and_ball_game.game_objects import Ball, Paddle


class GameplayState(GameState):
    play_bounds: Rectangle
    paddle: Paddle
    balls: list[Ball]

    @override
    def load(self) -> None:
        self.play_bounds = Rectangle(0, 0, 800, 600)

        paddle_width: int = 75
        paddle_height: int = 10
        paddle_dist_from_bottom: int = 100

        paddle_x: float = (self.play_bounds.width / 2) - (paddle_width / 2)
        paddle_y: float = self.play_bounds.height - paddle_dist_from_bottom

        self.paddle = Paddle(
            bounding_box=Rectangle(
                paddle_x,
                paddle_y,
                paddle_width,
                paddle_height
            ),
            color=GREEN,
            bounds=self.play_bounds,
            speed=350.0
        )
        self.balls = [
            Ball(
                speed=250.0,
                position=Vector2(10, 10),
                radius=5.0,
                color=BLUE,
                bounds=self.play_bounds,
                velocity=Vector2(1.0, 1.0)
            ),
        ]

    @override
    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.paddle.update(delta_time)
        for ball in self.balls:
            ball.update(delta_time)
            if ball.bounce_off(self.paddle.bounding_box):
                # ball bounce trajectory based on ball distance from center
                offset: float = (ball.position.x - (self.paddle.bounding_box.x + self.paddle.bounding_box.width / 2)) / (self.paddle.bounding_box.width / 2)
                offset = max(-1.0, min(1.0, offset))
                ball_dir: Vector2 = Vector2(offset, ball.velocity.y)
                ball_dir = vector2_normalize(ball_dir)
                ball.velocity.x = ball_dir.x
                ball.velocity.y = ball_dir.y

    def draw(self) -> None:
        self.paddle.draw()
        for ball in self.balls:
            ball.draw()
