from pyray import (
    Color,
    Rectangle,
    Vector2,
)

from brick_and_ball_game.components.velocity_component import VelocityComponent
from brick_and_ball_game.core.timer import Timer

TRAIL_LENGTH: int = 15
TRAIL_TIME: float = 0.01


class Ball:
    active: bool
    position: Vector2
    radius: float
    color: Color
    velocity: VelocityComponent
    trail_timer: Timer
    trail: list[Vector2]
    trail_length: int

    def __init__(
        self,
        position: Vector2,
        radius: float,
        color: Color,
        speed: float,
        velocity: Vector2,
    ) -> None:
        self.active = True
        self.position = position
        self.radius = radius
        self.color = color
        self.velocity = VelocityComponent(speed, velocity, friction=0)
        self.trail_length = TRAIL_LENGTH
        self.trail_timer = Timer(TRAIL_TIME, start=True)
        self.trail = []

    def bounce_off(self, rect: Rectangle) -> bool:
        if not self.active:
            return False

        # AABB collision check
        if (
            self.position.x + self.radius > rect.x
            and self.position.x - self.radius < rect.x + rect.width
            and self.position.y + self.radius > rect.y
            and self.position.y - self.radius < rect.y + rect.height
        ):
            # compute overlap distances for all four sides
            overlap_left = (self.position.x + self.radius) - rect.x
            overlap_right = (rect.x + rect.width) - (self.position.x - self.radius)
            overlap_top = (self.position.y + self.radius) - rect.y
            overlap_bottom = (rect.y + rect.height) - (self.position.y - self.radius)

            # find smallest overlap (the side we hit)
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            if min_overlap == overlap_left:
                # hit left side
                self.position.x = rect.x - self.radius
                self.velocity.x *= -1
            elif min_overlap == overlap_right:
                # hit right side
                self.position.x = rect.x + rect.width + self.radius
                self.velocity.x *= -1
            elif min_overlap == overlap_top:
                # hit top
                self.position.y = rect.y - self.radius
                self.velocity.y *= -1
            elif min_overlap == overlap_bottom:
                # hit bottom
                self.position.y = rect.y + rect.height + self.radius
                self.velocity.y *= -1

            return True

        return False

    def update(self, delta_time: float) -> None:
        if not self.active:
            return

        # update position
        self.position = self.velocity.update(self.position, delta_time)
    
        self.trail_timer.update(delta_time)
        if self.trail_timer.is_complete():
            self.trail.append(Vector2(self.position.x, self.position.y))
            if len(self.trail) > self.trail_length:
                self.trail.pop(0)
            self.trail_timer.reset()
            self.trail_timer.start()