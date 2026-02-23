from typing import Callable, Optional

class BacktrackingSolver:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.step_count = 0
        self._callback: Optional[Callable] = None
        self._stopped = False

    def solve(self, step_callback: Optional[Callable] = None) -> bool:
        self._callback = step_callback
        self._stopped = False
        self.step_count = 0
        return self._solve_recursive()

    def _solve_recursive(self) -> bool:
        if self._stopped:
            return False
        find = self.find_empty()
        if not find:
            return True
        row, col = find
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                self.step_count += 1
                if self._callback:
                    if not self._callback(row, col, num, False, self.step_count):
                        self._stopped = True
                        return False
                if self._solve_recursive():
                    return True
                self.board[row][col] = 0
                self.step_count += 1
                if self._callback:
                    if not self._callback(row, col, 0, True, self.step_count):
                        self._stopped = True
                        return False
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, num, pos):
        row, col = pos
        for j in range(9):
            if self.board[row][j] == num and col != j:
                return False
        for i in range(9):
            if self.board[i][col] == num and row != i:
                return False
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
        return True