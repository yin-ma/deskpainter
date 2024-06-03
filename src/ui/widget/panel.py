import tkinter as tk
import yaml
from PIL import Image, ImageTk
import sys
import tkinter.font


class Panel(tk.Toplevel):
    def __init__(self, root):
        super(Panel, self).__init__(root)
        self.root = root
        self.setting = root.setting

        # window attributes
        self.title = self.setting.get_config_by_key("panel_title")
        self.transparent_color = self.setting.get_config_by_key("transparent_color")
        self.wm_attributes('-transparentcolor', self.transparent_color)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.lift()

        # geometry
        self.root_wid, self.root_hig = root.winfo_screenwidth(), root.winfo_screenheight()
        self.panel_wid, self.panel_hig = int(self.setting.get_config_by_key("panel_wid")), int(self.setting.get_config_by_key("panel_hig"))
        self.geometry(f"{self.panel_wid}x{self.panel_hig}+{self.root_wid - self.panel_wid - 10}+{self.root_hig - self.panel_hig - 10}")

        # init bg
        self.panel_canvas = tk.Canvas(self, bg=self.transparent_color, highlightthickness=0)
        self.panel_canvas.pack(fill="both", expand=True)

        # init butts
        self.img_size = int(self.setting.get_config_by_key("butts_size"))
        self.font = tk.font.Font(font=f"{self.setting.get_config_by_key('app_font')} {self.img_size // 2 - 10} bold")
        self.butt_img = ImageTk.PhotoImage(Image.open("../res/default_button.png").resize((self.img_size, self.img_size)))
        self.num_items = 0
        self.butts = yaml.safe_load(self.setting.get_config_by_key("butts"))
        self.butts_dict = self.init_butts()
        self.top_window()
        self.bind('<Escape>', lambda event: sys.exit())

    def top_window(self):
        refresh_time = int(self.setting.get_config_by_key("refresh_time"))
        self.lift()
        self.after(refresh_time, lambda: self.top_window())
        self.update()

    def get_butt_by_tag(self, tag):
        return self.butts_dict[tag]

    def init_butts(self):
        butts_dict = {}
        rel_x = 1.0
        y_offset = (self.img_size + 0.1*self.img_size) / self.panel_hig
        rel_y = 1.0

        for b in self.butts:
            temp = tk.Button(self.panel_canvas,
                             image=self.butt_img,
                             bg=self.transparent_color,
                             activebackground=self.transparent_color,
                             highlightthickness=0,
                             bd=0,
                             text=self.butts[b],
                             wraplength=0,
                             compound="center",
                             justify="center",
                             font=self.font,
                             )
            temp.place(relx=rel_x, rely=rel_y, anchor=tk.SE)
            butts_dict[b] = temp
            rel_y -= y_offset
        return butts_dict




