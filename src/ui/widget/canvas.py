import tkinter as tk
import sys


class Canvas(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title(root.setting.get_config_by_key("canvas_title"))
        self.wid, self.hig = root.winfo_screenwidth(), root.winfo_screenheight()
        self.transparent_color = root.setting.get_config_by_key("transparent_color")
        self.attributes('-transparentcolor', self.transparent_color)
        self.attributes("-topmost", True)
        self.geometry(f"{self.wid}x{self.hig}+0+0")
        self.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self, bg=self.transparent_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bind('<Escape>', lambda event: sys.exit())
