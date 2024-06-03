class PenColorPanelButts:
    def __init__(self, main_activity):
        self.main_activity = main_activity
        self.data_manager = main_activity.data_manager
        self.setting = main_activity.setting
        self.butt_dict = self.main_activity.get_widget_by_tag("pen_color_panel").butt_dict
        self.color_lst = self.main_activity.get_widget_by_tag("pen_color_panel").pen_color_lst

        self.line_options = self.data_manager.line_options
        self.transparent_color = self.setting.get_config_by_key("transparent_color")

        for color in self.butt_dict:
            self.butt_dict[color].bind("<Button-1>", lambda event, c=color: self.pen_color(c))

        self.eraser_butt = self.main_activity.get_widget_by_tag("pen_color_panel").eraser_butt
        self.eraser_butt.bind("<Button-1>", lambda event: self.erase())

    def erase(self):
        self.line_options["fill"] = self.transparent_color

    def pen_color(self, color):
        self.line_options["fill"] = color
