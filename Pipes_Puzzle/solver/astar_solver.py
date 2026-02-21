import heapq
from .base_solver import BasePipesSolver
from .state_and_node import Node, generate_successors

class AStarSolver(BasePipesSolver):
    def _run_algorithm(self) -> bool:
        open_list = []
        visited = set()
        counter = 0 
        
        first_node = Node(self.initial_state, [2,2], None)
        heapq.heappush(open_list, (self.fx(first_node), counter, first_node))
        
        while open_list:
            if self._stopped:
                return False
                
            _, _, current_node = heapq.heappop(open_list)
            self.depth_counts[current_node.step] = self.depth_counts.get(current_node.step, 0) + 1
            
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
                    score = self.fx(item)
                    counter += 1
                    heapq.heappush(open_list, (score, counter, item))
                    
        return False

    def fx(self, current: Node) -> int:
        return self.gx(current) + self.hx(current)
        
    def gx(self, current: Node) -> int:
        return current.step * 2
        
    def hx(self, current: Node) -> int:
        ans = -5 * current.state.countBump
        if current.previous != None:
            if current.state.countBump == current.previous.state.countBump:
                s = False
                for i in range(5):
                    for j in range(5):
                        if current.state.head[i][j]["bump"] != current.previous.state.head[i][j]["bump"]:
                            ans -= 2
                            s = not(s)
                        elif current.state.head[i][j]["bump"] and current.previous.state.head[i][j]["bump"]:
                            if current.state.head[i][j]["heading"] != current.previous.state.head[i][j]["heading"]:
                                ans -= 2
                                s = not(s)
                        if s: break
                    if s: break
                if not(s): ans += 2
        
        if current.state.countBump:
            for i in [0,4]:
                for j in range(5):
                    list1 = current.state.getAngle(current.state.head[i][j])
                    if i == 0:
                        if 90 in list1:
                            ans += 1
                            if current.state.head[i][j]["bump"]: ans += 5
                        else: ans -= 2
                    elif i == 4:
                        if 270 in list1:
                            ans += 1
                            if current.state.head[i][j]["bump"]: ans += 5
                        else: ans -= 2
            
            for j in [0,4]:
                for i in range(5):
                    list1 = current.state.getAngle(current.state.head[i][j])
                    if j == 0:
                        if 180 in list1:
                            ans += 1
                            if current.state.head[i][j]["bump"]: ans += 5
                        else: ans -= 2
                    elif j == 4:
                        if 0 in list1:
                            ans += 1   
                            if current.state.head[i][j]["bump"]: ans += 5
                        else: ans -= 2     

        if current.state.checkRecursionBump(current.rotate[0], current.rotate[1]):
            ans += 2000
        return ans