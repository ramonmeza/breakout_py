from pyray import BLUE, Color, draw_rectangle, Rectangle, RED


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
    brick_width: float
    brick_height: float

    def __init__(self, rows: int, cols: int, bounding_box: Rectangle) -> None:
        self.bounding_box = bounding_box
        self.rows = rows
        self.cols = cols
        self.brick_width = bounding_box.width / self.cols
        self.brick_height = bounding_box.height / self.rows
        self.bricks = [Brick(RED if bool(i % 2) else BLUE) for i in range(rows * cols)]

    def are_all_bricks_destroyed(self) -> bool:
        return all(brick.hit_count <= 0 for brick in self.bricks)

    def get_brick_index_at(self, x: float, y: float) -> int | None:
        # convert world position into grid-space
        rel_x = x - self.bounding_box.x
        rel_y = y - self.bounding_box.y

        # check if point is within grid bounds
        if (
            rel_x < 0
            or rel_y < 0
            or rel_x >= self.bounding_box.width
            or rel_y >= self.bounding_box.height
        ):
            return None  # OOB

        # compute row and column
        col = int(rel_x // self.brick_width)
        row = int(rel_y // self.brick_height)

        # compute flat list index
        index = row * self.cols + col
        if 0 <= index < len(self.bricks):
            return index
        return None

    def draw(self) -> None:
        for i, brick in enumerate(self.bricks):
            if brick.hit_count <= 0:
                continue  # skip destroyed bricks

            row = i // self.cols
            col = i % self.cols
            x = self.bounding_box.x + col * self.brick_width
            y = self.bounding_box.y + row * self.brick_height

            draw_rectangle(
                int(x),
                int(y),
                int(self.brick_width - 1),  # leave 1px gap
                int(self.brick_height - 1),
                brick.color,
            )
