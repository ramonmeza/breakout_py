from pyray import (
    Color,
    draw_texture,
    Rectangle,
    Texture,
)

from brick_and_ball_game.core.utils import get_random_color


class Brick:
    color: Color
    hit_count: int

    def __init__(self, color: Color, hit_count: int = 1) -> None:
        self.color = color
        self.hit_count = hit_count


class BrickGrid:
    bounding_box: Rectangle
    bricks: list[Brick]
    rows: int
    cols: int
    brick_width: int
    brick_height: int

    def __init__(
        self, rows: int, cols: int, bounding_box: Rectangle, texture: Texture
    ) -> None:
        self.bounding_box = bounding_box
        self.rows = rows
        self.cols = cols
        self.brick_width = int(bounding_box.width / self.cols)
        self.brick_height = int(bounding_box.height / self.rows)
        self.bricks = [Brick(get_random_color()) for _ in range(rows * cols)]
        self.texture = texture
        self.texture.width = self.brick_width
        self.texture.height = self.brick_height

    def are_all_bricks_destroyed(self) -> bool:
        return all(brick.hit_count <= 0 for brick in self.bricks)

    def get_brick_index_at(self, x: float, y: float) -> int | None:
        # convert world position into grid-space
        rel_x: float = x - self.bounding_box.x
        rel_y: float = y - self.bounding_box.y

        # check if point is within grid bounds
        if (
            rel_x < 0
            or rel_y < 0
            or rel_x >= self.bounding_box.width
            or rel_y >= self.bounding_box.height
        ):
            return None  # OOB

        # compute row and column
        col: int = int(rel_x // self.brick_width)
        row: int = int(rel_y // self.brick_height)

        # compute flat list index
        index: int = row * self.cols + col
        if 0 <= index < len(self.bricks):
            return index
        return None

    def draw(self) -> None:
        for i, brick in enumerate(self.bricks):
            if brick.hit_count <= 0:
                continue  # skip destroyed bricks

            row: int = i // self.cols
            col: int = i % self.cols
            x: int = int(self.bounding_box.x + col * self.brick_width)
            y: int = int(self.bounding_box.y + row * self.brick_height)

            draw_texture(self.texture, x, y, brick.color)
