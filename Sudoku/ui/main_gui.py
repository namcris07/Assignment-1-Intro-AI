from __future__ import annotations
import tkinter as tk
from tkinter import messagebox

from solver.backtracking_solver import BacktrackingSolver
from performance.memory import PerformanceTracker

COLOR_SOLVED = ("#00AA00", "#CCFFCC")
COLOR_STEP = ("#0066CC", "#E6F0FF")

BUTTON_STYLES = {
    "primary": {"bg": "#4CAF50", "hover": "#45a049", "fg": "white", "active": "#3d8b40"},
    "secondary": {"bg": "#2196F3", "hover": "#1976D2", "fg": "white", "active": "#1565C0"},
    "warning": {"bg": "#FF9800", "hover": "#F57C00", "fg": "white", "active": "#E65100"},
    "danger": {"bg": "#f44336", "hover": "#d32f2f", "fg": "white", "active": "#c62828"},
}


class ModernButton(tk.Button):
    def __init__(self, master, text: str, command, style: str = "primary", **kwargs):
        self.style = BUTTON_STYLES.get(style, BUTTON_STYLES["primary"])
        super().__init__(
            master, text=text, command=command,
            bg=self.style["bg"], fg=self.style["fg"],
            activebackground=self.style["active"], activeforeground=self.style["fg"],
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2",
            padx=15, pady=8, **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg=self.style["hover"]))
        self.bind("<Leave>", lambda e: self.config(bg=self.style["bg"]))

    def update_style(self, style: str):
        self.style = BUTTON_STYLES.get(style, BUTTON_STYLES["primary"])
        self.config(bg=self.style["bg"], fg=self.style["fg"], activebackground=self.style["active"])


