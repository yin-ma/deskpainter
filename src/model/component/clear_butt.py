class ClearButt:
    def __init__(self, main_activity):
        self.main_activity = main_activity
        self.butt = main_activity.get_widget_by_tag("panel").get_butt_by_tag("clear_butt")
        self.canvas = main_activity.get_widget_by_tag("canvas").canvas
        self.butt.bind('<Double-Button-1>', lambda event: self.clear())

    def clear(self):
        self.canvas.delete("all")
        self.main_activity.data_manager.line_history.clear()
        if self.main_activity.data_manager.redo_history:
            self.main_activity.data_manager.redo_history.clear()
