import tracemalloc
from typing import Callable, Any

BYTES_TO_MB = 1024 * 1024
BYTES_TO_KB = 1024


class MemoryTracker:
    
    def __init__(self):
        self._is_tracking = False
        self._peak_memory_bytes = 0
        self._current_memory_bytes = 0
    
    def start(self) -> None:
        if self._is_tracking:
            tracemalloc.stop()
        tracemalloc.start()
        self._is_tracking = True
        self._peak_memory_bytes = 0
        self._current_memory_bytes = 0
    
    def stop(self) -> float:
        if not self._is_tracking:
            raise RuntimeError("MemoryTracker not started. Call start() first.")
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        self._is_tracking = False
        self._current_memory_bytes = current
        self._peak_memory_bytes = peak
        return self.peak_memory_mb
    
    def _get_memory(self) -> tuple[int, int]:
        if self._is_tracking:
            return tracemalloc.get_traced_memory()
        return self._current_memory_bytes, self._peak_memory_bytes
    
    @property
    def current_memory_mb(self) -> float:
        return self._get_memory()[0] / BYTES_TO_MB
    
    @property
    def peak_memory_mb(self) -> float:
        return self._get_memory()[1] / BYTES_TO_MB
    
    @property
    def current_memory_bytes(self) -> int:
        return self._get_memory()[0]
    
    @property
    def peak_memory_bytes(self) -> int:
        return self._get_memory()[1]
    
    def reset(self) -> None:
        if self._is_tracking:
            tracemalloc.stop()
        self._is_tracking = False
        self._peak_memory_bytes = 0
        self._current_memory_bytes = 0
    
    def get_formatted_memory(self) -> str:
        peak_mb = self.peak_memory_mb
        if peak_mb < 0.01:
            return f"{peak_mb:.4f} MB ({self.peak_memory_bytes / BYTES_TO_KB:.2f} KB)"
        elif peak_mb < 1:
            return f"{peak_mb:.4f} MB"
        return f"{peak_mb:.2f} MB"


def track_memory(func: Callable[..., Any], *args, **kwargs) -> tuple[Any, float]:
    tracker = MemoryTracker()
    tracker.start()
    result = func(*args, **kwargs)
    peak_mb = tracker.stop()
    return result, peak_mb


class SolverMemoryTracker:
    def __init__(self):
        self.tracker = MemoryTracker()
        self.last_peak_memory_mb = 0.0
        self.last_current_memory_mb = 0.0
    
    def measure_memory_usage(self, solver, board: list[list[int]]) -> tuple[bool, float, list[list[int]]]:
        board_copy = [row[:] for row in board]
        
        self.tracker.start()
        solver_instance = solver(board_copy)
        result = solver_instance.solve()
        self.last_peak_memory_mb = self.tracker.stop()
        self.last_current_memory_mb = self.tracker.current_memory_mb
        
        return result, self.last_peak_memory_mb, solver_instance.board
    
    def get_memory_string(self) -> str:
        return self.tracker.get_formatted_memory()


_solver_memory_tracker = SolverMemoryTracker()


def measure_and_solve_memory(solver_class, board: list[list[int]]) -> tuple[bool, float, list[list[int]]]:
    return _solver_memory_tracker.measure_memory_usage(solver_class, board)


def get_last_memory_string() -> str:
    return _solver_memory_tracker.get_memory_string()


class PerformanceTracker:
    
    def __init__(self):
        from performance.timer import Timer
        self.timer = Timer()
        self.memory_tracker = MemoryTracker()
        self.last_time_ms = 0.0
        self.last_peak_memory_mb = 0.0
    
    def measure_all(self, solver_class, board: list[list[int]]) -> dict:
        board_copy = [row[:] for row in board]
        
        self.memory_tracker.start()
        self.timer.start()
        
        solver_instance = solver_class(board_copy)
        result = solver_instance.solve()
        
        self.last_time_ms = self.timer.stop()
        self.last_peak_memory_mb = self.memory_tracker.stop()
        
        steps = getattr(solver_instance, 'step_count', 0)
        
        return {
            'success': result,
            'time_ms': self.last_time_ms,
            'memory_mb': self.last_peak_memory_mb,
            'solved_board': solver_instance.board,
            'steps': steps
        }
    
    def get_summary_string(self) -> str:
        return f"{self.last_time_ms:.2f} ms | {self.last_peak_memory_mb:.4f} MB"
