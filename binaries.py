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
