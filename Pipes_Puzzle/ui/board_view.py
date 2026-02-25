"""
BoardView: Canvas vẽ bảng 5x5 và các ống theo type/heading.
Ô có nước màu xanh, không nước màu trắng; ô trung tâm đánh dấu đỏ.
"""
import tkinter as tk


class BoardView(tk.Frame):
    CELL_SIZE = 70
    GRID_SIZE = 5
    BOARD_SIZE = CELL_SIZE * GRID_SIZE

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, width=self.BOARD_SIZE, height=self.BOARD_SIZE, 
                                bg='#FAFAFA', highlightthickness=2, highlightbackground="#333")
        self.canvas.pack()

    def draw_board(self, state_matrix):
        """Vẽ lại toàn bộ bảng theo ma trận trạng thái hiện tại."""
        self.canvas.delete("all") 
        self._draw_grid_lines()
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                self._draw_vector_pipe(r, c, state_matrix[r][c])

    def _draw_grid_lines(self):
        grid_color = '#B0B0B0' 
        for i in range(self.GRID_SIZE):
            pos = i * self.CELL_SIZE
            self.canvas.create_line(pos, 0, pos, self.BOARD_SIZE, fill=grid_color, dash=(2, 2))
            self.canvas.create_line(0, pos, self.BOARD_SIZE, pos, fill=grid_color, dash=(2, 2))

    def _draw_vector_pipe(self, row, col, pipe_data):
        pipe_type = pipe_data["type"]
        heading = pipe_data["heading"]
        is_bump = pipe_data.get("bump", False)
        
        render_row = (self.GRID_SIZE - 1) - row 
        cx = col * self.CELL_SIZE + self.CELL_SIZE // 2
        cy = render_row * self.CELL_SIZE + self.CELL_SIZE // 2
        
        pipe_color = "#5DADE2" if is_bump else "white" 
        outline_color = "#2C3E50"
        pipe_width = 16
        outline_width = 24
        border_thick = (outline_width - pipe_width) // 2 
        
        dirs = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}
        
        angles = []
        if pipe_type == 1: angles = [heading]
        elif pipe_type == 2: angles = [heading, (heading + 180) % 360]
        elif pipe_type == 3: angles = [heading, (heading + 90) % 360]
        elif pipe_type == 4: angles = [(heading - 90) % 360, heading, (heading + 90) % 360]
        
        for a in angles:
            dx, dy = dirs[a]
            ex = cx + dx * (self.CELL_SIZE // 2)
            ey = cy + dy * (self.CELL_SIZE // 2)
            self.canvas.create_line(cx, cy, ex, ey, fill=outline_color, width=outline_width, tags="pipe", capstyle=tk.BUTT)
        
        if len(angles) >= 2:
            r_out = outline_width // 2
            self.canvas.create_rectangle(cx - r_out, cy - r_out, cx + r_out, cy + r_out, fill=outline_color, outline="", tags="pipe")

        for a in angles:
            dx, dy = dirs[a]
            ex = cx + dx * (self.CELL_SIZE // 2)
            ey = cy + dy * (self.CELL_SIZE // 2)
            self.canvas.create_line(cx, cy, ex, ey, fill=pipe_color, width=pipe_width, tags="pipe", capstyle=tk.BUTT)
            
        if len(angles) >= 2:
            r_in = pipe_width // 2
            self.canvas.create_rectangle(cx - r_in, cy - r_in, cx + r_in, cy + r_in, fill=pipe_color, outline="", tags="pipe")
        
        r_dot = int(outline_width / 1.5) 

        if pipe_type == 1:
            self.canvas.create_oval(cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot, fill=pipe_color, outline=outline_color, width=border_thick, tags="pipe")
            
        if row == 2 and col == 2:
            self.canvas.create_oval(cx - r_dot, cy - r_dot, cx + r_dot, cy + r_dot, fill="#E74C3C", outline="#7B241C", width=border_thick, tags="pipe")