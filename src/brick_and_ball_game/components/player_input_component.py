import pyray


class InputButton:
    key: int

    def __init__(self, key: int) -> None:
        self.key = key


class InputAxis:
    pos: int
    neg: int
    value: float
    def __init__(self, pos: pyray.KeyboardKey, neg: pyray.KeyboardKey) -> None:
        self.pos = pos
        self.neg = neg
        self.value = 0.0


class PlayerInputComponent:
    axes: dict[str, InputAxis]
    buttons: dict[str, InputButton]

    def __init__(self) -> None:
        self.axes = {}
        self.buttons = {}

    def update(self, delta_time: float) -> None:
        """Only call if axes are bound."""
        # update axes
        for _, axis in self.axes.items():
            axis.value = 0.0
            if pyray.is_key_down(axis.pos):
                axis.value = -1.0
            if pyray.is_key_down(axis.neg):
                axis.value = 1.0

    def get_axis_value(self, axis_name: str) -> float:
        return self.axes[axis_name].value

    def add_axis(self, axis_name: str, pos: int, neg: int) -> None:
        self.axes[axis_name] = InputAxis(pos, neg)

    def add_button(self, btn_name: str, key: int) -> None:
        self.buttons[btn_name] = InputButton(key)

    def is_button_down(self, btn_name: str) -> bool:
        return pyray.is_key_down(self.buttons[btn_name].key)

    def is_button_pressed(self, btn_name: str) -> bool:
        return pyray.is_key_pressed(self.buttons[btn_name].key)
