import tkinter as tk
import copy

from solver import DFSSolver, BFSSolver, AStarSolver, SimulatedAnnealingSolver
from solver.state_and_node import State 
from performance.memory import PerformanceTracker
from data import TESTCASE

from ui.components import ModernButton
from ui.board_view import BoardView
from ui.diagnostics_panel import DiagnosticsPanel
from ui.control_panel import ControlPanel

class PipesGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pipes Puzzle - AI Solver")
        
        self.is_solving = False
        self.stop_solving = False
        self.solved_path = []
        self.current_step = 0
        self.current_solver = None
        
        self._build_architecture()
        self._reset_board()

    def _build_architecture(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # === CỘT TRÁI ===
        self.left_col = tk.Frame(self.main_frame)
        self.left_col.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        self.board_view = BoardView(self.left_col)
        self.board_view.pack()
        
        self.diag_panel = DiagnosticsPanel(self.left_col)
        self.diag_panel.pack(fill=tk.X, pady=(15, 0))

        self.btn_plot = ModernButton(self.left_col, text="Plot Statistic", command=self._trigger_plot, style="nav")
        self.btn_plot.pack(pady=(15, 0))
        self.btn_plot.config(state=tk.DISABLED)

        # === CỘT PHẢI ===
        self.right_col = tk.Frame(self.main_frame)
        self.right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Truyền callback để Control Panel biết gọi ai khi bấm nút
        callbacks = {
            'on_solve': self._solve,
            'on_stop': self._stop,
            'on_reset': self._reset_board,
            'on_level_change': lambda e: self._reset_board(),
            'on_prev': self._prev_step,
            'on_next': self._next_step
        }
        self.control_panel = ControlPanel(self.right_col, list(TESTCASE.keys()), callbacks)
        self.control_panel.pack(fill=tk.BOTH, expand=True)

        # Status Bar
        status_container = tk.Frame(self.right_col)
        status_container.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 10))
        tk.Label(status_container, text="Status:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        self.status_label = tk.Label(status_container, text="Ready", fg="blue", font=('Arial', 12, 'bold'))
        self.status_label.pack(side=tk.LEFT)

    # LOGIC CONTROLLER
    def _trigger_plot(self):
        if self.current_solver and hasattr(self.current_solver, 'depth_counts'):
            self.diag_panel.show_plot(
                self.current_solver.depth_counts, 
                self.control_panel.algo_var.get(), 
                self.control_panel.level_var.get()
            )

    def _reset_board(self):
        if self.is_solving: return
        self.stop_solving = True
        self.solved_path = []
        self.current_step = 0
        self.current_solver = None
        
        self.control_panel.toggle_nav_buttons(tk.DISABLED)
        self.btn_plot.config(state=tk.DISABLED, fg="#DDDDDD")
        self.diag_panel.reset_stats()
        self.status_label.config(text="Reset to Initial", fg="blue")
        
        lvl = self.control_panel.level_var.get()
        self.initial_state = State(copy.deepcopy(TESTCASE[lvl])).head 
        self.board_view.draw_board(self.initial_state)

    def _update_manual_view(self):
        frame = self.solved_path[self.current_step]
        if hasattr(frame, 'state'): frame = frame.state.head
        self.board_view.draw_board(frame)
        self.diag_panel.update_step_only(self.current_step, len(self.solved_path)-1)

    def _prev_step(self):
        if not self.solved_path or self.current_step <= 0 or self.is_solving: return
        self.current_step -= 1
        self._update_manual_view()

    def _next_step(self):
        if not self.solved_path or self.current_step >= len(self.solved_path) - 1 or self.is_solving: return
        self.current_step += 1
        self._update_manual_view()

    def _stop(self):
        if self.is_solving:
            self.stop_solving = True
            if self.current_solver: self.current_solver._stopped = True 
            self.status_label.config(text="Stopped by user", fg="red")

    def _solver_callback(self, row, col, current_matrix, is_stopped, step_count):
        if self.stop_solving: return False
        if step_count % 500 == 0:
            self.root.update_idletasks()
            self.root.update()
        return True

    def _solve(self):
        if self.is_solving: return
        
        algo_name = self.control_panel.algo_var.get()
        algo_map = {"DFS": DFSSolver, "BFS": BFSSolver, "A*": AStarSolver, "Simulated Annealing": SimulatedAnnealingSolver}
        solver_class = algo_map[algo_name]
        
        self.is_solving = True
        self.stop_solving = False
        self.control_panel.toggle_nav_buttons(tk.DISABLED)
        self.btn_plot.config(state=tk.DISABLED, fg="#DDDDDD")
        self.status_label.config(text="Thinking...", fg="orange")
        self.root.update()
        
        solve_state = copy.deepcopy(TESTCASE[self.control_panel.level_var.get()])
        self.board_view.draw_board(State(solve_state).head) # Vẽ state ban đầu
        
        self.current_solver = solver_class(solve_state)
        
        tracker = PerformanceTracker()
        tracker.memory_tracker.start()
        tracker.timer.start()
        
        result = self.current_solver.solve(step_callback=self._solver_callback)
            
        time_ms = tracker.timer.stop()
        mem_mb = tracker.memory_tracker.stop()
        
        if self.stop_solving: 
            self.is_solving = False
            return
        
        if result:
            self.status_label.config(text="Animating...", fg="green")
            self.solved_path = self.current_solver.path
            self.current_step = 0
            
            path_length = len(self.solved_path) - 1 if self.solved_path else 0
            self.diag_panel.update_stats(0, path_length, self.current_solver.step_count, time_ms, mem_mb)
            
            if algo_name in ["A*", "Simulated Annealing"]:
                self.btn_plot.config(state=tk.NORMAL, fg="white")

            if self.control_panel.step_by_step.get() and self.solved_path:
                self._animate_path(0)
            else:
                if self.solved_path:
                    self.current_step = path_length
                    self._update_manual_view()
                self.control_panel.toggle_nav_buttons(tk.NORMAL)
                self.is_solving = False
                self.status_label.config(text="FINISHED!", fg="green")
        else:
            self.status_label.config(text="STUCK", fg="red")
            self.diag_panel.update_stats("-", "-", self.current_solver.step_count, time_ms, mem_mb)
            self.is_solving = False

    def _animate_path(self, index: int):
        if self.stop_solving or index >= len(self.solved_path):
            self.is_solving = False
            self.control_panel.toggle_nav_buttons(tk.NORMAL)
            self.status_label.config(text="FINISHED!", fg="green")
            return
            
        try:
            if not self.diag_panel.step_label.winfo_exists():
                self.stop_solving = True
                return
            
            self.current_step = index
            self._update_manual_view()
            self.root.after(self.control_panel.speed_var.get(), lambda: self._animate_path(index + 1))
        except tk.TclError:
            self.stop_solving = True