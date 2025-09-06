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
        if dirname == "":
            continue
        if dirname not in cwd["content"]:
            return False
        if cwd["content"][dirname]["type"] == "file":
            return True
        cwd = cwd["content"][dirname]
    return True

def isfile(file_system: dict, path: str) -> bool:
    if path == "":
        return False
    if path[0] != "/":
        raise Exception("provided path is not absolute")
    if path[-1] == "/":
        path = path[:-1]
    cwd = file_system
    for dirname in path[1:].split("/"):
        if dirname == "":
            continue
        if dirname not in cwd["content"]:
            return False
        if cwd["content"][dirname]["type"] == "file":
            return True
        cwd = cwd["content"][dirname]
    return cwd["type"] == "file"

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
        if dirname not in cwd["content"]:
            return False
        if cwd["content"][dirname]["type"] == "file":
            return False
        cwd = cwd["content"][dirname]
    return cwd["type"] == "directory"

def resolve_path(file_system: dict, cwd: str, path: str) -> str:
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
        if dirname not in cwd["content"]:
            raise Exception("file does not exist")
        if cwd["content"][dirname]["type"] == "file":
            raise Exception("not a directory")
        cwd = cwd["content"][dirname]
    if cwd["type"] == "file":
        raise Exception("not a directory")
    return cwd

def get_node(file_system: dict, path: str) -> dict:
    cwd = file_system
    for node_name in path[1:].split("/"):
        if node_name == "":
            continue
        if node_name not in cwd["content"]:
            raise Exception("node does not exist")
        if cwd["content"][node_name]["type"] == "file":
            return cwd["content"][node_name]
        cwd = cwd["content"][node_name]
    return cwd

def get_file_node(file_system: dict, cwd: str, path: str):
    path = resolve_path(file_system, cwd, path)
    if not isfile(file_system, path):
        raise Exception("file does not exist")
    return get_node(file_system, path)

def listdir(file_system: dict, dirpath: str) -> Generator[str]:
    dir: dict = get_dir_dict(file_system, dirpath)
    for entry in dir["content"]:
        yield entry

def join(path1: str, path2: str) -> str:
    if path2[0] == "/":
        raise Exception("second path is absolute")
    if path1[-1] == "/":
        path1 = path1[:-1]
    return path1 + "/" + path2
