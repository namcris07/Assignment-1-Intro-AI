# -*- coding: utf-8 -*-
import sys
import os
from solver.backtracking_solver import BacktrackingSolver
from solver.astar_csp_solver import AStarCSPSolver
from performance.memory import PerformanceTracker

def read_board_from_file(filepath):
    board = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                row = [int(x) for x in line.strip().split()]
                board.append(row)
    return board

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    easy_dir = os.path.join(base_dir, "input", "easy")
    hard_dir = os.path.join(base_dir, "input", "hard")
    
    test_cases = []
    
    # Read easy boards
    if os.path.exists(easy_dir):
        for filename in sorted(os.listdir(easy_dir)):
            if filename.endswith(".txt"):
                filepath = os.path.join(easy_dir, filename)
                test_cases.append((f"Easy - {filename}", read_board_from_file(filepath)))
                
    # Read hard boards
    if os.path.exists(hard_dir):
        for filename in sorted(os.listdir(hard_dir)):
            if filename.endswith(".txt"):
                filepath = os.path.join(hard_dir, filename)
                test_cases.append((f"Hard - {filename}", read_board_from_file(filepath)))

    tracker = PerformanceTracker()
    
    report_path = os.path.join(base_dir, "benchmark_results.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("| Test Case | Thuật toán | Thời gian (ms) | Bộ nhớ (MB) | Số bước | Số trạng thái | Kết quả |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        for name, board in test_cases:
            # Run Backtracking
            res_bt = tracker.measure_all(BacktrackingSolver, board)
            status_bt = "Thành công" if res_bt['success'] else "Thất bại"
            f.write(f"| {name} | Backtracking | {res_bt['time_ms']:.2f} | {res_bt['memory_mb']:.4f} | {res_bt['steps']} | {res_bt['states']} | {status_bt} |\n")
            
            # Run A* CSP
            res_astar = tracker.measure_all(AStarCSPSolver, board)
            status_astar = "Thành công" if res_astar['success'] else "Thất bại"
            f.write(f"| {name} | A* + CSP | {res_astar['time_ms']:.2f} | {res_astar['memory_mb']:.4f} | {res_astar['steps']} | {res_astar['states']} | {status_astar} |\n")

if __name__ == "__main__":
    main()
