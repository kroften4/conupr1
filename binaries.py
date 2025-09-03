import os

def get_real_path(env_vars, path):
    if not os.path.isabs(path):
        path = os.path.join(env_vars["PWD"], path)
    return os.path.join(env_vars["VFS_PATH"], path[1:])

def pwd(env_vars, args) -> str:
    return env_vars["PWD"]

def ls(env_vars, args) -> str:
    output: list[str] = []
    real_dir = get_real_path(env_vars, env_vars["PWD"])
    for entry in os.listdir(real_dir):
        if os.path.isdir(os.path.join(real_dir, entry)):
            entry += "/"
        output.append(entry)
    return " ".join(output) + "\n"

def cd(env_vars, args) -> str:
    if len(args) > 2:
        return "cd: too many args\n"
    if len(args) < 2:
        return ""
    if not os.path.isdir(get_real_path(env_vars, args[1])):
        return "cd: the directory does not exist\n"
    new_path = os.path.abspath(os.path.join(env_vars["PWD"], args[1]))
    env_vars["PWD"] = new_path
    return ""

def show_args(env_vars, args) -> str:
    return f"command: cd, args: {", ".join(args[1:])}\n"

def touch(env_vars, args) -> str:
    if len(args) < 2:
        return "touch: missing file operand\n"
    if not os.path.isabs(args[1]):
        args[1] = os.path.join(env_vars["PWD"], args[1])
    location, filename = os.path.split(args[1])
    location = os.path.abspath(location)
    real_dir = get_real_path(env_vars, location)
    if not os.path.isdir(real_dir):
        return "touch: no such file or directory\n"
    filepath = os.path.join(real_dir, filename)
    if os.path.exists(filepath):
        return ""
    open(filepath, "w").close()
    return ""

def mkdir(env_vars, args) -> str:
    path = os.path.abspath(os.path.join(env_vars["PWD"], args[1]))
    real_path = get_real_path(env_vars, path)
    if os.path.exists(real_path):
        return "mkdir: file already exists\n"
    os.mkdir(real_path)
    return ""
