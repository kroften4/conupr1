def show_args(file_system, env_vars, args) -> str:
    return f"command: {args[0]}; args: {", ".join(args[1:])}\n"
