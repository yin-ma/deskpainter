import tkinter as tk
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
            "/save": self.save_locus,
            "/load": self.load_locus,
            "/quit": sys.exit,
            "/exit": sys.exit,
        }

    def save_locus(self, args):
        if not args:
            self.command_board.append_text("require a file name")
        elif len(args) == 1:
            locus = self.command_board.data_manager.line_history
            with open(f'../save/{args[0]}.locus', 'w') as f:
                json.dump(locus, f)
            self.command_board.append_text("locus saved")
        else:
            self.command_board.append_text("invalid file name")

    def load_locus(self, args):
        if not args:
            self.command_board.append_text("require a file name")
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



