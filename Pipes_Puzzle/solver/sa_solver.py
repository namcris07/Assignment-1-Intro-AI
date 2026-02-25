"""
Simulated Annealing (SA): Thuật toán heuristic dựa trên mô phỏng ủ kim loại.
Mỗi bước chọn ngẫu nhiên 1 ô, xoay sang hướng khác. Chấp nhận nếu tốt hơn,
hoặc với xác suất exp(-Δ/T) nếu tệ hơn. Không đảm bảo tìm được lời giải.
"""
import math
import random
import copy
from .base_solver import BasePipesSolver
from .state_and_node import Node, State, HEADING


class SimulatedAnnealingSolver(BasePipesSolver):

    def __init__(self, initial_state,
                 initial_temp: float = 500.0,
                 cooling_rate: float = 0.9995,
                 min_temp: float = 0.001,
                 max_iterations: int = 80000):
        super().__init__(initial_state)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iterations = max_iterations

    def _generate_random_neighbor(self, current_node):
        """Sinh trạng thái kề: chọn ngẫu nhiên 1 ô, xoay sang hướng khác hợp lệ."""
    
        matrix = copy.deepcopy(current_node.state.head)

        r = random.randint(0, 4)
        c = random.randint(0, 4)

        current_heading = matrix[r][c]["heading"]
        pipe_type = matrix[r][c]["type"]

        if pipe_type == 2:
            possible = [h for h in [0, 90] if h != current_heading and h != (current_heading + 180) % 360]
            if not possible:
                possible = [90 if current_heading in [0, 180] else 0]
        else:
            possible = [h for h in HEADING if h != current_heading]

        new_heading = random.choice(possible)
        matrix[r][c]["heading"] = new_heading

        return Node(matrix, [r, c], current_node)

    def _quick_score(self, node):
        """Điểm đánh giá: số ô chưa có nước (25 - countBump). Mục tiêu = 0."""
        return 25 - node.state.countBump

    def _run_algorithm(self) -> bool:
        current_node = Node(self.initial_state, [2, 2], None)

        current_score = self._quick_score(current_node)
        best_node = current_node
        best_score = current_score

        temperature = self.initial_temp
        iteration = 0

        while temperature > self.min_temp and iteration < self.max_iterations:
            if self._stopped:
                return False

            self.step_count += 1

            self.depth_counts[current_node.step] = self.depth_counts.get(current_node.step, 0) + 1

            if current_score == 0:
                self.path = self.get_path(current_node)
                return True

            neighbor = self._generate_random_neighbor(current_node)
            neighbor_score = self._quick_score(neighbor)

            delta = neighbor_score - current_score

            if delta <= 0:
                accept = True
            else:
                try:
                    probability = math.exp(-delta / temperature)
                except OverflowError:
                    probability = 0.0
                accept = random.random() < probability

            if accept:
                current_node = neighbor
                current_score = neighbor_score

                self.step_count -= 1
                row, col = current_node.rotate[0], current_node.rotate[1]
                if not self.report_step(row, col, current_node.state.head):
                    return False

            if current_score < best_score:
                best_score = current_score
                best_node = current_node

            temperature *= self.cooling_rate
            iteration += 1

        if best_score == 0:
            self.path = self.get_path(best_node)
            return True

        print(f"SA ended: {iteration} iters, "
              f"best_bumps={best_node.state.countBump}/25, "
              f"temp={temperature:.6f}")
        self.path = self.get_path(best_node)
        return False