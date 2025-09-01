import os
import tkinter
from tkinter import ttk
import socket

LOGIN = os.getlogin()
HOSTNAME = socket.gethostname()

window = tkinter.Tk()
window.title(f"VFS - {LOGIN}@{HOSTNAME}")

input_field = ttk.Entry()
input_field.pack()

output = ttk.Label()
output.pack()

COMMANDS = ["cd", "ls", "ipaddr", "exit"]

def parse_command(string: str) -> str:
    args = string.split()
    if args[0] not in COMMANDS:
        return f"unknown command: {args[0]}"
    for arg in args[1:]:
        if arg[0] != "\"" or arg[-1] != "\"" or arg.count("\"") != 2:
            return f"Error: {args[0]}: invalid quotes argument {arg}"
    if args[0] == "exit":
        window.destroy()
    return f"Success: command <{args[0]}>, args: {", ".join(args[1:])}"

def process_command():
    command = input_field.get()
    output["text"] += f"{LOGIN}@{HOSTNAME} > {command}\n"
    output["text"] += parse_command(command)+ "\n"

submit_btn = ttk.Button(text="Enter", command=process_command)
submit_btn.pack()

window.mainloop()
