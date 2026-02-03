# main.py
import tkinter as tk
from ui.main_gui import SudokuGUI

if __name__ == "__main__":
    root = tk.Tk()
    
    window_width = 900
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
    
    app = SudokuGUI(root)
    root.mainloop()