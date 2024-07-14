import tkinter as tk
import ast
from PIL import Image, ImageTk


class PenPanel(tk.Frame):
    def __init__(self, root):
        self.setting = root.setting
        super().__init__(root.get_widget_by_tag("panel"), background=self.setting.get_config_by_key("transparent_color"))
        self.root = root
        self.pen_butt = root.get_widget_by_tag("panel")
        self.transparent_color = self.setting.get_config_by_key("transparent_color")
        self.pen_butts = self.pen_butt.butts_dict
        self.img_size = int(self.setting.get_config_by_key("butts_size"))
        self.panel_hig = int(self.setting.get_config_by_key("panel_hig"))
        self.panel_wid = int(self.setting.get_config_by_key("panel_wid"))
        self.img = ImageTk.PhotoImage(Image.open("../res/default_button.png").resize((self.img_size//2, self.img_size//2)))
        self.font = tk.font.Font(font=f"{self.setting.get_config_by_key('app_font')} {max(self.img_size // 4 - 10, 15)} bold")

        self.pen_size_lst = ast.literal_eval(self.setting.get_config_by_key("pen_size"))
        self.butt_dict = {}
        self.init_panel()
        self.init_butts()

    def get_butts(self):
        return self.butt_dict

    def init_butts(self):
        temp = tk.Button(self,
                         image=self.img,
                         bg=self.transparent_color,
                         activebackground=self.transparent_color,
                         highlightthickness=0,
                         bd=0,
                         wraplength=0,
                         compound="center",
                         justify="center",
                         text=f"B",
                         font=self.font)
        self.butt_dict["b"] = temp
        temp.pack(anchor=tk.SE)
        temp.pack_forget()

        size = len(self.pen_size_lst)
        for b in self.pen_size_lst:
            temp = tk.Button(self,
                             image=self.img,
                             bg=self.transparent_color,
                             activebackground=self.transparent_color,
                             highlightthickness=0,
                             bd=0,
                             wraplength=0,
                             compound="center",
                             justify="center",
                             text=f"{size}",
                             font=self.font)
            self.butt_dict[size] = temp
            temp.pack(anchor=tk.SE)
            temp.pack_forget()

            size -= 1

    def init_panel(self):
        rel_x = 1 - (self.img_size + 0.1*self.img_size) / self.panel_wid
        y_offset = (self.img_size + 0.1*self.img_size) / self.panel_hig
        rel_y = 1.0

        for b in self.pen_butts:
            if b == "pen_butt":
                rel_y += y_offset * 0.5
                break
            rel_y -= y_offset

        self.place(relx=rel_x, rely=rel_y, anchor=tk.SE)
