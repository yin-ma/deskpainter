from .widget.canvas import Canvas
from .widget.panel import Panel
from .widget.pen_panel import PenPanel
from .widget.pen_color_panel import PenColorPanel
from .widget.command_board import CommandBoard

import tkinter as tk
import sys


class WidgetManager(tk.Tk):
    def __init__(self, setting):
        super().__init__()
        self.title(setting.get_config_by_key("main_title"))
        self.attributes("-alpha", 0.01)
        self.attributes('-fullscreen', True)
        self.setting = setting
        self.widget = {}
        self.registry()
        self.bind('<Escape>', lambda event: sys.exit())

    def registry(self):
        self.add_widget("view", self)

        # main drawing canvas
        self.add_widget("canvas", Canvas(self))

        # panel component
        self.add_widget("panel", Panel(self))
        self.add_widget("pen_panel", PenPanel(self))
        self.add_widget("pen_color_panel", PenColorPanel(self))
        self.add_widget("command_board", CommandBoard(self))

    def add_widget(self, key, obj):
        self.widget[key] = obj

    def get_widget_by_tag(self, tag):
        return self.widget[tag]

    def get_widget_by_id(self, i):
        pass

    def run(self):
        self.mainloop()
