import tkinter as tk
import tkinter.font


class CommandBoard(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setting = root.setting
        self.title(self.setting.get_config_by_key("command_board_title"))
        self.transparent_color = self.setting.get_config_by_key("transparent_color")
        self.font_family = self.setting.get_config_by_key("command_font_family")
        self.font_size = self.setting.get_config_by_key("command_font_size")
        self.font = tk.font.Font(font=f'{self.font_family} {self.font_size} bold')
        self.root_wid = self.root.winfo_screenwidth()
        self.root_hig = self.root.winfo_screenheight()
        self.wid = int(self.setting.get_config_by_key("command_window_wid"))
        self.hig = int(self.setting.get_config_by_key("command_window_hig"))

        self.attributes("-topmost", True)
        self.wm_attributes('-transparentcolor', self.transparent_color)
        self.overrideredirect(True)
        self.init_window()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.main_display = MainDisplay(self.main_frame, self.setting)
        self.withdraw()

    def init_window(self):
        x_offset = self.root_wid // 2 - self.wid // 2
        y_offset = self.root_hig // 2 - self.hig // 2
        self.geometry(f"{self.wid}x{self.hig}+{x_offset}+{y_offset}")


class MainDisplay(tk.Frame):
    def __init__(self, root, setting):
        self.bg_color = "black" if setting.get_config_by_key("dark_mode") == "1" else "white"
        self.text_color = "white" if setting.get_config_by_key("dark_mode") == "1" else "black"
        super(MainDisplay, self).__init__(root, background=self.bg_color)
        self.root = root
        self.setting = setting
        self.transparent_color = setting.get_config_by_key("transparent_color")
        self.pack(fill="both", anchor=tk.NW, expand=True)

        self.wid = int(setting.get_config_by_key("command_window_wid"))
        self.text_box = tk.Text(self, bg=self.bg_color, foreground=self.text_color)
        self.text_box.place(x=0, y=0, relwidth=1.0, relheight=0.8)
        self.text_box.config(state="disabled")

        self.entry = tk.Text(self, bg=self.bg_color, foreground=self.text_color, insertbackground=self.text_color)
        self.entry.place(relx=0, rely=0.8, relwidth=1.0, relheight=0.2)