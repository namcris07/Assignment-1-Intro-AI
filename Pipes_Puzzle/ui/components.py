import tkinter as tk

BUTTON_STYLES = {
    "primary": {"bg": "#4CAF50", "hover": "#45a049", "fg": "white", "active": "#3d8b40"},
    "warning": {"bg": "#FF9800", "hover": "#F57C00", "fg": "white", "active": "#E65100"},
    "secondary": {"bg": "#7F8C8D", "hover": "#606B6C", "fg": "white", "active": "#4A5354"}, 
    "nav": {"bg": "#3498DB", "hover": "#2980B9", "fg": "white", "active": "#21618C"},
}

class ModernButton(tk.Button):
    def __init__(self, master, text: str, command, style: str = "primary", **kwargs):
        self.colors = BUTTON_STYLES.get(style, BUTTON_STYLES["primary"])
        super().__init__(
            master, text=text, command=command,
            bg=self.colors["bg"], fg=self.colors["fg"],
            activebackground=self.colors["active"], activeforeground=self.colors["fg"],
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2",
            padx=15, pady=8, disabledforeground="#DDDDDD", **kwargs
        )
        self.bind("<Enter>", lambda e: self.config(bg=self.colors["hover"]) if self['state'] == 'normal' else None)
        self.bind("<Leave>", lambda e: self.config(bg=self.colors["bg"]) if self['state'] == 'normal' else None)