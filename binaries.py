import shesh_os
import cal_utils
import datetime as dt

def pwd(file_system, env_vars, args) -> str:
    if len(args) > 1:
        return f"{args[0]}: too many args\n"
    return env_vars["CWD"] + "\n"

def ls(file_system, env_vars, args) -> str:
    if len(args) > 1:
        return f"{args[0]}: too many args\n"
    output: list[str] = []
    curr_dir = env_vars["CWD"]
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

def tree(file_system, env_vars, args) -> str:
    output: str = ""
    return output

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