class SudokuGUI:
    CELL_SIZE = 60
    GRID_SIZE = 9
    BOARD_SIZE = CELL_SIZE * GRID_SIZE
    DEFAULT_SPEED = 50

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sudoku Solver")
        self.cells: list[list[tk.Entry]] = [[None for _ in range(9)] for _ in range(9)]
        self.initial_cells: set[tuple[int, int]] = set()
        self.step_by_step = tk.BooleanVar(value=True)
        self.speed_var = tk.IntVar(value=self.DEFAULT_SPEED)
        self.is_solving = False
        self.stop_solving = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        self._setup_board()
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        self._setup_controls()
        self._setup_speed_control()
        self._setup_status()

    def _setup_board(self) -> None:
        board_frame = tk.Frame(self.main_frame)
        board_frame.pack(side=tk.LEFT)
        self.canvas = tk.Canvas(
            board_frame, width=self.BOARD_SIZE, height=self.BOARD_SIZE,
            bg='white', highlightthickness=0
        )
        self.canvas.pack()
        self._draw_grid_lines()
        validate_cmd = (self.root.register(self._validate_input), '%P')
        for r in range(9):
            for c in range(9):
                x = c * self.CELL_SIZE + self.CELL_SIZE // 2
                y = r * self.CELL_SIZE + self.CELL_SIZE // 2
                entry = tk.Entry(
                    board_frame, width=2, font=('Arial', 20, 'bold'),
                    justify='center', validate='key', validatecommand=validate_cmd,
                    bd=0, highlightthickness=0
                )
                self.canvas.create_window(x, y, window=entry, width=self.CELL_SIZE - 8, height=self.CELL_SIZE - 8)
                self.cells[r][c] = entry

    def _draw_grid_lines(self) -> None:
        for i in range(self.GRID_SIZE + 1):
            thickness = 3 if i % 3 == 0 else 1
            pos = i * self.CELL_SIZE
            self.canvas.create_line(pos, 0, pos, self.BOARD_SIZE, width=thickness, fill='black')
            self.canvas.create_line(0, pos, self.BOARD_SIZE, pos, width=thickness, fill='black')

    def _setup_controls(self) -> None:
        tk.Label(self.right_frame, text="Controls", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        ctrl_frame = tk.Frame(self.right_frame)
        ctrl_frame.pack(pady=5)
        buttons = [
            ("Solve", self._solve, "primary"),
            ("Stop", self._stop, "warning"),
            ("Reset", self._reset_board, "danger"),
        ]
        self.buttons = {}
        for text, command, style in buttons:
            btn = ModernButton(ctrl_frame, text=text, command=command, style=style)
            btn.pack(pady=4, fill=tk.X)
            self.buttons[text.lower()] = btn

    def _setup_speed_control(self) -> None:
        self._add_separator()
        tk.Label(self.right_frame, text="Step-by-Step", font=('Arial', 10, 'bold')).pack()
        tk.Checkbutton(
            self.right_frame, text="Show steps",
            variable=self.step_by_step, font=('Arial', 9)
        ).pack(pady=5)
        speed_frame = tk.Frame(self.right_frame)
        speed_frame.pack(pady=5, fill=tk.X)
        tk.Label(speed_frame, text="Speed (ms):", font=('Arial', 9)).pack(side=tk.LEFT)
        self.speed_label = tk.Label(speed_frame, text=str(self.DEFAULT_SPEED), font=('Arial', 9, 'bold'), fg='blue')
        self.speed_label.pack(side=tk.RIGHT)
        tk.Scale(
            self.right_frame, from_=10, to=100, orient=tk.HORIZONTAL,
            variable=self.speed_var, showvalue=False,
            command=lambda v: self.speed_label.config(text=v), length=100
        ).pack(pady=5)

    def _add_separator(self):
        tk.Frame(self.right_frame, height=2, bg='gray').pack(fill=tk.X, pady=10)

    def _setup_status(self) -> None:
        self._add_separator()
        tk.Label(self.right_frame, text="Status", font=('Arial', 10, 'bold')).pack()
        self.status_label = tk.Label(self.right_frame, text="Ready", font=('Arial', 10), fg="blue")
        self.status_label.pack(pady=5)
        self.step_label = tk.Label(self.right_frame, text="Steps: 0", font=('Arial', 9), fg="gray")
        self.step_label.pack(pady=2)
        self._add_separator()
        tk.Label(self.right_frame, text="Performance Stats", font=('Arial', 10, 'bold')).pack()
        self.nodes_label = tk.Label(self.right_frame, text="Nodes: -", font=('Arial', 9), fg="#555")
        self.nodes_label.pack(pady=2)
        self.time_label = tk.Label(self.right_frame, text="Time: -", font=('Arial', 9), fg="#555")
        self.time_label.pack(pady=2)
        self.memory_label = tk.Label(self.right_frame, text="Memory: -", font=('Arial', 9), fg="#555")
        self.memory_label.pack(pady=2)

    def _validate_input(self, val: str) -> bool:
        return val == "" or (val.isdigit() and 1 <= int(val) <= 9)

    def _get_board(self) -> list[list[int]]:
        return [
            [int(self.cells[r][c].get()) if self.cells[r][c].get() else 0 for c in range(9)]
            for r in range(9)
        ]

    def _set_board(self, board: list[list[int]]) -> None:
        self.initial_cells.clear()
        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                cell.delete(0, tk.END)
                cell.config(bg='white', fg='black')
                if board[r][c] != 0:
                    cell.insert(0, str(board[r][c]))
                    self.initial_cells.add((r, c))

    def _update_cell(self, row: int, col: int, value: int, is_remove: bool = False) -> None:
        cell = self.cells[row][col]
        cell.delete(0, tk.END)
        if is_remove or value == 0:
            cell.config(bg='white', fg='black')
        else:
            cell.insert(0, str(value))
            cell.config(fg=COLOR_STEP[0], bg=COLOR_STEP[1])
        self.root.update()

    def _step_callback(self, row: int, col: int, value: int, is_backtrack: bool, step_count: int) -> bool:
        if self.stop_solving:
            return False
        self.step_label.config(text=f"Steps: {step_count}")
        if self.step_by_step.get():
            self._update_cell(row, col, value, is_remove=is_backtrack)
            self.root.after(self.speed_var.get())
            self.root.update()
        return True

    def _stop(self) -> None:
        if self.is_solving:
            self.stop_solving = True
            self.status_label.config(text="Stopped", fg="orange")

    def _reset_stats(self):
        self.nodes_label.config(text="Nodes: -", fg="#555")
        self.time_label.config(text="Time: -", fg="#555")
        self.memory_label.config(text="Memory: -", fg="#555")

    def _display_stats(self, nodes: int, time_ms: float, memory_mb: float):
        self.nodes_label.config(text=f"Nodes: {nodes}", fg="#2196F3")
        if time_ms < 1:
            time_text = f"Time: {time_ms:.4f} ms"
            time_color = "#4CAF50"
        elif time_ms < 1000:
            time_text = f"Time: {time_ms:.2f} ms"
            time_color = "#4CAF50"
        else:
            time_text = f"Time: {time_ms:.2f} ms ({time_ms/1000:.2f}s)"
            time_color = "#FF9800"
        self.time_label.config(text=time_text, fg=time_color)
        if memory_mb < 0.01:
            memory_text = f"Memory: {memory_mb * 1024:.2f} KB"
        else:
            memory_text = f"Memory: {memory_mb:.4f} MB"
        self.memory_label.config(text=memory_text, fg="#9C27B0")

    def _solve(self) -> None:
        if self.is_solving:
            return
        board = self._get_board()
        self.initial_cells = {(r, c) for r in range(9) for c in range(9) if board[r][c] != 0}
        self.is_solving = True
        self.stop_solving = False
        self.step_label.config(text="Steps: 0")
        self.status_label.config(text="Solving...", fg="orange")
        self._reset_stats()
        self.root.update()
        solver = BacktrackingSolver(board)
        perf_tracker = PerformanceTracker()
        perf_result = perf_tracker.measure_all(BacktrackingSolver, board)
        if self.step_by_step.get():
            result = solver.solve(step_callback=self._step_callback)
        else:
            result = solver.solve()
        self.is_solving = False
        if self.stop_solving:
            return
        if result:
            self._set_board(solver.board)
            for r in range(9):
                for c in range(9):
                    if (r, c) not in self.initial_cells:
                        self.cells[r][c].config(fg=COLOR_SOLVED[0], bg=COLOR_SOLVED[1])
            self.step_label.config(text=f"Steps: {getattr(solver, 'step_count', 0)}")
            self.status_label.config(text="Solved", fg="green")
            self._display_stats(perf_result['steps'], perf_result['time_ms'], perf_result['memory_mb'])
        else:
            self.status_label.config(text="No solution found", fg="red")
            self._reset_stats()
            messagebox.showerror("Error", "No solution found for this Sudoku")

    def _reset_board(self) -> None:
        self.stop_solving = True
        self.is_solving = False
        self.initial_cells.clear()
        self.status_label.config(text="Ready", fg="blue")
        self.step_label.config(text="Steps: 0")
        self._reset_stats()
        for r in range(9):
            for c in range(9):
                self.cells[r][c].config(bg='white', fg='black')
                self.cells[r][c].delete(0, tk.END)


def main():
    root = tk.Tk()
    root.resizable(False, False)
    SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
