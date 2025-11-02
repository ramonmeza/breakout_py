from brick_and_ball_game.core.game_state import GameState


class StateManager:
    states: list[GameState]

    def __init__(self) -> None:
        self.states = []

    def push(self, state: GameState) -> None:
        # unload previous state
        if len(self.states) > 0:
            self.states[-1].unload()

        self.states.append(state)
        self.states[-1].load()

    def pop(self) -> GameState | None:
        if len(self.states) > 0:
            state: GameState = self.states.pop()
            state.unload()
            return state
        return None

    def update(self, delta_time: float) -> None:
        if len(self.states) > 0:
            self.states[-1].update(delta_time)
        
    def draw(self) -> None:
        if len(self.states) > 0:
            self.states[-1].draw()

    def unload(self) -> None:
        while len(self.states) > 0:
            self.pop()
