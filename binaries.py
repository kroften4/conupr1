import shesh_os
import cal_utils
import datetime as dt
import copy

def pwd(file_system, env_vars, args) -> str:
    if len(args) > 1:
        return f"{args[0]}: too many args\n"
    return env_vars["CWD"] + "\n"

def ls(file_system, env_vars, args) -> str:
    if len(args) == 1:
        curr_dir = env_vars["CWD"]
    elif len(args) == 2:
        curr_dir = shesh_os.resolve_path(file_system, env_vars["CWD"], args[1])
    else:
        return f"{args[0]}: too many args\n"
    if not shesh_os.isdir(file_system, curr_dir):
        if shesh_os.isfile(file_system, curr_dir):
            return curr_dir.split("/")[-1] + "\n"
        else:
            return f"{args[0]}: no such file or directory\n"
    output: list[str] = []
    for entry in shesh_os.listdir(file_system, curr_dir):
        if shesh_os.isdir(file_system, shesh_os.join(curr_dir, entry)):
            entry += "/"
        output.append(entry)
    return " ".join(output) + "\n"

def cd(file_system, env_vars, args) -> str:
    if len(args) > 2:
        return f"{args[0]}: too many args\n"
    if len(args) < 2:
        return ""
    path: str = args[1]
    path = shesh_os.resolve_path(file_system, env_vars["CWD"], path)
    if not shesh_os.isdir(file_system, path):
        return f"{args[0]}: the directory does not exist\n"
    env_vars["CWD"] = path
    return ""

def show_args(file_system, env_vars, args) -> str:
    return f"command: {args[0]}; args: {", ".join(args[1:])}\n"

def cat(file_system, env_vars, args) -> str:
    if len(args) != 2:
        return f"{args[0]}: incorrect number of args\n"
    file = args[1]
    if not shesh_os.isfile(
        file_system,
        shesh_os.resolve_path(file_system, env_vars["CWD"], file)
    ):
        return f"{args[0]}: file does not exist\n"
    file = shesh_os.get_file_node(file_system, env_vars["CWD"], file)
    return file["content"].decode()

def head(file_system, env_vars, args) -> str:
    file: str = ""
    amount: int = 10
    if len(args) == 2:
        file = args[1]
    elif len(args) == 3:
        file = args[1]
        try:
            amount = int(args[2])
        except ValueError:
            return f"{args[0]}: second argument is not an integer\n"
    else:
        return f"{args[0]}: incorrect number of args\n"
    if not shesh_os.isfile(
        file_system,
        shesh_os.resolve_path(file_system, env_vars["CWD"], file)
    ):
        return f"{args[0]}: file does not exist\n"
    if amount <= 0:
        return f"{args[0]}: amount of lines must be > 0\n"
    output = shesh_os.get_file_node(
        file_system, env_vars["CWD"], file
    )["content"].decode().split("\n")[:amount]
    return "\n".join(output) + "\n"

def uniq(file_system, env_vars, args) -> str:
    if len(args) != 2:
        return f"{args[0]}: incorrect number of args\n"
    file = args[1]
    if not shesh_os.isfile(
        file_system,
        shesh_os.resolve_path(file_system, env_vars["CWD"], file)
    ):
        return f"{args[0]}: file does not exist\n"
    lines = shesh_os.get_file_node(
        file_system, env_vars["CWD"], file
    )["content"].decode().split("\n")
    output: list[str] = []
    for line in lines:
        if line not in output:
            output.append(line)
    return "\n".join(output) + "\n"

def cal(file_system, env_vars, args) -> str:
    if len(args) == 1:
        month = dt.datetime.now().month
        year = dt.datetime.now().year
        return cal_utils.month_cal(month, year)
    if len(args) == 2:
        try:
            year = int(args[1])
        except ValueError:
            return f"{args[0]}: argument is not a number\n"
        return cal_utils.multimonth_cal(1, year, 12)
    if len(args) == 3:
        try:
            month = int(args[1])
            year = int(args[2])
        except ValueError:
            return f"{args[0]}: argument is not a number\n"
        return cal_utils.month_cal(month, year)
    if len(args) == 4:
        try:
            month_start = int(args[1])
            year_start = int(args[2])
            month_number = int(args[3])
        except ValueError:
            return f"{args[0]}: argument is not a number\n"
        return cal_utils.multimonth_cal(month_start, year_start, month_number)
    return f"{args[0]}: incorrect number of arguments\n"

def cp(file_system, env_vars, args) -> str:
    if len(args) != 3:
        return f"{args[0]}: invalid number of arguments\n"
    cwd = env_vars["CWD"]
    source = shesh_os.resolve_path(file_system, cwd, args[1])
    dest = shesh_os.resolve_path(file_system, cwd, args[2])
    new_name: str = ""
    if not shesh_os.exists(file_system, source):
        return f"{args[0]}: node does not exist\n"
    if not shesh_os.isdir(file_system, dest):
        new_name = dest.split("/")[-1]
        dest = dest.split("/")[:-1]
        dest = "/" + "/".join(dest)
        if not shesh_os.isdir(file_system, dest):
            return f"{args[0]}: invalid path provided for destination\n"
    else:
        new_name: str = shesh_os.get_node(file_system, source)["name"]

    source = shesh_os.get_node(file_system, source)
    dest = shesh_os.get_node(file_system, dest)
    dest["content"][new_name] = copy.deepcopy(source)
    return ""

def rm(file_system, env_vars, args) -> str:
    nodepath: str = ""
    cwd = env_vars["CWD"]
    if len(args) == 2:
        nodepath = shesh_os.resolve_path(file_system, cwd, args[1])
        if shesh_os.isdir(file_system, nodepath):
            return f"{args[0]}: provide a `-r` flag to remove a directory\n"
    elif len(args) == 3:
        if args[1] != "-r":
            return f"{args[0]}: unknown argument\n"
        nodepath = shesh_os.resolve_path(file_system, cwd, args[2])
    else:
        return f"{args[0]}: invalid number of arguments\n"
    if nodepath == "/":
        return f"{args[0]}: cannot remove root\n"
    if not shesh_os.exists(file_system, nodepath):
        return f"{args[0]}: node does not exist\n"

    nodename: str = shesh_os.get_node(file_system, nodepath)["name"]
    parent_path: str = "/" + "/".join(nodepath[1:].split("/")[:-1])
    parent = shesh_os.get_node(file_system, parent_path)
    parent["content"].pop(nodename)

    return ""
