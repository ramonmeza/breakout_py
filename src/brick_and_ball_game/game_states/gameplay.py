from __future__ import annotations
from enum import IntEnum
from typing import override

import math

from pyray import (
    check_collision_recs,
    draw_text,
    draw_texture,
    GREEN,
    KeyboardKey,
    measure_text,
    Rectangle,
    RED,
    Vector2,
    vector2_normalize,
    WHITE,
)

from brick_and_ball_game.core.game_state import GameState
from brick_and_ball_game.core.timer import Timer
from brick_and_ball_game.components.player_input_component import PlayerInputComponent
from brick_and_ball_game.game_objects.ball import Ball
from brick_and_ball_game.game_objects.bricks import BrickGrid
from brick_and_ball_game.game_objects.paddle import Paddle


RESPAWN_TIMER: float = 3.0
BALL_RADIUS: float = 7.0
BALL_SPEED: float = 300.0
PLAYER_LIVES: int = 3
BRICK_ROWS: int = 3
BRICK_COLS: int = 5


class GameplayStates(IntEnum):
    STATE_STARTING = 0
    STATE_PLAYING = 1
    STATE_LOST_LIFE = 2
    STATE_GAME_WON = 3
    STATE_GAME_LOST = 4


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
    game_timer: Timer
    has_won: bool
    has_lost: bool
    player_lives: int
    ball_hit_bottom: bool
    score: int
    current_state: int
    player_input: PlayerInputComponent

    @override
    def load(self) -> None:
        self.game_timer = Timer(RESPAWN_TIMER)
        self.score = 0
        self.hud = HUD()
        self.has_won = False
        self.has_lost = False
        self.player_lives = PLAYER_LIVES
        self.ball_hit_bottom = False
        self.current_state = GameplayStates.STATE_STARTING
        self.play_bounds = Rectangle(0, 0, 800, 600)

        # load paddle
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
        self.texture_manager.load_texture("Paddle", r"assets\textures\paddleBlue.png")
        self.texture_manager.get_texture("Paddle").width = int(
            self.paddle.bounding_box.width
        )
        self.texture_manager.get_texture("Paddle").height = int(
            self.paddle.bounding_box.height
        )

        # create balls
        self.balls = [
            Ball(
                speed=BALL_SPEED,
                position=Vector2((self.play_bounds.width / 2), (paddle_y - 50)),
                radius=BALL_RADIUS,
                color=RED,
                velocity=Vector2(0.0, -1.0),
            ),
        ]
        self.texture_manager.load_texture("Ball", r"assets\textures\ballGrey.png")
        self.texture_manager.get_texture("Ball").width = int(BALL_RADIUS * 2)
        self.texture_manager.get_texture("Ball").height = int(BALL_RADIUS * 2)
        self.sound_manager.load_sfx("Bounce Wall", r"assets\sfx\Hit_4.wav", volume=0.35)
        self.sound_manager.load_sfx(
            "Bounce Brick", r"assets\sfx\Coin_2.wav", volume=0.35
        )
        self.sound_manager.load_sfx(
            "Bounce Paddle", r"assets\sfx\Hit_5.wav", volume=0.35
        )

        # load bricks
        self.texture_manager.load_texture(
            "Brick", r"assets\textures\element_grey_rectangle.png"
        )
        self.bricks = BrickGrid(
            rows=BRICK_ROWS,
            cols=BRICK_COLS,
            bounding_box=Rectangle(0, 50, self.play_bounds.width, 150),
            texture=self.texture_manager.get_texture("Brick"),
        )

        # bind input
        self.player_input = PlayerInputComponent()
        self.player_input.add_button("Pause", KeyboardKey.KEY_ESCAPE)

        # load audio
        self.sound_manager.load_sfx("Lose", r"assets\sfx\lose_1.wav")
        self.sound_manager.load_sfx("Win", r"assets\sfx\stat_increase.wav")
        self.sound_manager.load_sfx("Life Lost", r"assets\sfx\Explosion_6.wav")

    @override
    def unload(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        match self.current_state:
            case GameplayStates.STATE_STARTING:
                if self.game_timer.is_complete():
                    self.current_state = GameplayStates.STATE_PLAYING
                    self.game_timer.reset()
                    self.game_timer.stop()
                elif not self.game_timer.is_running():
                    self.game_timer.start()

            case GameplayStates.STATE_PLAYING:
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
                    self.current_state = GameplayStates.STATE_LOST_LIFE

                # check win condition
                if self.bricks.are_all_bricks_destroyed():
                    self.current_state = GameplayStates.STATE_GAME_WON

                # pause menu (only if playing)
                if self.player_input.is_button_pressed("Pause"):
                    from brick_and_ball_game.game_states.menus import PauseMenu

                    self.state_manager.push(PauseMenu())

            case GameplayStates.STATE_LOST_LIFE:
                self.sound_manager.play_sfx("Life Lost")
                self.player_lives -= 1
                self.current_state = GameplayStates.STATE_STARTING
                # game over condition
                if self.player_lives <= 0:
                    self.current_state = GameplayStates.STATE_GAME_LOST
                else:
                    self.respawn()

            case GameplayStates.STATE_GAME_WON:
                if not self.has_won:
                    self.sound_manager.play_sfx("Win")
                    self.has_won = True
                    from brick_and_ball_game.game_states.menus import GameOverMenu

                    self.state_manager.push(
                        GameOverMenu(has_won=True, score=self.score)
                    )

            case GameplayStates.STATE_GAME_LOST:
                if not self.has_lost:
                    self.sound_manager.play_sfx("Lose")
                    self.has_lost = True
                    from brick_and_ball_game.game_states.menus import GameOverMenu

                    self.state_manager.push(
                        GameOverMenu(has_won=False, score=self.score)
                    )

            case _:
                pass

        # update timers
        self.game_timer.update(delta_time)

    def draw(self) -> None:
        self.bricks.draw()
        # draw balls
        for ball in self.balls:
            if not ball.active:
                continue

            draw_texture(
                self.texture_manager.get_texture("Ball"),
                int(ball.position.x - ball.radius),
                int(ball.position.y - ball.radius),
                WHITE,
            )

        # draw paddle
        draw_texture(
            self.texture_manager.get_texture("Paddle"),
            int(self.paddle.bounding_box.x),
            int(self.paddle.bounding_box.y),
            WHITE,
        )

        # HUD
        self.hud.draw(self.player_lives, self.score)

        # count-down
        if self.game_timer.is_running():
            self.draw_text_centered(str(math.ceil(self.game_timer.get_counter())))

    def draw_text_centered(
        self, msg: str, font_size: int = 40, offset_x: int = 0, offset_y: int = 0
    ) -> None:
        msg_width: int = measure_text(msg, font_size)
        msg_x: int = int((self.play_bounds.width / 2) - (msg_width / 2)) + offset_x
        msg_y: int = int((self.play_bounds.height / 2) - (font_size / 2)) + offset_y
        draw_text(msg, msg_x, msg_y, font_size, WHITE)

    def handle_ball_walls(self, ball: Ball) -> None:
        # left
        if ball.position.x - ball.radius < self.play_bounds.x:
            ball.velocity.x *= -1
            ball.position.x = self.play_bounds.x + ball.radius
            self.sound_manager.play_sfx("Bounce Wall")

        # right
        if ball.position.x + ball.radius > self.play_bounds.x + self.play_bounds.width:
            ball.velocity.x *= -1
            ball.position.x = self.play_bounds.x + self.play_bounds.width - ball.radius
            self.sound_manager.play_sfx("Bounce Wall")

        # top
        if ball.position.y - ball.radius < self.play_bounds.y:
            ball.velocity.y *= -1
            ball.position.y = self.play_bounds.y + ball.radius
            self.sound_manager.play_sfx("Bounce Wall")

        # bottom
        if ball.position.y + ball.radius > self.play_bounds.y + self.play_bounds.height:
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
                        self.sound_manager.play_sfx("Bounce Brick")

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
            ball.velocity.speed += 25.0
            self.score += 5
            self.sound_manager.play_sfx("Bounce Paddle")

    def respawn(self) -> None:
        self.paddle.velocity.x = 0.0
        self.paddle.position = Vector2(
            (self.play_bounds.width / 2) - (self.paddle.bounding_box.width / 2),
            self.paddle.position.y,
        )
        self.balls = [
            Ball(
                speed=250.0,
                position=Vector2(
                    (self.play_bounds.width / 2), (self.paddle.bounding_box.y - 50)
                ),
                radius=5.0,
                color=WHITE,
                velocity=Vector2(0.0, -1.0),
            ),
        ]
