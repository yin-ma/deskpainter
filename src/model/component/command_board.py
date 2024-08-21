import tkinter as tk
from PIL import Image, ImageTk, ImageGrab

import sys
import subprocess
import json
import os


class CommandBoard:
    def __init__(self, main_activity):
        self.main_activity = main_activity
        self.data_manager = main_activity.data_manager
        self.butt = main_activity.get_widget_by_tag("panel").get_butt_by_tag("command_butt")

        self.board = self.main_activity.get_widget_by_tag("command_board")
        self.text_box = self.board.main_display.text_box
        self.entry = self.board.main_display.entry
        self.command = Command(self)

        self.entry.bind("<Control-Return>", lambda event: self.send_entry())
        self.butt.bind('<Button-1>', lambda event: self.hide_board())

    def hide_board(self):
        if self.data_manager.num_command_butt_clicks % 2 == 1:
            self.board.withdraw()
        else:
            self.board.deiconify()
        self.data_manager.num_command_butt_clicks += 1

    def create_new_line(self):
        pass

    def append_text(self, s):
        self.text_box.config(state="normal")
        self.text_box.insert(tk.END, s + "\n")
        self.text_box.config(state="disabled")
        self.text_box.see(tk.END)

    def send_entry(self):
        s = self.entry.get(1.0, tk.END)
        self.del_entry()
        self.append_text(s)
        if s.startswith("/"):
            command, *args = s.split()
            self.execute_command(command, args)

        return "break"

    def del_entry(self):
        self.entry.delete("1.0", tk.END)

    def execute_command(self, command, args):
        if command in self.command.command:
            self.command.command[command](args)
        else:
            self.append_text("command doesn't exist.")


class Command:
    def __init__(self, command_board):
        self.command_board = command_board
        self.text_box = command_board.text_box
        self.entry = command_board.entry

        self.command = {
            "/help": self.show_help,
            "/?": self.show_help,
            "/clear": self.clear_board,
            "/pen_size": self.set_pen_size,
            "/pen_color": self.set_pen_color,
            "/border_mode": self.set_border_mode,
            "/border_color": self.set_border_color,
            "/border_size": self.set_border_size,
            "/bg": self.set_bg,
            "/save": self.save_locus,
            "/load": self.load_locus,
            "/loadbg": self.load_bg,
            "/rmbg": self.remove_bg,
            "/sc": self.screenshot,
            "/quit": sys.exit,
            "/exit": sys.exit,
        }

    def set_border_color(self, args):
        self.command_board.data_manager.border_line_options["fill"] = args

    def set_border_size(self, args):
        self.command_board.data_manager.border_line_options["width"] = args

    def set_border_mode(self, args):
        if not args:
            self.command_board.data_manager.border_mode = False
            return
        if len(args) == 1:
            print(args)
            if args[0] == "1":
                self.command_board.data_manager.border_mode = True
            else:
                self.command_board.data_manager.border_mode = False

    def set_bg(self, args):
        if not args:
            self.command_board.append_text("require args")
        elif len(args) == 1:
            canvas = self.command_board.main_activity.canvas.canvas
            try:
                canvas.config(bg=args)
            except:
                self.command_board.append_text("invalid color")
        else:
            self.command_board.append_text("invalid args")

    def save_locus(self, args):
        if not args:
            self.command_board.append_text("require file name")
        elif len(args) == 1:
            locus = self.command_board.data_manager.line_history
            with open(f'../save/{args[0]}.locus', 'w') as f:
                json.dump(locus, f)
            self.command_board.append_text("locus saved")
        else:
            self.command_board.append_text("invalid file name")

    def load_locus(self, args):
        if not args:
            self.command_board.append_text("require file name")
        elif len(args) == 1:
            file_name = args[0]
            f_is_exist = os.path.isfile(f"../save/{file_name}.locus")
            if f_is_exist:
                with open(f"../save/{file_name}.locus", "r") as f:
                    temp = json.load(f)

                self.command_board.main_activity.clear_butt.clear()
                for obj, arg in temp:
                    self.command_board.data_manager.line_history.append([obj, arg])
                    self.command_board.data_manager.line = self.command_board.main_activity.get_widget_by_tag(
                        "canvas").canvas.create_line(
                        obj, **arg)
                    self.command_board.data_manager.line_id.append(self.command_board.data_manager.line)
                self.command_board.append_text(f"locus loaded")
            else:
                self.command_board.append_text(f"invalid file name")
        else:
            self.command_board.append_text("invalid file name")

    def screenshot(self, args):
        def sc():
            x0 = canvas.winfo_rootx()
            y0 = canvas.winfo_rooty()
            x1 = x0 + canvas.winfo_width()
            y1 = y0 + canvas.winfo_height()

            im = ImageGrab.grab((x0, y0, x1, y1))
            filename = "../save/df.png"
            if len(args) == 1:
                filename = f"../save/{args[0]}.png"
            im.save(filename)
            self.command_board.board.deiconify()
            self.command_board.main_activity.hide_butt.show_panel()
            self.command_board.append_text(f"screenshot saved as {filename}")
        canvas = self.command_board.main_activity.canvas.canvas
        self.command_board.main_activity.hide_butt.hide_panel()
        self.command_board.main_activity.hide_butt.butt_dict["hide_butt"].place_forget()
        self.command_board.board.withdraw()
        self.command_board.main_activity.widget_manager.after(100, sc)

    def remove_bg(self, args):
        canvas = self.command_board.main_activity.canvas.canvas
        data_manager = self.command_board.main_activity.data_manager
        data_manager.bg = None
        canvas.delete("all")
        for obj, arg in self.command_board.main_activity.data_manager.line_history:
            line_id = canvas.create_line(obj, **arg)
        self.command_board.append_text(f"background cleared")

    def load_bg(self, args):
        if not args or len(args) == 1:
            file_name = "df"
            if len(args) == 1:
                file_name = args[0]
            f_is_exist = os.path.isfile(f"../save/{file_name}.png")

            if f_is_exist:
                canvas = self.command_board.main_activity.canvas.canvas
                data_manager = self.command_board.main_activity.data_manager
                data_manager.bg = ImageTk.PhotoImage(Image.open(f"../save/{file_name}.png"))
                width, height = canvas.winfo_width(), canvas.winfo_height()

                line_history = data_manager.line_history.copy()

                self.command_board.main_activity.clear_butt.clear()
                canvas.create_image(width*0.5, height*0.5, image=data_manager.bg)
                self.command_board.append_text(f"background loaded as {file_name}.png")

                data_manager.line_history = line_history.copy()

                for obj, arg in line_history:
                    line_id = canvas.create_line(obj, **arg)
                    data_manager.add_line(line_id)
            else:
                self.command_board.append_text(f"invalid file name")
        else:
            self.command_board.append_text("invalid file name")

    def set_pen_size(self, args):
        self.command_board.data_manager.line_options["width"] = args

    def set_pen_color(self, args):
        self.command_board.data_manager.line_options["fill"] = args

    def clear_board(self, args):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete("1.0", tk.END)
        self.text_box.config(state=tk.DISABLED)

    def show_help(self, args):
        for c in self.command:
            self.command_board.append_text(c)



