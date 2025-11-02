from __future__ import annotations
from typing import override

from pyray import (
    check_collision_recs,
    draw_text,
    GREEN,
    measure_text,
    Rectangle,
    Vector2,
    vector2_normalize,
    WHITE,
)

from brick_and_ball_game.core.game_state import GameState
from brick_and_ball_game.game_objects import Ball, BrickGrid, Paddle


class HUD:
    def draw(self, lives: int, score: int) -> None:
        draw_text(f"LIVES: {lives}", 10, 10, 20, WHITE)
        draw_text(f"SCORE: {score}", 10, 40, 20, WHITE)


class GameplayState(GameState):
    play_bounds: Rectangle
    paddle: Paddle
    balls: list[Ball]
    bricks: BrickGrid
    hud: HUD

    has_won: bool
    has_lost: bool
    is_playing: bool
    player_lives: int
    ball_hit_bottom: bool
    score: int

    @override
    def load(self) -> None:
        self.score = 0
        self.hud = HUD()
        self.has_won = False
        self.has_lost = False
        self.is_playing = True
        self.player_lives = 3
        self.ball_hit_bottom = False

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
        self.bricks = BrickGrid(
            rows=4,
            cols=5,
            bounding_box=Rectangle(0, 50, self.play_bounds.width, 150)
        )

    @override
    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        should_respawn: bool = False
        if self.is_playing:
            self.paddle.update(delta_time)
            for ball in self.balls:
                ball.update(delta_time)
                self.handle_ball_walls(ball)
                self.handle_ball_bricks(ball)
                self.handle_ball_paddle(ball)

                # if ball hit bottom, make it inactive
                if self.ball_hit_bottom:
                    self.ball_hit_bottom = False
                    ball.active = False

            # if all balls are inactive
            if not any(ball.active for ball in self.balls):
                self.player_life_lost()
                should_respawn = True

        # win condition
        if self.bricks.are_all_bricks_destroyed():
            self.win(delta_time)
            should_respawn = False

        # game over condition
        if self.player_lives <= 0:
            self.lose(delta_time)
            should_respawn = False

        if should_respawn:
            self.respawn()

    def draw(self) -> None:
        self.bricks.draw()
        for ball in self.balls:
            ball.draw()
        self.paddle.draw()

        if self.has_won:
            self.draw_text_centered("YOU WIN!")
        elif self.has_lost:
            self.draw_text_centered("YOU LOSE.")
        else:
            self.hud.draw(self.player_lives, self.score)

    def draw_text_centered(self, msg: str) -> None:
            font_size: int = 40
            msg_width: int = measure_text(msg, font_size)
            msg_x: int = int((self.play_bounds.width / 2) - (msg_width / 2))
            msg_y: int = int((self.play_bounds.height / 2) - (font_size / 2))
            draw_text(
                msg,
                msg_x,
                msg_y,
                font_size,
                WHITE
            )

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
            # ball.velocity.y *= -1
            # ball.position.y = self.play_bounds.y + self.play_bounds.height - ball.radius
            self.ball_hit_bottom = True

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
                        self.score += 10

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

            self.score += 5

    def player_life_lost(self) -> None:
        self.player_lives -= 1

    def respawn(self) -> None:
        self.is_playing = True
        self.paddle.velocity.x = 0.0
        self.paddle.position = Vector2((self.play_bounds.width / 2) - (self.paddle.bounding_box.width / 2), self.paddle.position.y)
        self.balls = [
            Ball(
                speed=250.0,
                position=Vector2((self.play_bounds.width / 2), (self.paddle.bounding_box.y - 50)),
                radius=5.0,
                color=WHITE,
                velocity=Vector2(0.0, -1.0),
            ),
        ]

    def win(self, delta_time: float) -> None:
        self.is_playing = False
        self.has_won = True

    def lose(self, delta_time: float) -> None:
        self.is_playing = False
        self.has_lost = True
