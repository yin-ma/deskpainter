import sys


class QuitButt:
    def __init__(self, main_activity):
        self.butt = main_activity.get_widget_by_tag("panel").get_butt_by_tag("quit_butt")
        self.butt.bind("<Button-1>", lambda event: self.quit())

    @staticmethod
    def quit():
        sys.exit()
