from pyray import Vector2, vector2_add, vector2_normalize, vector2_scale


class VelocityComponent:
    speed: float
    velocity: Vector2
    friction: float

    def __init__(
        self, speed: float, velocity: Vector2 = Vector2(0, 0), friction: float = 0.0
    ) -> None:
        self.speed = speed
        self.velocity = velocity
        self.friction = friction

    def update(self, current_position: Vector2, delta_time: float) -> Vector2:
        # normalize velocity to prevent faster diagonal movement
        dir = vector2_normalize(self.velocity)
        displacement: Vector2 = vector2_scale(dir, self.speed * delta_time)
        next_position: Vector2 = vector2_add(current_position, displacement)
        return next_position

    @property
    def x(self) -> float:
        return self.velocity.x

    @x.setter
    def x(self, value: float) -> None:
        self.velocity.x = value

    @property
    def y(self) -> float:
        return self.velocity.y

    @y.setter
    def y(self, value: float) -> None:
        self.velocity.y = value
