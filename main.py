import os
import tkinter
from tkinter import ttk
import socket
import sys

import binaries

if len(sys.argv) != 3:
    print("shesh: invalid arguments. Usage: shesh \"path/to/vfs\" \"path/to/init/script\" ")
    exit(1)

SHESH_VFS_PATH = sys.argv[1]
SHESHRC_PATH = sys.argv[2]
if not os.path.isfile(SHESHRC_PATH):
    print("shesh: no file at specified path for init script")
    exit(1)
if not os.path.isdir(SHESH_VFS_PATH):
    print("shesh: no directory at specified path for vfs source")
    exit(1)

print(f"shesh: starting the VFS (VFS path: \"{SHESH_VFS_PATH}\", init script path: \"{SHESHRC_PATH}\")")

LOGIN = os.getlogin()
HOSTNAME = socket.gethostname()

window = tkinter.Tk()
window.title(f"VFS - {LOGIN}@{HOSTNAME}")

input_field = ttk.Entry()

output_field = ttk.Label()
output_field["text"] += "Welcome to shesh, a shell emulator\n"

FILE_SYSTEM = {}
BINARIES = {
    "cd": binaries.cd,
    "ls": binaries.ls,
    "pwd": binaries.pwd,
    "show_args": binaries.show_args
}
BUILTINS = ["exit"]
ENV_VARS = {"CWD": "/"}

def deserialize_file_system(path: str) -> dict:
    if not os.path.isdir(path):
        raise Exception("not a directory")
    result: dict = {}

    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path, entry)):
            result[entry] = deserialize_file_system(os.path.join(path, entry))
        if os.path.isfile(os.path.join(path, entry)):
            result[entry] = ""

    return result

FILE_SYSTEM = deserialize_file_system(SHESH_VFS_PATH)

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
    elif command_name in BINARIES:
        binary = BINARIES[command_name]
        return binary(FILE_SYSTEM, ENV_VARS, args)
    else:
        return f"shesh: {args[0]}: command not found\n"

def display_command(command_string: str) -> None:
    output_field["text"] += f"{LOGIN}@{HOSTNAME} {ENV_VARS["CWD"]}> {command_string}\n"
    command_output = exec_command(command_string)
    output_field["text"] += command_output

def process_user_input() -> None:
    command_string = input_field.get()
    display_command(command_string)

submit_btn = ttk.Button(text="Enter", command=process_user_input)

output_field.pack()
input_field.pack()
submit_btn.pack()

for line in open(SHESHRC_PATH, "r").readlines():
    line = line.strip()
    if line == "" or line[0] == "#":
        continue
    display_command(line)

window.mainloop()
