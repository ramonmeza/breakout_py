from pyray import (
    Color,
    RED,
    ORANGE,
    GREEN,
    BLUE,
    YELLOW,
    PURPLE,
    WHITE,
    get_random_value,
    draw_text,
    measure_text,
    Rectangle,
)


def get_random_color() -> Color:
    options: list[Color] = [
        RED,
        ORANGE,
        GREEN,
        BLUE,
        YELLOW,
        PURPLE
    ]
    i: int = get_random_value(0, len(options) - 1)
    return options[i]


def draw_text_centered(msg: str, bounds: Rectangle, offset_x: int = 0, offset_y: int = 0, font_size: int = 40, color: Color = WHITE) -> None:
    msg_width: int = measure_text(msg, font_size)
    msg_x: int = int((bounds.width / 2) - (msg_width / 2)) + offset_x
    msg_y: int = int((bounds.height / 2) - (font_size / 2)) + offset_y
    draw_text(msg, msg_x, msg_y, font_size, color)
