class PenButt:
    def __init__(self, main_activity):
        self.main_activity = main_activity
        self.data_manager = main_activity.data_manager
        self.butt = main_activity.get_widget_by_tag("panel").butts_dict["pen_butt"]
        self.eraser = main_activity.get_widget_by_tag("pen_color_panel").eraser_butt

        self.butt.bind('<Button-1>', lambda event: self.show_panel())

    def show_panel(self):
        if self.data_manager.num_pen_butt_clicks % 2 == 1:
            for k, v in self.main_activity.get_widget_by_tag("pen_panel").butt_dict.items():
                v.pack_forget()

            for k, v in self.main_activity.get_widget_by_tag("pen_color_panel").butt_dict.items():
                v.pack_forget()

            self.eraser.pack_forget()
        else:
            for k, v in self.main_activity.get_widget_by_tag("pen_panel").butt_dict.items():
                v.pack()

            for k, v in self.main_activity.get_widget_by_tag("pen_color_panel").butt_dict.items():
                v.pack()

            self.eraser.pack()
        self.data_manager.num_pen_butt_clicks += 1
