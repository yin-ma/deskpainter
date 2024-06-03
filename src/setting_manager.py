import configparser


class SettingManager:
    def __init__(self, file_path):
        self.config_parser = configparser.ConfigParser()
        self.setting = {}
        self._init(file_path)

    def _init(self, file_path):
        self.config_parser.read(file_path, encoding="utf-8")

        for k in self.config_parser["SETTING"]:
            self.setting[k] = self.config_parser["SETTING"][k]

    def get_config_by_key(self, key):
        return self.setting[key]

    def set_config_by_key(self, key, val):
        self.setting[key] = val

    def save_config(self):
        pass
