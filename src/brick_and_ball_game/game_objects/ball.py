from pyray import Rectangle, Vector2, Color, draw_circle, vector2_normalize

from brick_and_ball_game.components import VelocityComponent

class Ball:
    bounds: Rectangle
    position: Vector2
    radius: float
    color: Color
    velocity: VelocityComponent

    def __init__(self, position: Vector2, radius: float, color: Color, bounds: Rectangle, speed: float, velocity: Vector2) -> None:
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
        if (self.position.y + self.radius > rect.y) and \
            (self.position.y - self.radius < rect.y + rect.height) and \
            (self.position.x + self.radius > rect.x) and \
            (self.position.x - self.radius < rect.x + rect.width):
            if self.velocity.y > 0:
                self.position.y = rect.y - self.radius
            else:
                self.position.y = rect.y + rect.height + self.radius

            self.velocity.y *= -1
            return True
        
        return False

    def update(self, delta_time: float) -> None:
        # update position
        self.position = self.velocity.update(self.position, delta_time)
        self._keep_in_bounds()

    def draw(self) -> None:
        draw_circle(
            int(self.position.x),
            int(self.position.y),
            self.radius,
            self.color
        )
