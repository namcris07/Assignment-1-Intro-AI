"""
Flask backend cho Pipes Puzzle Web.
API: POST /api/solve - giải puzzle, trả về path và thống kê.
"""
import sys
import os
import copy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from solver import DFSSolver, BFSSolver, AStarSolver, SimulatedAnnealingSolver, State
from data import TESTCASE
from performance.memory import PerformanceTracker
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")


@app.route("/")
def index():
    """Phục vụ trang chủ."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/levels")
def get_levels():
    """Trả về danh sách level có sẵn."""
    return jsonify(list(TESTCASE.keys()))


@app.route("/api/solve", methods=["POST"])
def solve():
    """
    Giải puzzle: nhận {level, algorithm}, trả về {success, path, time_ms, memory_mb, states_explored}.
    path: list các ma trận 5x5 (mỗi frame của animation).
    """
    try:
        data = request.get_json(silent=True) or {}
        level = data.get("level", "level 0")
        algorithm = data.get("algorithm", "A*")

        if level not in TESTCASE:
            return jsonify({"error": f"Level '{level}' không tồn tại"}), 400

        algo_map = {
            "DFS": DFSSolver,
            "BFS": BFSSolver,
            "A*": AStarSolver,
            "Simulated Annealing": SimulatedAnnealingSolver,
        }
        if algorithm not in algo_map:
            return jsonify({"error": f"Thuật toán '{algorithm}' không hợp lệ"}), 400

        initial_state = copy.deepcopy(TESTCASE[level])
        solver_class = algo_map[algorithm]
        solver = solver_class(initial_state)

        tracker = PerformanceTracker()
        tracker.memory_tracker.start()
        tracker.timer.start()

        result = solver.solve(step_callback=None)  # Không callback khi chạy API

        time_ms = tracker.timer.stop()
        mem_mb = tracker.memory_tracker.stop()

        path = list(solver.path) if solver.path else []

        return jsonify({
            "success": result,
            "path": path,
            "time_ms": round(float(time_ms), 2),
            "memory_mb": round(float(mem_mb), 4),
            "states_explored": solver.step_count,
            "path_length": len(path) - 1 if path else 0,
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500


@app.route("/api/initial/<level>")
def get_initial(level):
    """Trả về trạng thái ban đầu của level (để vẽ bảng trước khi Solve)."""
    if level not in TESTCASE:
        return jsonify({"error": f"Level '{level}' không tồn tại"}), 404
    state = State(copy.deepcopy(TESTCASE[level]))
    return jsonify(state.head)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
