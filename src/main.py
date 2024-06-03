from ui.widgetManager import WidgetManager
from model.main_activity import MainActivity
from setting_manager import SettingManager


if __name__ == "__main__":
    setting_manager = SettingManager("../setting.ini")
    widget_manager = WidgetManager(setting_manager)
    model = MainActivity(widget_manager, setting_manager)
    model.run()
