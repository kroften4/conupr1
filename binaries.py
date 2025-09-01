def ls(env_vars, args) -> str:
    return f"command: ls, args: {", ".join(args[1:])}\n"

def cd(env_vars, args) -> str:
    return f"command: cd, args: {", ".join(args[1:])}\n"
