from .data_manager import DataManager

from .component.canvas import Canvas
from .component.quit_butt import QuitButt
from .component.redo_butt import RedoButt
from .component.undo_butt import UndoButt
from .component.clear_butt import ClearButt
from .component.scr_butt import ScrButt
from .component.hide_butt import HideButt
from .component.pen_butt import PenButt
from .component.pen_panel_butts import PenPanelButts
from .component.pen_color_panel_butts import PenColorPanelButts
from .component.command_board import CommandBoard


class MainActivity:
    def __init__(self, widget_manager, setting):
        self.widget_manager = widget_manager
        self.data_manager = DataManager(setting)
        self.setting = setting

        # add functionality to this app
        self.canvas = Canvas(self)
        self.quit_butt = QuitButt(self)
        self.command_butt = CommandBoard(self)
        self.scr_butt = ScrButt(self)
        self.undo_butt = UndoButt(self)
        self.redo_butt = RedoButt(self)
        self.pen_butt = PenButt(self)
        self.clear_butt = ClearButt(self)
        self.hide_butt = HideButt(self)

        # tiny-butts
        self.pen_panel_butts = PenPanelButts(self)
        self.pen_color_panel_butts = PenColorPanelButts(self)

    def get_widget_by_tag(self, tag):
        return self.widget_manager.get_widget_by_tag(tag)

    def run(self):
        self.widget_manager.run()
