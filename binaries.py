import shesh_os

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
