class Timer:
    duration: float
    _counter: float
    _running: bool

    def __init__(self, duration: float, start: bool = False) -> None:
        self.duration = duration
        self._counter = duration
        self._running = start

    def update(self, delta_time: float) -> None:
        if self._running:
            self._counter = max(0.0, self._counter - delta_time)
            if self._counter <= 0:
                self._running = False

    def is_running(self) -> bool:
        return self._running

    def progress(self) -> float:
        if self.duration <= 0:
            return 1.0
        return 1.0 - max(0.0, self._counter / self.duration)

    def get_counter(self) -> float:
        return self._counter

    def start(self) -> None:
        self._running = True
        self._counter = self.duration

    def stop(self) -> None:
        self._running = False

    def reset(self, duration: float = 0.0) -> None:
        """If `duration` is `0.0`, use duration provided during init"""
        if duration:
            self.duration = duration
        self._counter = self.duration

    def is_complete(self) -> bool:
        return self._counter <= 0
