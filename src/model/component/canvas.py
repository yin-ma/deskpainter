class Canvas:
    def __init__(self, main_activity):
        self.main_activity = main_activity
        self.data_manager = main_activity.data_manager
        self.view = main_activity.get_widget_by_tag("view")
        self.canvas = main_activity.get_widget_by_tag("canvas").canvas
        self.setting = main_activity.setting
        self.isMoving = False
        self.isDrawing = False
        self.points = []
        self.line = None
        self.border = None
        self.prevMouseX = None
        self.prevMouseY = None
        self.totalMouseX = 0
        self.totalMouseY = 0

        self.line_options = self.data_manager.line_options
        self.border_line_options = self.data_manager.border_line_options

        self.view.bind("<Button-1>", self.mouse_down)
        self.view.bind('<B1-Motion>', self.mouse_move)
        self.view.bind('<ButtonRelease-1>', self.mouse_up)

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind('<B1-Motion>', self.mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)

        self.view.bind("<Control_L>", self.move_canvas)
        self.view.bind("<Control-KeyRelease>", self.stop_moving)
        self.main_activity.get_widget_by_tag("panel").bind("<Button-1>", self.change_focus)

    def change_focus(self, event):
        self.view.focus_set()

    def stop_moving(self, event):
        if self.isMoving:
            self.prevMouseY = None
            self.prevMouseX = None
            self.isMoving = False
            self.totalMouseX = 0
            self.totalMouseY = 0

    def move_canvas(self, event):
        if self.isDrawing:
            return
        self.isMoving = True
        self.prevMouseX = event.x
        self.prevMouseY = event.y

    def mouse_down(self, event):
        if not self.isMoving:
            self.isDrawing = True
            self.data_manager.redo_history.clear()

    def mouse_move(self, event):
        if not self.isMoving:
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
        if self.isMoving:
            for l in self.data_manager.line_id:
                self.canvas.move(l, event.x - self.prevMouseX, event.y - self.prevMouseY)
            self.totalMouseX += event.x - self.prevMouseX
            self.totalMouseY += event.y - self.prevMouseY
            self.prevMouseX = event.x
            self.prevMouseY = event.y

    def mouse_up(self, event):
        if not self.isMoving:
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

        if self.isMoving:
            for d in range(len(self.data_manager.line_history)):
                pos, config = self.data_manager.line_history[d]
                temp = []
                for i in range(0, len(pos), 2):
                    new_pos_x = pos[i] + self.totalMouseX
                    new_pos_y = pos[i + 1] + self.totalMouseY
                    temp.append(new_pos_x)
                    temp.append(new_pos_y)
                self.data_manager.line_history[d] = [temp, config]
            self.totalMouseX = 0
            self.totalMouseY = 0