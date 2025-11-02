from abc import ABC, abstractmethod


class GameState(ABC):
    def load(self) -> None:
        pass
    
    def unload(self) -> None:
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
