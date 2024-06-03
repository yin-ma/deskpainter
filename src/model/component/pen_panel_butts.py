class PenPanelButts:
    def __init__(self, main_activity):
        self.data_manager = main_activity.data_manager
        self.butt_dict = main_activity.get_widget_by_tag("pen_panel").butt_dict
        self.size_lst = main_activity.get_widget_by_tag("pen_panel").pen_size_lst

        self.line_options = self.data_manager.line_options

        for size in self.butt_dict:
            self.butt_dict[size].bind("<Button-1>", lambda event, s=size: self.pen_size(s))

    def pen_size(self, size):
        self.line_options["width"] = self.size_lst[size-1]
