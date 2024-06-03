class RedoButt:
    def __init__(self, main_activity):
        self.data_manager = main_activity.data_manager
        self.butt = main_activity.get_widget_by_tag("panel").get_butt_by_tag("redo_butt")
        self.canvas = main_activity.get_widget_by_tag("canvas").canvas

        self.butt.bind('<Button-1>', lambda event: self.redo())

    def redo(self):
        if self.data_manager.redo_history:
            obj, arg = self.data_manager.redo()
            line_id = self.canvas.create_line(obj, **arg)
            self.data_manager.add_line(line_id)
            self.data_manager.add_history(obj, arg)
