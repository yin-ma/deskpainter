class UndoButt:
    def __init__(self, main_activity):
        self.data_manager = main_activity.data_manager
        self.butt = main_activity.get_widget_by_tag("panel").get_butt_by_tag("undo_butt")
        self.canvas = main_activity.get_widget_by_tag("canvas").canvas

        self.butt.bind('<Button-1>', lambda event: self.undo())

    def undo(self):
        idx = self.data_manager.undo()
        if idx != -1:
            self.canvas.delete(f"{idx}")
