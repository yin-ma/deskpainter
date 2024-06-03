class ScrButt:
    def __init__(self, main_activity):
        self.main_activity = main_activity
        self.data_manager = main_activity.data_manager
        self.butt = main_activity.get_widget_by_tag("panel").get_butt_by_tag("scr_butt")
        self.setting = main_activity.setting
        self.canvas = main_activity.get_widget_by_tag("canvas").canvas

        self.num_screen = int(self.setting.get_config_by_key("num_screen"))

        self.butt.bind('<Button-1>', lambda event: self.switch_screen())

    def switch_screen(self):
        screen_id, line_history = self.data_manager.change_screen()
        self.canvas.delete("all")
        self.butt.config(text=f"{screen_id + 1}")
        if line_history:
            for obj, arg in line_history:
                line_id = self.canvas.create_line(obj, **arg)
                self.data_manager.add_line(line_id)

