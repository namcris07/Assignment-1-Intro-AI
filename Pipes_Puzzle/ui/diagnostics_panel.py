import tkinter as tk
import matplotlib.pyplot as plt
from .components import ModernButton

class DiagnosticsPanel(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Diagnostics", font=('Arial', 10, 'bold'), bg="#f0f0f0", bd=1, relief=tk.SUNKEN, **kwargs)
        self.plot_data = None
        self.plot_algo = ""
        self.plot_level = ""
        self._setup_ui()

    def _setup_ui(self):
        stats_container = tk.Frame(self, bg="#f0f0f0")
        stats_container.pack(fill=tk.X, expand=True, ipadx=5, ipady=10)
        
        diag_left = tk.Frame(stats_container, bg="#f0f0f0")
        diag_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        diag_right = tk.Frame(stats_container, bg="#f0f0f0")
        diag_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.step_label = tk.Label(diag_left, text="Step: 0 / 0", bg="#f0f0f0", font=('Arial', 11, 'bold'), fg="#D35400")
        self.step_label.pack(pady=(2, 5))
        self.nodes_label = tk.Label(diag_left, text="States Explored: -", bg="#f0f0f0", font=('Arial', 10))
        self.nodes_label.pack(pady=2)
        
        self.time_label = tk.Label(diag_right, text="Time: -", bg="#f0f0f0", font=('Arial', 10))
        self.time_label.pack(pady=(2, 5))
        self.memory_label = tk.Label(diag_right, text="Peak Memory: -", bg="#f0f0f0", font=('Arial', 10))
        self.memory_label.pack(pady=2)

    def update_stats(self, step, max_step, nodes, time_ms, memory_mb):
        self.step_label.config(text=f"Step: {step} / {max_step}")
        self.nodes_label.config(text=f"States Explored: {nodes}")
        self.time_label.config(text=f"Time: {time_ms:.2f} ms")
        self.memory_label.config(text=f"Peak Memory: {memory_mb:.4f} MB")

    def update_step_only(self, step, max_step):
        self.step_label.config(text=f"Step: {step} / {max_step}")

    def reset_stats(self):
        self.step_label.config(text="Step: 0 / 0")
        self.nodes_label.config(text="States Explored: -")
        self.time_label.config(text="Time: -")
        self.memory_label.config(text="Peak Memory: -")

    def show_plot(self, data, algo_name, level_name):
        """Hàm độc lập để vẽ biểu đồ"""
        if not data: return 
        x_steps = sorted(list(data.keys()))
        y_counts = [data[step] for step in x_steps]

        color = "#2980B9" if algo_name == "A*" else "#D35400"

        plt.figure(figsize=(9, 5))
        plt.bar(x_steps, y_counts, color=color, edgecolor='white' if len(x_steps) < 100 else 'none')
        plt.title(f'Statistics - {algo_name} ({level_name})', fontsize=14, fontweight='bold')
        plt.xlabel('Number of step (Depth / Path Length)', fontsize=12)
        plt.ylabel('Number of searching in step (Nodes Evaluated)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()