from __future__ import annotations
from typing import override

from pyray import (
    check_collision_recs,
    GREEN,
    Rectangle,
    Vector2,
    vector2_normalize,
    WHITE,
)

from brick_and_ball_game.core.game_state import GameState
from brick_and_ball_game.game_objects import Ball, BrickGrid, Paddle


class GameplayState(GameState):
    play_bounds: Rectangle
    paddle: Paddle
    balls: list[Ball]
    bricks: BrickGrid
    player_lives: int

    @override
    def load(self) -> None:
        self.player_lives = 3
        self.play_bounds = Rectangle(0, 0, 800, 600)
        paddle_width: int = 75
        paddle_height: int = 10
        paddle_dist_from_bottom: int = 100
        paddle_x: float = (self.play_bounds.width / 2) - (paddle_width / 2)
        paddle_y: float = self.play_bounds.height - paddle_dist_from_bottom
        self.paddle = Paddle(
            bounding_box=Rectangle(paddle_x, paddle_y, paddle_width, paddle_height),
            color=GREEN,
            bounds=self.play_bounds,
            speed=350.0,
        )
        self.balls = [
            Ball(
                speed=250.0,
                position=Vector2((self.play_bounds.width / 2), (paddle_y - 50)),
                radius=5.0,
                color=WHITE,
                velocity=Vector2(0.0, -1.0),
            ),
        ]
        self.bricks = BrickGrid(6, 9, Rectangle(0, 50, self.play_bounds.width, 150))

    @override
    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        self.paddle.update(delta_time)
        for ball in self.balls:
            ball.update(delta_time)
            self.handle_ball_walls(ball)
            self.handle_ball_bricks(ball)
            self.handle_ball_paddle(ball)

    def handle_ball_walls(self, ball: Ball) -> None:
        # left
        if ball.position.x - ball.radius < self.play_bounds.x:
            ball.velocity.x *= -1
            ball.position.x = self.play_bounds.x + ball.radius

        # right
        if ball.position.x + ball.radius > self.play_bounds.x + self.play_bounds.width:
            ball.velocity.x *= -1
            ball.position.x = self.play_bounds.x + self.play_bounds.width - ball.radius

        # top
        if ball.position.y - ball.radius < self.play_bounds.y:
            ball.velocity.y *= -1
            ball.position.y = self.play_bounds.y + ball.radius

        # bottom
        if ball.position.y + ball.radius > self.play_bounds.y + self.play_bounds.height:
            ball.velocity.y *= -1
            ball.position.y = self.play_bounds.y + self.play_bounds.height - ball.radius

    def handle_ball_bricks(self, ball: Ball) -> None:
        ball_coll: Rectangle = Rectangle(
            ball.position.x, ball.position.y, ball.radius * 2, ball.radius * 2
        )
        bricks_coll: Rectangle = self.bricks.bounding_box
        if check_collision_recs(ball_coll, bricks_coll):
            brick_index = self.bricks.get_brick_index_at(
                ball.position.x, ball.position.y
            )
            if brick_index is not None:
                brick = self.bricks.bricks[brick_index]
                if brick.hit_count > 0:
                    # calculate the rectangle for this brick
                    row = brick_index // self.bricks.cols
                    col = brick_index % self.bricks.cols
                    brick_rect = Rectangle(
                        self.bricks.bounding_box.x + col * self.bricks.brick_width,
                        self.bricks.bounding_box.y + row * self.bricks.brick_height,
                        self.bricks.brick_width,
                        self.bricks.brick_height,
                    )

                    if ball.bounce_off(brick_rect):
                        brick.hit_count -= 1

    def handle_ball_paddle(self, ball: Ball) -> None:
        if ball.bounce_off(self.paddle.bounding_box):
            # ball bounce trajectory based on ball distance from center
            offset: float = (
                ball.position.x
                - (self.paddle.bounding_box.x + self.paddle.bounding_box.width / 2)
            ) / (self.paddle.bounding_box.width / 2)
            offset = max(-1.0, min(1.0, offset))
            ball_dir: Vector2 = Vector2(offset, ball.velocity.y)
            ball_dir = vector2_normalize(ball_dir)
            ball.velocity.x = ball_dir.x
            ball.velocity.y = ball_dir.y

    def draw(self) -> None:
        self.bricks.draw()
        for ball in self.balls:
            ball.draw()
        self.paddle.draw()
