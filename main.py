import os
import tkinter
from tkinter import ttk
import sys

import binaries

if len(sys.argv) != 3:
    print("shesh: invalid arguments. Usage: shesh \"path/to/vfs.xml\" \"path/to/init/script\" ")
    exit(1)

SHESH_VFS_PATH = sys.argv[1]
SHESHRC_PATH = sys.argv[2]
if not os.path.isfile(SHESHRC_PATH):
    print("shesh: no file at specified path for init script")
    exit(1)

print(f"shesh: starting the VFS (VFS path: \"{SHESH_VFS_PATH}\", init script path: \"{SHESHRC_PATH}\")")

BINARIES = {
    "cd": binaries.show_args,
    "ls": binaries.show_args,
}
BUILTINS = ["exit"]
ENV_VARS = {"CWD": "/"}

def parse_args(command_string: str) -> list[str]:
    command_string = command_string.lstrip()
    args = []
    arg_idx = 0
    end_quote_char = None
    for i in range(len(command_string)):
        if arg_idx == len(args):
            args.append("")
        char = command_string[i]
        prev = command_string[i - 1]

        if len(args[arg_idx]) == 0:
            if char == "\"" or char == "'":
                end_quote_char = char

        if end_quote_char is None:
            if char == " " and prev == "\\":
                args[arg_idx] = args[arg_idx][:-1]
            if char != " " or prev == "\\":
                args[arg_idx] += char
            elif char == " " and prev != "\\" and prev != " ":
                arg_idx += 1
        else:
            if char != end_quote_char:
                args[arg_idx] += char
            elif len(args[arg_idx]) != 0:
                end_quote_char = None
    return args

def exec_command(command_string: str) -> str | None:
    args = parse_args(command_string)
    command_name = args[0]
    if command_name in BUILTINS:
        if command_name == "exit":
            window.destroy()
            exit(0)
    elif command_name in BINARIES:
        binary = BINARIES[command_name]
        return binary(ENV_VARS, args)
    else:
        return f"shesh: {args[0]}command not found"

def display_command(command_string: str) -> None:
    add_text(output_widget, f"{command_string}\n")
    command_output = exec_command(command_string)
    add_text(output_widget, command_output)

def process_user_input() -> None:
    command_string = input_field.get()
    display_command(command_string)

def add_text(text_widget, content):
    text_widget.config(state=tkinter.NORMAL)
    text_widget.insert(tkinter.END, content)
    text_widget.config(state=tkinter.DISABLED)
    text_widget.see(tkinter.END)

window = tkinter.Tk()
window.title(f"VFS")

input_field = ttk.Entry()

frame = ttk.Frame(window)
frame.pack(anchor=tkinter.NW)

scrollbar = ttk.Scrollbar(frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

output_widget = tkinter.Text(
    frame, 
    height=22,
    width=80,
    wrap=tkinter.WORD,
    yscrollcommand=scrollbar.set,
    state=tkinter.DISABLED,
    font=("Courier", 14)
)

scrollbar.config(command=output_widget.yview)

submit_btn = ttk.Button(text="Enter", command=process_user_input)

output_widget.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
input_field.pack(anchor=tkinter.W)
submit_btn.pack(anchor=tkinter.W)

for line in open(SHESHRC_PATH, "r").readlines():
    line = line.strip()
    if line == "" or line[0] == "#":
        continue
    if line.split()[0] not in BINARIES and line.split()[0] not in BUILTINS:
        continue
    display_command(line)

window.mainloop()
