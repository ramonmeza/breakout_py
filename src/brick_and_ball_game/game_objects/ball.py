from pyray import Color, draw_circle, Rectangle, Vector2

from brick_and_ball_game.components import VelocityComponent


class Ball:
    active: bool
    position: Vector2
    radius: float
    color: Color
    velocity: VelocityComponent

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

    def draw(self) -> None:
        if not self.active:
            return

        draw_circle(int(self.position.x), int(self.position.y), self.radius, self.color)
