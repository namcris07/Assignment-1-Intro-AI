"""
DFS (Depth-First Search): Tìm kiếm theo chiều sâu.
Dùng ngăn xếp (stack): lấy nút cuối, sinh successors thêm vào cuối.
Không đảm bảo lời giải ngắn nhất.
"""
from .base_solver import BasePipesSolver
from .state_and_node import Node, generate_successors


class DFSSolver(BasePipesSolver):
    def _run_algorithm(self) -> bool:
        open_list = []
        visited = set() # __hash__ --> Fast Set()
        
        first_node = Node(self.initial_state, [2,2], None)
        open_list.append(first_node)
        
        while open_list:
            if self._stopped:
                return False
                
            current_node = open_list.pop()
            
            if current_node.state.countBump == 25:
                self.path = self.get_path(current_node)
                return True
            
            # Depth Limited: Chỉ cho phép DFS đi sâu tối đa 3 bước
            # if current_node.step >= 3:
            #     continue 
                
            if current_node.state in visited:
                continue
                
            visited.add(current_node.state)
            
            row, col = current_node.rotate[0], current_node.rotate[1]
            if not self.report_step(row, col, current_node.state.head):
                return False

            successors = generate_successors(current_node)
            for item in successors:
                if item.state not in visited:
                    open_list.append(item)
                    
        return False