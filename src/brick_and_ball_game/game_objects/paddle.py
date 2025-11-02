from pyray import (
    Color,
    draw_rectangle,
    KeyboardKey,
    Rectangle,
    Vector2,
)

from brick_and_ball_game.components import PlayerInputComponent, VelocityComponent


class Paddle:
    bounding_box: Rectangle
    color: Color
    velocity: VelocityComponent
    player_input: PlayerInputComponent
    bounds: Rectangle

    def __init__(
        self, bounding_box: Rectangle, color: Color, bounds: Rectangle, speed: float
    ) -> None:
        self.bounding_box = bounding_box
        self.color = color
        self.velocity = VelocityComponent(speed, Vector2(0.0, 0.0), 5.0)
        self.player_input = PlayerInputComponent()
        self.player_input.add_axis(
            "X Axis",
            KeyboardKey.KEY_LEFT,
            KeyboardKey.KEY_RIGHT,
        )
        self.bounds = bounds

    @property
    def position(self) -> Vector2:
        return Vector2(self.bounding_box.x, self.bounding_box.y)

    @position.setter
    def position(self, value: Vector2) -> None:
        self.bounding_box.x = value.x
        self.bounding_box.y = value.y

    def _keep_in_bounds(self) -> None:
        # left
        if self.bounding_box.x < self.bounds.x:
            self.bounding_box.x = self.bounds.x

        # right
        if (
            self.bounding_box.x + self.bounding_box.width
            > self.bounds.x + self.bounds.width
        ):
            self.bounding_box.x = (
                self.bounds.x + self.bounds.width - self.bounding_box.width
            )

    def update(self, delta_time: float) -> None:
        self.player_input.update(delta_time)
        self.velocity.x = self.player_input.get_axis_value("X Axis")
        self.position = self.velocity.update(self.position, delta_time)
        self._keep_in_bounds()

    def draw(self) -> None:
        draw_rectangle(
            int(self.bounding_box.x),
            int(self.bounding_box.y),
            int(self.bounding_box.width),
            int(self.bounding_box.height),
            self.color,
        )
