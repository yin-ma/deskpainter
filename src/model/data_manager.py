class DataManager:
    def __init__(self, setting):
        self.num_main_butt_clicks = 0
        self.num_pen_butt_clicks = 0
        self.num_command_butt_clicks = 0

        self.line_id = []
        self.line_history = []
        self.redo_history = []
        self.bgImg = None
        self.bgColor = setting.get_config_by_key("transparent_color")

        self.border_mode = False
        self.border_line_options = {
            "fill": "#000000",
            "width": str(int(setting.get_config_by_key("default_pen_size")) + 5)
        }

        self.line_options = {
            "fill": setting.get_config_by_key("default_pen_color"),
            "width": setting.get_config_by_key("default_pen_size")
        }

        self.screen_id = 0
        self.num_screen = int(setting.get_config_by_key("num_screen"))
        self.screens = {
            i: {"line_history": [],
                "redo_history": [],
                "line_id": [],
                "bgImg": None,
                "bgColor": self.bgColor
                } for i in range(int(setting.get_config_by_key("num_screen")))
            }

    def add_line(self, line_id):
        self.line_id.append(line_id)

    def add_history(self, points, config):
        self.line_history.append([points, config])

    def undo(self):
        if self.line_history:
            obj, arg = self.line_history.pop(-1)
            self.redo_history.append([obj, arg])
            idx = self.line_id.pop(-1)
            return idx
        return -1

    def redo(self):
        return self.redo_history.pop(-1)

    def clear(self):
        self.line_id.clear()
        self.line_history.clear()
        self.redo_history.clear()

    def get_current_screen_id(self):
        return self.screen_id

    def change_screen(self):
        self.screens[self.screen_id]["line_history"] = self.line_history.copy()
        self.screens[self.screen_id]["line_id"] = self.line_id.copy()
        self.screens[self.screen_id]["redo_history"] = self.redo_history.copy()
        self.screens[self.screen_id]["bgImg"] = self.bgImg
        self.screens[self.screen_id]["bgColor"] = self.bgColor

        self.screen_id += 1
        self.screen_id = self.screen_id % self.num_screen
        self.clear()

        self.line_history = self.screens[self.screen_id]["line_history"]
        self.line_id = self.screens[self.screen_id]["line_id"]
        self.redo_history = self.screens[self.screen_id]["redo_history"]
        self.bgImg = self.screens[self.screen_id]["bgImg"]
        self.bgColor = self.screens[self.screen_id]["bgColor"]

        return self.screen_id, self.line_history

