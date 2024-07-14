class Canvas:
    def __init__(self, main_activity):
        self.main_activity = main_activity
        self.data_manager = main_activity.data_manager
        self.view = main_activity.get_widget_by_tag("view")
        self.canvas = main_activity.get_widget_by_tag("canvas").canvas
        self.setting = main_activity.setting
        self.isDrawing = False
        self.points = []
        self.line = None
        self.border = None

        self.line_options = self.data_manager.line_options
        self.border_line_options = self.data_manager.border_line_options

        self.view.bind("<Button-1>", self.mouse_down)
        self.view.bind('<B1-Motion>', self.mouse_move)
        self.view.bind('<ButtonRelease-1>', self.mouse_up)

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind('<B1-Motion>', self.mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)

    def mouse_down(self, event):
        self.isDrawing = True
        self.data_manager.redo_history.clear()

    def mouse_move(self, event):
        if self.isDrawing:
            self.points.extend([event.x, event.y])
            if len(self.points) == 4:
                if self.data_manager.border_mode:
                    self.border = self.canvas.create_line(self.points, **self.border_line_options)
                self.line = self.canvas.create_line(self.points, **self.line_options)
            elif len(self.points) >= 4:
                if self.data_manager.border_mode:
                    self.canvas.coords(self.border, self.points)
                self.canvas.coords(self.line, self.points)

    def mouse_up(self, event):
        self.isDrawing = False
        if len(self.points) >= 4:
            if self.data_manager.border_mode:
                self.data_manager.add_line(self.border)
                self.data_manager.add_history(self.points.copy(), self.border_line_options.copy())
            self.data_manager.add_line(self.line)
            self.data_manager.add_history(self.points.copy(), self.line_options.copy())
        self.points.clear()
        self.border = None
        self.line = None
