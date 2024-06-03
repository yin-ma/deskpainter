import tkinter as tk


class HideButt:
    def __init__(self, main_activity):
        self.butt = main_activity.get_widget_by_tag("panel").get_butt_by_tag("hide_butt")
        self.setting = main_activity.setting
        self.butt_dict = main_activity.get_widget_by_tag("panel").butts_dict

        self.main_activity = main_activity
        self.data_manager = main_activity.data_manager
        self.view = main_activity.widget_manager
        self.canvas = main_activity.get_widget_by_tag("canvas")
        self.panel = main_activity.get_widget_by_tag("panel")
        self.command_board = main_activity.get_widget_by_tag("command_board")
        self.pen_panel_dict = main_activity.get_widget_by_tag("pen_panel").butt_dict
        self.pen_color_dict = main_activity.get_widget_by_tag("pen_color_panel").butt_dict
        self.eraser = main_activity.get_widget_by_tag("pen_color_panel").eraser_butt

        self.butt.bind('<Button-1>', lambda event: self.hide())
        self.butt.bind('<B1-Motion>', lambda event: self.move_panel(event))

    def move_panel(self, event):
        img_size = int(self.setting.get_config_by_key("butts_size"))
        self.panel.geometry(f"+{self.panel.winfo_x() - img_size//2 + event.x}+{self.panel.winfo_y() - img_size//2 + event.y}")

    def show_panel(self):
        img_size = int(self.setting.get_config_by_key("butts_size"))
        panel_hig = int(self.setting.get_config_by_key("panel_hig"))
        rel_x = 1.0
        y_offset = (img_size + 0.1*img_size) / panel_hig
        rel_y = 1.0
        for b in self.butt_dict:
            self.butt_dict[b].place(relx=rel_x, rely=rel_y, anchor=tk.SE)
            rel_y -= y_offset

        if self.data_manager.num_pen_butt_clicks % 2 == 1:
            for b in self.pen_color_dict:
                self.pen_color_dict[b].pack()

            for b in self.pen_panel_dict:
                self.pen_panel_dict[b].pack()

            self.eraser.pack()

    def hide_panel(self):
        for b in self.butt_dict:
            if b == "hide_butt":
                continue
            self.butt_dict[b].place_forget()

        for b in self.pen_color_dict:
            self.pen_color_dict[b].pack_forget()

        for b in self.pen_panel_dict:
            self.pen_panel_dict[b].pack_forget()

        self.eraser.pack_forget()

    def hide(self):
        if self.data_manager.num_main_butt_clicks % 2 == 0:
            self.view.withdraw()
            self.canvas.withdraw()
            self.command_board.withdraw()
            self.hide_panel()
        else:
            self.view.deiconify()
            self.canvas.deiconify()
            self.show_panel()
            if self.data_manager.num_command_butt_clicks % 2 == 1:
                self.command_board.deiconify()

        self.data_manager.num_main_butt_clicks += 1
