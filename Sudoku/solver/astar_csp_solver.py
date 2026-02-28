from typing import Callable, Optional, List, Tuple, Set, Dict

class AStarCSPSolver:
    def __init__(self, board: List[List[int]]):
        self.board = [row[:] for row in board]
        self.step_count = 0
        self.state_count = 0
        self._callback: Optional[Callable] = None
        self._stopped = False
        self.domains: Dict[Tuple[int, int], Set[int]] = {}

    def _initialize_domains(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    self.domains[(r, c)] = set(range(1, 10))
        
        for r in range(9):
            for c in range(9):
                if self.board[r][c] != 0:
                    val = self.board[r][c]
                    self._forward_check(r, c, val)

    def _forward_check(self, row: int, col: int, val: int) -> List[Tuple[int, int]]:
        changed = []

        for i in range(9):
            if i != col and (row, i) in self.domains and val in self.domains[(row, i)]:
                self.domains[(row, i)].remove(val)
                changed.append((row, i))
            if i != row and (i, col) in self.domains and val in self.domains[(i, col)]:
                self.domains[(i, col)].remove(val)
                changed.append((i, col))

        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if (r, c) != (row, col) and (r, c) in self.domains and val in self.domains[(r, c)]:
                    self.domains[(r, c)].remove(val)
                    changed.append((r, c))
        return changed

    def _restore_domains(self, changed_cells: List[Tuple[int, int]], val: int):
        for r, c in changed_cells:
            self.domains[(r, c)].add(val)

    def _calculate_f(self) -> float:

        g = len(self.domains)
        h = sum(1.0 / len(domain) for domain in self.domains.values() if len(domain) > 0)
        return g + h

    def _get_mrv_cell(self) -> Optional[Tuple[int, int]]:
        if not self.domains:
            return None
        
        min_len = 10
        best_cell = None
        for cell, domain in self.domains.items():
            if len(domain) < min_len:
                min_len = len(domain)
                best_cell = cell
                if min_len == 1:
                    break
        return best_cell

    def solve(self, step_callback: Optional[Callable] = None) -> bool:
        self._callback = step_callback
        self._stopped = False
        self.step_count = 0
        self.state_count = 0
        self.domains.clear()
        self._initialize_domains()
        return self._solve_recursive()

    def _solve_recursive(self) -> bool:
        self.state_count += 1
        if self._stopped:
            return False
            
        cell = self._get_mrv_cell()
        if not cell:
            return True 
            
        row, col = cell
        possible_values = list(self.domains[cell])
        
        if not possible_values:
            return False
            
        value_f_scores = []
        del self.domains[cell] 
        
        for val in possible_values:
            changed = self._forward_check(row, col, val)
            
            is_dead_end = any(len(self.domains[peer]) == 0 for peer in changed)
            
            if not is_dead_end:
                f_score = self._calculate_f()
                value_f_scores.append((f_score, val))
            else:
                value_f_scores.append((float('inf'), val))
                
            self._restore_domains(changed, val)
            
        value_f_scores.sort(key=lambda x: x[0])
        
        for f_score, val in value_f_scores:
            if f_score == float('inf'):
                continue 
                
            self.board[row][col] = val
            self.step_count += 1
            
            if self._callback:
                if not self._callback(row, col, val, False, self.step_count):
                    self._stopped = True
                    return False
                    
            changed = self._forward_check(row, col, val)
            
            if self._solve_recursive():
                return True
                
            self.board[row][col] = 0
            self.step_count += 1
            
            if self._callback:
                if not self._callback(row, col, 0, True, self.step_count):
                    self._stopped = True
                    return False
                    
            self._restore_domains(changed, val)

        self.domains[cell] = set(possible_values)
        return False
