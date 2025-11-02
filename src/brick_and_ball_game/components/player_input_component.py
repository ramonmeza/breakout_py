from pyray import KeyboardKey, is_key_down


class PlayerInputComponent:
    x_axis_keys: tuple[KeyboardKey, ...]
    x_axis: float

    def __init__(self) -> None:
        self.x_axis_keys = (
            KeyboardKey.KEY_LEFT,
            KeyboardKey.KEY_RIGHT
        )
        self.x_axis = 0.0

    def update(self, delta_time: float) -> None:
        self.x_axis = 0.0
        if is_key_down(self.x_axis_keys[0]):
            self.x_axis = -1.0
        if is_key_down(self.x_axis_keys[1]):
            self.x_axis = 1.0
