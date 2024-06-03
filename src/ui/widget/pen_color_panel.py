import tkinter as tk
import ast
from PIL import Image, ImageTk
from PIL import ImageColor


class PenColorPanel(tk.Frame):
    def __init__(self, root):
        self.setting = root.setting
        super().__init__(root.get_widget_by_tag("panel"), background=self.setting.get_config_by_key("transparent_color"))
        self.root = root
        self.pen_butt = root.get_widget_by_tag("pen_panel").pen_butt
        self.transparent_color = self.setting.get_config_by_key("transparent_color")
        self.butts = self.pen_butt.butts_dict
        self.img_size = int(self.setting.get_config_by_key("butts_size"))
        self.panel_hig = int(self.setting.get_config_by_key("panel_hig"))
        self.panel_wid = int(self.setting.get_config_by_key("panel_wid"))
        self.font = tk.font.Font(font=f"{self.setting.get_config_by_key('app_font')} {max(self.img_size // 4 - 10, 15)} bold")

        self.pen_color_lst = ast.literal_eval(self.setting.get_config_by_key("pen_color"))
        self.img_lst = [CustomImage(Image.open("../res/button_color.png").resize((self.img_size//2, self.img_size//2)), c) for c in
                        self.pen_color_lst]
        self.eraser_img = ImageTk.PhotoImage(Image.open("../res/default_button.png").resize((self.img_size//2, self.img_size//2)))
        self.eraser_butt = None
        self.butt_dict = {}
        self.init_panel()
        self.init_butts()

    def get_butts(self):
        return self.butt_dict

    def init_butts(self):
        # pens
        for num, c in enumerate(self.pen_color_lst):
            temp = tk.Button(self,
                             image=self.img_lst[num],
                             bg=self.transparent_color,
                             activebackground=self.transparent_color,
                             highlightthickness=0,
                             bd=0,
                             wraplength=0,
                             compound="center",
                             justify="center",
                             text=" ",
                             font=self.font)
            temp.pack(anchor=tk.SE)
            temp.pack_forget()
            self.butt_dict[c] = temp

        # eraser
        temp = tk.Button(self,
                         image=self.eraser_img,
                         bg=self.transparent_color,
                         activebackground=self.transparent_color,
                         highlightthickness=0,
                         bd=0,
                         wraplength=0,
                         compound="center",
                         justify="center",
                         text=" ",
                         font=self.font)
        temp.pack(anchor=tk.SE)
        temp.pack_forget()
        self.eraser_butt = temp

    def init_panel(self):
        rel_x = 1 - (self.img_size + 0.1*self.img_size) / self.panel_wid - (self.img_size // 2 + 0.1*self.img_size // 2) / \
                self.panel_wid
        y_offset = (self.img_size + 0.1*self.img_size) / self.panel_hig
        rel_y = 1.0

        for b in self.butts:
            if b == "pen_butt":
                rel_y += y_offset*0.25
                break
            rel_y -= y_offset

        self.place(relx=rel_x, rely=rel_y, anchor=tk.SE)


class CustomImage(ImageTk.PhotoImage):
    def __init__(self, img, target_color):
        color = ImageColor.getcolor(target_color, "RGB")
        new_imgdata = []
        for c in img.getdata():
            if c[0] == c[1] == c[2] == 0:
                new_imgdata.append(c)
            else:
                new_imgdata.append(color)

        new_img = Image.new(img.mode, img.size)
        new_img.putdata(new_imgdata)

        super().__init__(new_img)
