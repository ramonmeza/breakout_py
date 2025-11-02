from pyray import Color, draw_circle, Rectangle, Vector2

from brick_and_ball_game.components import VelocityComponent


class Ball:
    bounds: Rectangle
    position: Vector2
    radius: float
    color: Color
    velocity: VelocityComponent

    def __init__(
        self,
        position: Vector2,
        radius: float,
        color: Color,
        bounds: Rectangle,
        speed: float,
        velocity: Vector2,
    ) -> None:
        self.bounds = bounds
        self.position = position
        self.radius = radius
        self.color = color
        self.velocity = VelocityComponent(speed, velocity, friction=0)

    def _keep_in_bounds(self) -> None:
        # left
        if self.position.x - self.radius < self.bounds.x:
            self.velocity.x *= -1
            self.position.x = self.bounds.x + self.radius

        # right
        if self.position.x + self.radius > self.bounds.x + self.bounds.width:
            self.velocity.x *= -1
            self.position.x = self.bounds.x + self.bounds.width - self.radius

        # top
        if self.position.y - self.radius < self.bounds.y:
            self.velocity.y *= -1
            self.position.y = self.bounds.y + self.radius

        # bottom
        if self.position.y + self.radius > self.bounds.y + self.bounds.height:
            self.velocity.y *= -1
            self.position.y = self.bounds.y + self.bounds.height - self.radius

    def bounce_off(self, rect: Rectangle) -> bool:
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
        # update position
        self.position = self.velocity.update(self.position, delta_time)
        self._keep_in_bounds()

    def draw(self) -> None:
        draw_circle(int(self.position.x), int(self.position.y), self.radius, self.color)
