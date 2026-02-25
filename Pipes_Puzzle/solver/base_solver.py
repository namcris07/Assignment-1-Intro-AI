"""
Lớp cơ sở cho các thuật toán giải Pipes Puzzle.
Định nghĩa giao diện chung: solve(), report_step(), get_path().
"""
from typing import Callable, Optional


class BasePipesSolver:
    """Lớp trừu tượng: các solver kế thừa và triển khai _run_algorithm()."""

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.step_count = 0
        self.path = []
        self._callback: Optional[Callable] = None
        self._stopped = False
        self.depth_counts = {}

    def solve(self, step_callback: Optional[Callable] = None) -> bool:
        """Chạy thuật toán. Trả về True nếu tìm được lời giải, False nếu thất bại."""
        self._callback = step_callback
        self._stopped = False
        self.step_count = 0
        return self._run_algorithm()

    def _run_algorithm(self) -> bool:
        """Triển khai cụ thể bởi subclass (DFS, BFS, A*, SA)."""
        raise NotImplementedError("Subclass must implement this algorithm!")

    def report_step(self, row: int, col: int, current_matrix: list) -> bool:
        """Gọi callback khi xử lý mỗi bước (GUI cập nhật, kiểm tra dừng)."""
        self.step_count += 1
        if self._callback:
            if not self._callback(row, col, current_matrix, self._stopped, self.step_count):
                self._stopped = True
                return False
        return True

    def get_path(self, end_node) -> list:
        """Truy vết từ nút đích về gốc, trả về danh sách các trạng thái trên đường đi."""
        path = []
        temp = end_node
        while temp:
            path.insert(0, temp.state.head)
            temp = temp.previous
        return path