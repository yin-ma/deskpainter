class PenPanelButts:
    def __init__(self, main_activity):
        self.data_manager = main_activity.data_manager
        self.butt_dict = main_activity.get_widget_by_tag("pen_panel").butt_dict
        self.size_lst = main_activity.get_widget_by_tag("pen_panel").pen_size_lst

        self.line_options = self.data_manager.line_options
        self.border_options = self.data_manager.border_line_options

        for char in self.butt_dict:
            if char == "b":
                self.butt_dict[char].bind("<Button-1>", lambda event, s=char: self.border_mode(s))
            else:
                self.butt_dict[char].bind("<Button-1>", lambda event, s=char: self.pen_size(s))

    def border_mode(self, args):
        self.data_manager.border_mode = ~self.data_manager.border_mode

    def pen_size(self, size):
        self.line_options["width"] = self.size_lst[size-1]
        self.border_options["width"] = str(int(self.size_lst[size-1]) + 5)
