"""
BFS (Breadth-First Search): Tìm kiếm theo chiều rộng.
Dùng hàng đợi (deque): lấy nút đầu, sinh successors thêm vào cuối.
Đảm bảo tìm được lời giải ngắn nhất (ít bước xoay nhất).
"""
from collections import deque
from .base_solver import BasePipesSolver
from .state_and_node import Node, generate_successors


class BFSSolver(BasePipesSolver):
    def _run_algorithm(self) -> bool:
        # Dùng deque của lib chuẩn giúp pop(0) có O(1) thay vì O(N) của List
        open_queue = deque()
        visited = set()
        
        first_node = Node(self.initial_state, [2,2], None)
        open_queue.append(first_node)
        
        while open_queue:
            if self._stopped:
                return False
                
            current_node = open_queue.popleft()
            
            if current_node.state.countBump == 25:
                self.path = self.get_path(current_node)
                return True
                
            if current_node.state in visited:
                continue
                
            visited.add(current_node.state)
            
            row, col = current_node.rotate[0], current_node.rotate[1]
            if not self.report_step(row, col, current_node.state.head):
                return False
                
            successors = generate_successors(current_node)
            for item in successors:
                if item.state not in visited:
                    open_queue.append(item)
                    
        return False