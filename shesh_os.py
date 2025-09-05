from typing import Generator

def exists(file_system: dict, path: str) -> bool:
    if path == "":
        return False
    if path[0] != "/":
        raise Exception("provided path is not absolute")
    if path[-1] == "/":
        path = path[:-1]
    cwd: dict = file_system
    for dirname in path.split("/"):
        if dirname not in cwd:
            return False
        if type(cwd[dirname]) == str:
            return True
        cwd = cwd[dirname]
    return True

def isfile(file_system: dict, path: str) -> bool:
    if path == "":
        return False
    if path[0] != "/":
        raise Exception("provided path is not absolute")
    if path[-1] == "/":
        path = path[:-1]
    cwd = file_system
    for dirname in path.split("/"):
        if dirname not in cwd:
            return False
        if type(cwd[dirname]) == str:
            return True
        cwd = cwd[dirname]
    return type(cwd) == str

def isabs(path: str) -> bool:
    if path == "":
        return False
    return path[0] == "/"

def isdir(file_system: dict, path: str) -> bool:
    if path == "":
        return False
    if not isabs(path):
        raise Exception("provided path is not absolute")
    if path[-1] == "/":
        path = path[:-1]
    cwd = file_system
    for dirname in path[1:].split("/"):
        if dirname == "":
            continue
        if dirname not in cwd:
            return False
        if type(cwd[dirname]) == str:
            return False
        cwd = cwd[dirname]
    return type(cwd) == dict

def resolve_path(file_systen: dict, cwd: str, path: str) -> str:
    if not isabs(cwd):
        raise Exception("provided cwd is not absolute")
    if not isabs(path):
        path = join(cwd, path)
    split_path: list[str] = path[1:].split("/")
    i = 0
    while i < len(split_path):
        dirname = split_path[i]
        if dirname == "..":
            if i - 1 >= 0:
                split_path.pop(i - 1)
                split_path.pop(i - 1)
                i -= 2
            else:
                split_path.pop(i)
                i -= 1
        i += 1
    path = "/" + "/".join(split_path)
    return path

def get_dir_dict(file_system: dict, dirpath: str) -> dict:
    cwd = file_system
    for dirname in dirpath[1:].split("/"):
        if dirname == "":
            continue
        if dirname not in cwd:
            raise Exception("file does not exist")
        if type(cwd[dirname]) == str:
            raise Exception("not a directory")
        cwd = cwd[dirname]
    if type(cwd) == str:
        raise Exception("not a directory")
    return cwd

def listdir(file_system: dict, dirpath: str) -> Generator[str]:
    dir: dict = get_dir_dict(file_system, dirpath)
    for entry in dir:
        yield entry

def join(path1: str, path2: str) -> str:
    if path2[0] == "/":
        raise Exception("second path is absolute")
    if path1[-1] == "/":
        path1 = path1[:-1]
    return path1 + "/" + path2
