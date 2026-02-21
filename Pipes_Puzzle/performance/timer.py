import time
from typing import Optional, Callable, Any


class Timer:
    def __init__(self):
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._elapsed_ms: float = 0.0

    def start(self) -> None:
        self._start_time = time.perf_counter()
        self._end_time = None
        self._elapsed_ms = 0.0

    def stop(self) -> float:
        if self._start_time is None:
            raise RuntimeError("Timer not started. Call start() first.")
        self._end_time = time.perf_counter()
        self._elapsed_ms = (self._end_time - self._start_time) * 1000
        return self._elapsed_ms

    @property
    def elapsed_ms(self) -> float:
        if self._start_time is None:
            return 0.0
        if self._end_time is not None:
            return self._elapsed_ms
        return (time.perf_counter() - self._start_time) * 1000

    def reset(self) -> None:
        self._start_time = None
        self._end_time = None
        self._elapsed_ms = 0.0

    def get_formatted_time(self) -> str:
        elapsed = self.elapsed_ms
        if elapsed < 1:
            return f"{elapsed:.4f} ms"
        elif elapsed < 1000:
            return f"{elapsed:.2f} ms"
        return f"{elapsed:.2f} ms ({elapsed / 1000:.2f} s)"


def time_solver(solver_func: Callable[..., Any], *args, **kwargs) -> tuple[Any, float]:
    timer = Timer()
    timer.start()
    result = solver_func(*args, **kwargs)
    return result, timer.stop()


class SolverTimer:
    def __init__(self):
        self.timer = Timer()
        self.last_solve_time_ms: float = 0.0

    def measure_solve_time(self, solver, board: list[list[int]]) -> tuple[bool, float, list[list[int]]]:
        board_copy = [row[:] for row in board]
        solver_instance = solver(board_copy)
        self.timer.start()
        result = solver_instance.solve()
        self.last_solve_time_ms = self.timer.stop()
        return result, self.last_solve_time_ms, solver_instance.board

    def get_time_string(self) -> str:
        return self.timer.get_formatted_time()


_solver_timer = SolverTimer()


def measure_and_solve(solver_class, board: list[list[int]]) -> tuple[bool, float, list[list[int]]]:
    return _solver_timer.measure_solve_time(solver_class, board)


def get_last_time_string() -> str:
    return _solver_timer.get_time_string()
