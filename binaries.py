def show_args(env_vars, args) -> str:
    return f"command: {args[0]}; args: {", ".join(args[1:])}\n"
