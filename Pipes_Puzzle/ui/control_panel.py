import tkinter as tk
from tkinter import ttk
from ui.components import ModernButton

class ControlPanel(tk.Frame):
    def __init__(self, master, level_list, callbacks, **kwargs):
        super().__init__(master, **kwargs)
        self.callbacks = callbacks
        
        self.algo_var = tk.StringVar(value="A*")
        self.level_var = tk.StringVar(value=level_list[0])
        self.step_by_step = tk.BooleanVar(value=True)
        self.speed_var = tk.IntVar(value=50)
        
        self._setup_ui(level_list)

    def _setup_ui(self, level_list):
        tk.Label(self, text="Select Algorithm", font=('Arial', 10, 'bold')).pack(pady=(0, 5), anchor="w")
        algo_cb = ttk.Combobox(self, textvariable=self.algo_var, state="readonly", font=('Arial', 10))
        algo_cb['values'] = ("DFS", "BFS", "A*", "Simulated Annealing")
        algo_cb.pack(pady=5, fill=tk.X)
        
        tk.Label(self, text="Select Level", font=('Arial', 10, 'bold')).pack(pady=(10, 5), anchor="w")
        level_cb = ttk.Combobox(self, textvariable=self.level_var, state="readonly", font=('Arial', 10))
        level_cb['values'] = tuple(level_list)
        level_cb.bind("<<ComboboxSelected>>", self.callbacks['on_level_change'])
        level_cb.pack(pady=5, fill=tk.X)

        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(pady=10, fill=tk.X)
        ModernButton(ctrl_frame, text="Solve", command=self.callbacks['on_solve'], style="primary").pack(pady=4, fill=tk.X)
        ModernButton(ctrl_frame, text="Stop", command=self.callbacks['on_stop'], style="warning").pack(pady=4, fill=tk.X)
        ModernButton(ctrl_frame, text="Reset", command=self.callbacks['on_reset'], style="secondary").pack(pady=4, fill=tk.X)

        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=(15, 15), fill=tk.X) 
        self.btn_prev = ModernButton(nav_frame, text="< Prev", command=self.callbacks['on_prev'], style="nav")
        self.btn_prev.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self.btn_next = ModernButton(nav_frame, text="Next >", command=self.callbacks['on_next'], style="nav")
        self.btn_next.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2, 0))
        self.toggle_nav_buttons(tk.DISABLED)
        
        anim_frame = tk.Frame(self)
        anim_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Checkbutton(anim_frame, text="Show steps (Animation)", variable=self.step_by_step, font=('Arial', 9)).pack(anchor="w", pady=(0, 5))
        tk.Scale(anim_frame, from_=10, to=500, orient=tk.HORIZONTAL, variable=self.speed_var, label="Speed (ms):", font=('Arial', 9, 'bold')).pack(fill=tk.X)

    def toggle_nav_buttons(self, state):
        self.btn_prev.config(state=state)
        self.btn_next.config(state=state)
        if state == tk.NORMAL:
            self.btn_prev.config(fg="white")
            self.btn_next.config(fg="white")
        else:
            self.btn_prev.config(fg="#DDDDDD")
            self.btn_next.config(fg="#DDDDDD")